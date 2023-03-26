from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from customers.models import CompleteProfile,Products,Cart,Cartitems,OrderItem,Reviews,DeliveryProfile,Delivery
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
from django.http import HttpResponse
import json
from AgroBasket.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
import razorpay
from django.core.mail import send_mail

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %matplotlib inline
plt.style.use("ggplot")

import sklearn
from sklearn.decomposition import TruncatedSVD
from django.templatetags.static import static

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def home(request):
    return render(request,'customerhome.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Success!")
            return redirect("/")
        else:
            messages.info(request,'Invalid cedentials')
            return redirect('/login')
    else:
        return render(request,'customerlogin.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username = username, password=password1, email=email)
                user.save()
                send_mail(
                    subject = 'Welcome to AgroBasket',
                    message = request.POST['username'] + '' + ' we are happy to have you here',
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [request.POST['email']],
                    fail_silently=False,
                )
                print('user created')
                return redirect('/login')
        else:
            messages.info(request,'Password not matching..')
            return redirect('/register')
    else:
         return render(request,'customerregister.html')

def logout(request):
   auth.logout(request)
   return redirect('/')

def createprofile(request):
    if request.method == "POST":
        user_profile = CompleteProfile()
        print(request.user)
        user_profile.username = request.user
        user_profile.fullName = request.POST.get('fullname')
        user_profile.emailAddress = request.POST.get('email')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')
        user_profile.zipcode = request.POST.get('zip')
        user_profile.save()
        return redirect('userprofile')
  
def userprofile(request):
    existingprofile = len(CompleteProfile.objects.filter(username=request.user))
    if existingprofile>0:
        profiledetails = CompleteProfile.objects.get(username = request.user)
        context = {"existingprofile":existingprofile,"profiledetails":profiledetails}
        return render(request,"customerprofile.html",context)
    else:
        context = {"existingprofile":existingprofile}
        return render(request,"customerprofile.html",context)

def updateprofile(request):
    user_profile = CompleteProfile.objects.get(username = request.user)
    if request.method == "POST":
        user_profile.fullName = request.POST.get('fullname')
        user_profile.emailAddress = request.POST.get('email')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')
        user_profile.zipcode = request.POST.get('zip')
        user_profile.save()
        return redirect('userprofile')
    return render(request,'customerprofileupdate.html',{"user_profile":user_profile})

def customerproducts(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
        allProducts = Products.objects.all()
        return render(request, 'customerproducts.html', {'allProducts': allProducts,'cart':cart})
    allProducts = Products.objects.all()
    print(allProducts)
    return render(request,"customerproducts.html",{"allProducts":allProducts})

def customerproductDetail(requests):
    return render(requests, 'customerproductDetail.html')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
        cartitems = cart.cartitems_set.all()
        
    else:
        cartitems = []
        cart = {"get_cart_total": 0, "get_itemtotal": 0}

    return render(request, 'cart.html', {'cartitems' : cartitems, 'cart':cart})

def updateCart(request):
    data = json.loads(request.body)
    print("in")
    productId = data["productId"]
  
    action = data["action"]
    product = Products.objects.get(id=productId)
    customer = request.user
    cart, created = Cart.objects.get_or_create(customer = customer, completed = False)
    cartitem, created = Cartitems.objects.get_or_create(cart = cart, product = product)

    #If you add the same item twice it will basically increase the cart quantity
    if action == "add":
        cartitem.quantity += 1
        cartitem.save()

    return JsonResponse("Cart Updated", safe = False)

def updateQuantity(request):
    data = json.loads(request.body)
    quantityFieldValue = data['qfv']
    quantityFieldProduct = data['qfp']
    product = Cartitems.objects.filter(product__name = quantityFieldProduct).last()
    product.quantity = quantityFieldValue
    product.save()
    return JsonResponse("Quantity updated", safe = False)

def track(request):
    allOrders = OrderItem.objects.filter(username = request.user)
    
    return render(request,"customertrack.html", {"allOrders":allOrders})

def productDetail(request, slug):
    prod = Products.objects.filter(slug = slug).first()
    allreviews = Reviews.objects.filter(product_id = prod.id)
    
    context = {'prod': prod,'allreviews':allreviews}
    return render(request , 'productdetail.html', context)

client = razorpay.Client(auth=("rzp_test_yOgTa9YwwHLKDR", "qDmtqkDq7Rs3OIpFDd7JDtRR"))
def checkout(request,token):
    cartitems = Cart.objects.get(cart_id=token)
    allcartprod = Cartitems.objects.filter(cart=cartitems)
    totalprice = []
    for prod in allcartprod:
        totalprice.append(float(prod.product.price)*float(prod.quantity))

    Amount = sum(totalprice)
    order_amount = Amount*100
    print(order_amount)
    order_currency = 'INR'
    payment = client.order.create(dict(amount = order_amount, currency= order_currency,payment_capture = 1))
    payment_id = payment['id']

    orders = OrderItem()
    order_items_for_pdf = OrderItem.objects.filter(cartid=cartitems)
    print(len(OrderItem.objects.filter(cartid=cartitems)))
    user_detail = CompleteProfile.objects.get(username = request.user)
    print(user_detail)
    if len(OrderItem.objects.filter(cartid = cartitems )) == 0:
        orders.username = request.user
        orders.cartid = cartitems
        orders.total_amount = Amount
        orders.modeofdelivery = "Electric Vehicle"
        orders.order_location = user_detail.city
        orders.email = user_detail.emailAddress
        orders.zip_code = user_detail.zipcode
        orders.save()
        print("saved successfully!")
    context={'order_amount':order_amount,'api_key':RAZORPAY_API_KEY,'payment_id':payment_id}
    data = {
        'products': order_items_for_pdf,
        'order_amount':order_amount,
    }
    generate_pdf(data)

    return render(request,'payment.html',context)

def productSearch(request):
    query=request.GET['query']
    allProd= Products.objects.filter(name__icontains=query)
    params = {'allProd': allProd}
    return render(request, 'productSearch.html', params)


def reviews(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            ratings = request.POST.get('ratings')
            reviews = request.POST.get('review')
        
        reviews_detail = Reviews()
        reviews_detail.rating = ratings
        reviews_detail.review = reviews
        reviews_detail.product_id = id
        reviews_detail.username = request.user
        reviews_detail.save()
        print("Reviews saved successfully!")

        return redirect("customerproducts")
    
    return render(request,"customerproducts.html")


def devlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Success!")
            return redirect("/devhome")
        else:
            messages.info(request,'Invalid cedentials')
            return redirect('/devlogin')
    else:
        return render(request,'devlogin.html')

def devlogout(request):
   auth.logout(request)
   return redirect('/devhome')

def devhome(request):
    user_details = DeliveryProfile.objects.get(username = request.user)
    usercode = user_details.zipcode
    allActiveOrders = OrderItem.objects.filter(zip_code = usercode)
    
    return render(request,"devhome.html",{"allActiveOrders":allActiveOrders})
        

def devorders(request):
    alldevorders = OrderItem.objects.filter(devname = request.user)
    print(alldevorders)
    return render(request,"devorders.html",{"alldevorders":alldevorders,})

def updatedeliverystatus(request,cartid):
    if request.user.is_authenticated:
        order_status = OrderItem.objects.get( cartid= cartid) 
        print(request.user)
        order_status.devname = str(request.user)
        order_status.shipped_status = "True"
        order_status.save()
        send_mail(
                    subject = 'Update on Your Order Status',
                    message = 'Your product is out for delivery',
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [order_status.email],
                    fail_silently=False,
                )
    
        return redirect('devhome')
    
def updatefinalstatus(request,cartid):
    if request.user.is_authenticated:
        order_status = OrderItem.objects.get( cartid= cartid)
        print("yes")
        order_status.delivery_status = "True"
        order_status.save()
        send_mail(
                    subject = 'Update on Your Order Status',
                    message = 'Your product is delivered',
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [order_status.email],
                    fail_silently=False,
                )
        return redirect('devorders')

def recoomendation_function():
    amazon_ratings = pd.read_csv(static('Crops1.csv'))
    amazon_ratings = amazon_ratings.dropna()
    amazon_ratings.head()
    popular_products = pd.DataFrame(amazon_ratings.groupby('ProductId')['Rating'].count())
    most_popular = popular_products.sort_values('Rating', ascending=False)
    most_popular.head(10)
    
def generate_pdf(data):
    # Get the HTML template
    template = get_template('./invoice.html')

    # Render the template with context data
    context = {'name': 'AgroBasket',
               'products': data,
               }
    html = template.render(context)

    # Create a response object with the PDF data
    response1 = HttpResponse(content_type='application/pdf')
    response1['Content-Disposition'] = 'attachment; filename="my_pdf.pdf"'

    # Create a PDF object
    pdf = pisa.CreatePDF(html, dest=response1)

    # If PDF creation failed, return an error response
    if pdf.err:
        return HttpResponse('Error generating PDF file')

    # Close the PDF object cleanly, and we're done.

    # Return the response object
    return response1
