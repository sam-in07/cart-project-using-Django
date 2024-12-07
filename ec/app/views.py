
from django.shortcuts import render,redirect
from django.db.models import Count
from . models import Cart, Customer, Product
from django.views import View
from django.http import JsonResponse
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
# views.py
from .models import Customer
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,"app/home.html")
def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")


class CategoryView(View):
    def get(self,request,val):
        product =Product.objects.filter(category=val)
        title =Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())


class CategoryTitle(View):
    def get(self,request,val):
        product =Product.objects.filter(category=val)
        title =Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())


    
class ProductDetail(View):
    def get(self, request, pk):
      product = Product.objects.get(pk=pk)
      return render(request, "app/productdetail.html",locals())
       

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {'form': form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registered successfully.")
            return redirect('login')  # Redirect to the login page or another relevant page
        else:
            messages.warning(request, "Invalid input data")
            return render(request, "app/customerregistration.html", {'form': form})
        
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()  # Corrected the typo
        return render(request, 'app/profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
    
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            # Save the customer profile
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            
            messages.success(request, "Congratulations! Profile saved successfully.")
            # Redirect to avoid resubmission on refresh
           
        
        else:
            messages.warning(request, "Invalid input data.")
            return render(request, 'app/profile.html', locals())
        

def address(request):        
    add =Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request, pk):
       form = CustomerProfileForm(request.POST)
        
       if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name =form.changed_data['name']
            add.locality =form.cleaned_data['locality']
            add.city =form.cleaned_data['city']
            add.mobile =form.cleaned_data['mobile']
            add.state =form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()  
            messages.success(request, "Congratulations! Profile updated successfully.")
          
            
       else:
            messages.warning(request, "Invalid input data.")
            return redirect("address")
        


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart =Cart.objects.filter(user=user)
    amount =0
    for p in cart:
        value =p.quantity * p.product.discounted_price
        amount =amount +value
    totalamount =amount +40    
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
    
        return render(request,'app/checkout.html',locals())

def plus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        user =request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart :
            value =p.quantity *p.product.discounted_price
            amount =amount +value
            totalamount =amount +40

        print(prod_id)
        data={
               'quantity':c.quantity,
               'amount': amount,
               'totalamount':totalamount
        }
        return JsonResponse(data)
    
 
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        user =request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart :
            value =p.quantity *p.product.discounted_price
            amount =amount +value
            totalamount =amount +40

        print(prod_id)
        data={
               'quantity':c.quantity,
               'amount': amount,
               'totalamount':totalamount
        }
        return JsonResponse(data)   
    

    
def remove_cart(request):
    if request.method =='GET':
        prod_id=request.GET['prod_id']
        c =Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user =request.user
        cart =Cart.objects.filter(user=user)
        amount =0
        for p in cart :
            value =p.quantity *p.product.discounted_price
            amount =amount +value
            totalamount =amount +40

        print(prod_id)
        data={
               'quantity':c.quantity,
               'amount': amount,
               'totalamount':totalamount
        }
        return JsonResponse(data)