from django.shortcuts import render, HttpResponse, redirect
from .models import *
# Create your views here.

def first(request):
    return HttpResponse('this is my first view...')

def demo(request):
    return render(request, 'demo.html')

def style(request):
    return render(request, 'style.html')

def show(request):
    data = Student.objects.all()
    print(data)
    #for i in data:
    #    print(i.name)
    return render(request, 'show.html',{'student': data})

def showimg(request):
    dataimg = Img.objects.all()
    return render(request, 'showimg.html',{'dataimg': dataimg}) 

def store(request):
    if request.method == 'POST':
        print("This is first line after POST method")
        store_data  = Student()
        store_data.email = request.POST.get('email')
        store_data.name = request.POST.get('uname')
        store_data.save()
    return render(request, 'store.html')

#def storeget(request):
    if request.method == 'GET':
        print(name,email)
        #store_data  = Student()
        email = request.GET.get('email')
        name = request.GET.get('uname')
    return render(request, 'storeget.html')

def storeimg(request):
    if request.method == 'POST'and request.FILES:
        store_image  = Img()
        store_image.name = request.POST['name']
        store_image.image = request.FILES['image']
        store_image.save()
    return render(request, 'storeimg.html')



def register(request):
    if request.method == 'POST':
        sign_up = Registration(email=request.POST['email'], 
                               name =request.POST['name'],
                               mob = request.POST['mob'], 
                               address = request.POST['add'],
                               password = request.POST['password'])
        try:    
            already_reg =  Registration.objects.get(email = request.POST['email'])
            if already_reg:
                return render(request, 'register.html', {'already': 'Email already registered!! '})
        except:
            sign_up.save()
            return render(request, 'register.html', {'registration': 'Registration Successful'})
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        try:
            is_present = Registration.objects.get(email=request.POST['email'])
            if is_present:
                if request.POST['password'] == is_present.password:
                    request.session['login'] = is_present.email
                    return redirect('index')
                
            
                else:
                    return render(request, 'login.html', {'wrong_pass': 'Invalid Password'}) 
        except:
            return render(request, 'login.html', {'error': 'Email not registered'})
    else:    
        return render(request, 'login.html')
    


def index(request):
    cat = Category.objects.all()
    if 'login' in request.session:
        return render(request, 'index.html', {'cat': cat, 'logged_in' : True})
    
    else:
        return render(request, 'index.html', {'cat': cat})
    
def logout(request):
    del request.session['login']
    return redirect('index')

def product(request, id):
    pro = Product.objects.filter(category=id)
    if 'login' in request.session:
        
        return render(request, 'product.html',{'pro': pro, 'logged_in': True})
    else:
        return render(request, 'product.html',{'pro': pro,})
    
def product_detail(request,id):
    prod = Product.objects.get(pk=id)
    if 'login'in request.session:
        return render(request, 'product1.html',{'product':prod,'logged_in': True})
    else:
        return render(request, 'product1.html',{'product':prod})

def profile(request):
    if 'login' in request.session:
        logged_user = Registration.objects.get(email = request.session['login'])
        return render(request, 'profile.html',{'logged_in': True, 'logged_user': logged_user})
    else:
        return redirect('login')