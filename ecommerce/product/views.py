from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Product, Category, Signup, Order
from django.contrib.auth.hashers import check_password, make_password
from django.views import View
from .middlewares.auth_user import simple_middleware
from django.utils.decorators import method_decorator
# Create your views here.


class Index(View):

    def get(self, request, id=None):

        product = None

        if id != None:
            product = Product.get_product_filter(id)
        else:
            product = Product.get_all_product()

        category = Category.get_all_category()
        a = request.session.get('email')
        context = {'product': product, 'category': category, 'a': a}
        return render(request, 'product/index.html', context)

    def post(self, request, id=None):

        product_id = request.POST.get('productid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            qty = cart.get(product_id)
            if qty:
                if remove:
                    if qty == 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = qty - 1
                else:
                    cart[product_id] = qty + 1
            else:
                cart[product_id] = 1

        else:
            cart = {}
            cart[product_id] = 1

        request.session['cart'] = cart
        print(request.session.get('email'), '--->', request.session['cart'])

        return redirect('index')


class signup(View):
    def get(self, request):
        return render(request, 'product/signup.html')

    def post(self, request):
        error_msg = None

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(fname, lname, email, password)
        values = {'fname': fname, 'lname': lname, 'email': email}
        customer = Signup(first_name=fname, last_name=lname,
                          email=email, password=password)

        if len(fname) < 4:
            error_msg = "First Name Must Be More Than 4 Character"
        elif len(lname) < 4:
            error_msg = "Last Name Must Be More Than 4 Character"
        elif customer.is_exist():
            error_msg = "Email is Registered"

        if not error_msg:
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('index')

        else:

            context = {'error': error_msg, 'values': values}
            return render(request, 'product/signup.html', context)


class Login(View):

    return_url = None
    def get(self, request):
        Login.returnurl = request.GET.get('return_url')
        print('url--->',Login.returnurl)
        return render(request, 'product/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_msg = None
        customer = Signup.customer_check_by_email(email)

        if customer:

            flag = check_password(password, customer.password)

            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = customer.email

                if Login.returnurl:
                    return HttpResponseRedirect(Login.returnurl)
                else:
                    Login.returnurl = None
                    return redirect('index')
            else:
                error_msg = "email or password invalid"

        else:
            error_msg = "email or password invalid"

        context = {'error': error_msg}
        return render(request, 'product/login.html', context)


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):

    def get(self, request):
        cart = request.session.get('cart')
        if cart:
            pass
        else:
            request.session['cart'] = {}

        ids = request.session.get('cart').keys()
        print(request.session.get('cart').values())
        product_detail = Product.get_product_detail(ids)
        context = {'products': product_detail}
        return render(request, 'product/cart.html', context)


class Checkout(View):

    def post(self, request):
        customer = request.session.get('customer')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Product.get_product_detail(list(cart.keys()))

        print('checkout--->', products)
        print('checkout--->', cart)
        print('checkout--->', customer)

        for productx in products:

            order = Order(product=productx, customer=Signup(
                id=customer), qty=cart.get(str(productx.id)), price=productx.price, address=address, phone=phone)

            order.save()
        request.session['cart'] = {}
        return redirect('index')


class Placeorder(View):
    @method_decorator(simple_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        if customer:
            order = Order.get_order_by_id(customer)
            customer_name = Signup.get_customer_detail(customer)

            context = {'order': order, 'customer_name': customer_name}
            return render(request, 'product/placeorder.html', context)
        else:
            return render(request, 'product/placeorder.html')

    def post(self, request):
        context = {}
        return render(request, 'product/placeorder.html', context)
