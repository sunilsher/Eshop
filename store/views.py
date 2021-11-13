from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from django.http import HttpResponse
from .models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.views import View


def index(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    return render(request, 'index.html', data)


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email

        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()

            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = "First Name Required!!"
        elif len(customer.first_name) < 4:
            error_message = "First name must be 4 character long or long"
        elif not customer.last_name:
            error_message = "Last Name Required"
        elif len(customer.last_name) < 4:
            error_message = 'Last name must be 4 character or more'
        elif not customer.phone:
            error_message = 'Phone Number Required '
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 Character long'
        elif len(customer.password) < 6:
            error_message = 'password must be 6 character long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 character long'
        elif customer.isExists:
            error_message = 'Email Already Registered..'
            # saving
        return error_message


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('homepage')
            else:
                error_message = 'Email or Password invalid'
        else:
            error_message = "Email or Password Invalid!!"
        print(email, password)
        return render(request, 'login.html', {'error': error_message})

