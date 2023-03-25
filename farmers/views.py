from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from customers.models import Products
from farmers.models import FarmerProfile

# Create your views here.
def farmerregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('farmerregister')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('farmerregister')
            else:
                user = User.objects.create_user(username = username, password=password1, email=email)
                user.save()
                print('user created')
                return redirect('farmerlogin')
        else:
            messages.info(request,'Password not matching..')
            return redirect('farmerregister')
        
    else:         
       return render(request, 'farmerregister.html')
    

def farmerlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Success!")
            return redirect("farmerhome")
        else:
            messages.info(request,'Invalid cedentials')
            return redirect('farmerlogin')
    else:
        return render(request, 'farmerlogin.html')

def farmerhome(request):
    return render(request, 'farmerhome.html')

def farmerlogout(request):
   auth.logout(request)
   return redirect('farmerlogin')

def farmerproduct(request):
   current_details = FarmerProfile.objects.get(username = request.user)
   company_name = current_details.comp_name
   print(company_name)
   allProducts = Products.objects.filter(comp_name = company_name)

   return render(request, 'farmerproduct.html',{"allProducts":allProducts})

def farmerprofile(request):
    existingprofile = len(FarmerProfile.objects.filter(username=request.user))
    if existingprofile>0:
        profiledetails = FarmerProfile.objects.get(username = request.user)
        context = {"existingprofile":existingprofile,"profiledetails":profiledetails}
        return render(request, 'farmerprofile.html', context)
    else:
        context = {"existingprofile":existingprofile,}
        return render(request, 'farmerprofile.html', context)

def createprofile(request):
    if request.method == "POST":
        user_profile = FarmerProfile()
        print(request.user)
        user_profile.username = request.user
        user_profile.fullName = request.POST.get('fullname')
        user_profile.emailAddress = request.POST.get('email')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')
        user_profile.zipcode = request.POST.get('zip')
        user_profile.comp_name = request.POST.get('compName')
        user_profile.save()
        return redirect('farmerprofile')

def updateprofile(request):
    user_profile = FarmerProfile.objects.get(username = request.user)
    if request.method == "POST":
        user_profile.fullName = request.POST.get('fullname')
        user_profile.emailAddress = request.POST.get('email')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.state = request.POST.get('state')
        user_profile.zipcode = request.POST.get('zip')
        user_profile.comp_name = request.POST.get('compName')
        user_profile.save()
        return redirect('farmerprofile')
    return render(request,'customerprofileupdate.html',{"user_profile":user_profile})

def farmerupload(request):
    if request.method == 'POST':
        farmProd = Products()
        prodName = request.POST.get('prodName')
        compName = request.POST.get('compName')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        discPrice= request.POST.get('discPrice')
        coupons = request.POST.get('coupons')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        farmProd.name = prodName
        farmProd.comp_name = compName
        farmProd.desc = desc
        farmProd.price = price
        farmProd.discounted_price =discPrice
        farmProd.image = image
        farmProd.save()
        return redirect('farmerproduct')
    else:
        return render(request , 'farmerupload.html')
    


def updateproduct(request,id):
    product_details = Products.objects.get(id=id)
    if request.method == "POST":
        product_details.name = request.POST.get('prodName')
        product_details.comp_name = request.POST.get('compName')
        product_details.desc = request.POST.get('desc')
        product_details.price = request.POST.get('price')
        product_details.category = request.POST.get('category')
        product_details.image = request.FILES.get('image')
        product_details.save()
        print("Successfully updated!")
    return render(request,'updateproduct.html',{"product_details":product_details})