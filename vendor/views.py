from django.shortcuts import render
from .models import * 
# Create your views here.


def registaration_ven(request):
    data = TYPE_BUSINESS
    if request.method == 'POST':
        sign_up = Ven_reg(email = request.POST['email'],
                               name = request.POST['name'],
                               mob = request.POST['mob'],
                               add = request.POST['add'],
                               password = request.POST['password'],
                               sell_type = request.POST['bt'])
        try:
            already_reg = Ven_reg.objects.get(email = request.POST['email'])
            if already_reg:
                return render(request,'vendor/register.html',{'already':"Email already exists..",})   
        except:
            sign_up.save()
            return render(request,'vendor/register.html',{'registration':"Registration successfull.",'type':data})
            # return redirect('login')
    else:
        return render(request,'vendor/register.html',{'type':data})