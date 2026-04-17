from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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
        hashed_password = make_password(request.POST['password'])
        sign_up = Registration(email=request.POST['email'], 
                               name =request.POST['name'],
                               mob = request.POST['mob'], 
                               address = request.POST['add'],
                               password = hashed_password)
        try:    
            already_reg =  Registration.objects.get(email = request.POST['email'])
            if already_reg:
                return render(request, 'register.html', {'already': 'Email already registered!! '})
        except:
            sign_up.save()
            messages.success(request, 'Registration Successful! Welcome to Dj E-Commerce.')
            return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        try:
            is_present = Registration.objects.get(email=request.POST['email'])
            if is_present:
                if check_password(request.POST['password'], is_present.password) or request.POST['password'] == is_present.password:
                    # Upgrade password hashing if plain text matches
                    if request.POST['password'] == is_present.password:
                        is_present.password = make_password(request.POST['password'])
                        is_present.save()

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

def add_to_cart(request, id):
    if 'login' in request.session:
        qty = int(request.POST.get('qty', 1))
        user = Registration.objects.get(email=request.session['login'])
        product = Product.objects.get(id=id)
        
        cart_obj, created = Cart.objects.get_or_create(user=user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart_obj, product=product)
        
        if not item_created:
            cart_item.quantity += qty
        else:
            cart_item.quantity = qty
        cart_item.save()
        return redirect('cart')
    return redirect('login')

def cart(request):
    if 'login' in request.session:
        user = Registration.objects.get(email=request.session['login'])
        cart_obj = Cart.objects.filter(user=user).first()
        cart_items = cart_obj.items.all() if cart_obj else []
        total = sum([item.get_total_price() for item in cart_items])
        
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'logged_in': user})
    return redirect('login')

def checkout(request):
    if 'login' in request.session:
        user = Registration.objects.get(email=request.session['login'])
        cart_obj = Cart.objects.filter(user=user).first()
        cart_items = cart_obj.items.all() if cart_obj else []
        total = sum([item.get_total_price() for item in cart_items])
        
        if request.method == 'POST':
            if not cart_obj or not cart_items:
                return redirect('cart')
            
            name = request.POST.get('name')
            email = request.POST.get('email')
            mob = request.POST.get('mob')
            address = request.POST.get('add')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            pin = request.POST.get('pin')
            paymentvia = request.POST.get('paymentvia')
            
            order = Order.objects.create(
                user=user, name=name, email=email, mobile=mob, address=address,
                city=city, state=state, country=country, pincode=pin,
                total_amount=total, payment_method=paymentvia
            )
            
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
            
            # clear the cart
            if cart_obj:
                cart_obj.delete()
            
            if paymentvia == 'online':
                return redirect('payment', order_id=order.id)
            else:
                return HttpResponse("Order Placed Successfully! (Cash on Delivery)") 
                
        return render(request, 'checkout.html', {'cart_data': cart_items, 'total': total, 'logged_in': user})
    return redirect('login')

def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    # Using test keys
    razorpay_merchant_key = "rzp_test_SefNhMt82MChpI"
    razorpay_merchant_secret = "PahYR7VvY7QeBDcfSPOsbnc9"
    
    try:
        client = razorpay.Client(auth=(razorpay_merchant_key, razorpay_merchant_secret))
        data = { "amount": order.total_amount * 100, "currency": "INR", "receipt": f"order_{order.id}" }
        payment_order = client.order.create(data=data)
        
        order.razorpay_order_id = payment_order['id']
        order.save()
        
        context = {
            'razorpay_merchant_key': razorpay_merchant_key,
            'razorpay_amount': order.total_amount * 100,
            'currency': 'INR',
            'razorpay_order_id': payment_order['id'],
            'callback_url': '/payment_verify/',
        }
        return render(request, 'razorpay.html', context)
    except:
        return HttpResponse("Razorpay keys are invalid placeholders. Please add your test keys.")

@csrf_exempt
def payment_verify(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        
        razorpay_merchant_key = "rzp_test_SefNhMt82MChpI"
        razorpay_merchant_secret = "PahYR7VvY7QeBDcfSPOsbnc9"
        client = razorpay.Client(auth=(razorpay_merchant_key, razorpay_merchant_secret))
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            order.payment_status = 'Paid'
            order.save()
            return HttpResponse("Payment Successful!")
        except:
            order.payment_status = 'Failed'
            order.save()
            return HttpResponse("Payment Failed! Signature mismatch.")
    return redirect('index')

def order_history(request):
    if 'login' in request.session:
        user = Registration.objects.get(email=request.session['login'])
        orders = Order.objects.filter(user=user).order_by('-created_at')
        return render(request, 'order_history.html', {'orders': orders, 'logged_in': True})
    return redirect('login')