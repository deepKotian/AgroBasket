from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

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
   return render(request, 'farmerproduct.html')

def farmerprofile(request):
   return render(request, 'farmerprofile.html')

def farmerupload(request):
   return render(request, 'farmerupload.html')