from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from customers.models import CompleteProfile,Products,Cart,Cartitems
from django.http import JsonResponse
import json
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
            return redirect('login')
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
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password=password1, email=email)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'Password not matching..')
            return redirect('register')

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
    profiledetails = CompleteProfile.objects.get(username = request.user)
    context = {"existingprofile":existingprofile,"profiledetails":profiledetails}
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
    return render(request,"customertrack.html")


def productDetail(request):
    return render(request,"productDetail.html")