from math import prod
from nis import cat
from time import timezone
from django.db.models import Avg
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import re
import random
from urllib import request
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from ecomapp.models import Banner, Brand, Category, Coupon, Location, Order, OrderItems, Product, Reviews, SubCategory, User, Wishlist
from .constants import const_page_number
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views herej.
def notfound_404(req):
    return render(req, "error404.html")


def home(req):
    home_category_products = []
    categories = Category.objects.all()[:10]
    wishlist = Wishlist.objects.all()
    sub_categories = SubCategory.objects.all()[:10]

    time_threshold = datetime.now() - timedelta(hours=24)

    todays_deals = Product.objects.filter(created_at__gt=time_threshold)

    brands = Brand.objects.all()[:5]
    popular_categories = Category.objects.filter(is_popular=True)
    latest_products = Product.objects.all().order_by("created_at")[:5]
    home_cate = Category.objects.filter(in_home=True)
    banners = Banner.objects.all()[:3]
    for i in range(len(home_cate)):
        home_category_products.append(
            {"category_slug": home_cate[i].slug, "category_name": home_cate[i].title,
             "wlists": len(wishlist),
             "products": Product.objects.filter(category=home_cate[i])})

    return render(req, "ecomapp/home.html", {
        "categories": categories,
        "banners": banners,
        "sub_categories": sub_categories,
        "home_category_products": home_category_products,
        "latest_products": latest_products,
        "popular_categories": popular_categories,
        "todays_deals": todays_deals,
        "brands": brands})


def aboutus(req):
    return render(req, "ecomapp/aboutus.html")


def contactus(req):
    return render(req, "ecomapp/contactus.html")


def login_user(req):
    if req.user.is_authenticated:
        return redirect(reverse("ecomapp:home"))
    if req.method == "POST":
        try:
            email = req.POST.get("email")
            password = req.POST.get("password")
            user = User.objects.filter(email=email)
            if len(user) == 0:
                messages.error(req, 'Either wrong username or password.')
                return render(req, "login.html")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(req, user)
                next = req.GET.get("next")
                if next is not None:
                    return redirect(f'{next}')

                return redirect(reverse("ecomapp:home"))

            else:
                messages.error(req, 'Either wrong username or password tala.')
                return render(req, "login.html")
        except:
            messages.error(req, 'Something Went Wrong.')

    return render(req, "login.html")


def register_user(req):
    if req.user.is_authenticated:
        return redirect(reverse("ecomapp:home"))
    if req.method == "POST":
        try:
            firstname = req.POST.get("firstname")
            if not re.match(r"^[A-Za-z]+$", firstname):
                messages.error(req, 'Please enter a valid firstname.')
                return render(req, "register.html")
            lastname = req.POST.get("lastname")
            if not re.match(r"^[A-Za-z]+$", lastname):
                messages.error(req, 'Please enter a valid lastname.')
                return render(req, "register.html")
            email = req.POST.get("email")
            if not re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email):
                messages.error(req, 'Please enter a valid email.')
                return render(req, "register.html")
            password = req.POST.get("password")
            user = User.objects.filter(email=email)
            if len(user) != 0:
                messages.error(req, 'User with this email already exist.')
                return render(req, "register.html")
            user = User.objects.create_user(
                email=email, first_name=firstname, last_name=lastname, password=password)
            user = authenticate(email=email, password=password)
            login(req, user)
            next = req.GET.get("next")
            if next is not None:
                return redirect(f'{next}')
            return redirect(reverse("ecomapp:home"))
            messages.success(req, 'User successfully created.')
        except:
            messages.error(req, 'Something Went Wrong.')
            return render(req, "register.html")
    return render(req, "register.html")


def brand_list(req):
    brands = Brand.objects.all()
    page = req.GET.get('page', 1)
    paginator = Paginator(brands, const_page_number)
    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)
    return render(req, "ecomapp/brands.html", {"brands": brands})


def products_by_brand(req, slug):
    products = []
    brand = Brand.objects.filter(slug=slug)
    if len(brand) == 0:
        return render(req, "error404.html")
    products_list = Product.objects.filter(brand=brand[0])

    page = req.GET.get('page', 1)
    paginator = Paginator(products_list, const_page_number)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/products_by_brand.html", {"slug": slug, "products": products})


def category_list(req):
    categories = Category.objects.all().order_by("created_at")
    page = req.GET.get('page', 1)
    paginator = Paginator(categories, const_page_number)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/categories.html", {"categories": categories})


def products_by_search(req):
    products_list = []
    if 'product' in req.GET:
        products_list = Product.objects.filter(
            title__icontains=str(req.GET["product"]))
    page = req.GET.get('page', 1)
    paginator = Paginator(products_list, const_page_number)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/search.html", {"products": products})


def products_by_category(req, slug):
    products = []
    products_list = []
    category = Category.objects.get(slug=slug)

    if category is None:
        return render(req, "error404.html")
    if 'max' not in req.GET or 'min' not in req.GET:
        if 'sub_category' in req.GET:
            sub_categ = SubCategory.objects.get(slug=req.GET["sub_category"])
            products_list = Product.objects.filter(
                category=category, sub_category=sub_categ).order_by("created_at")
        else:
            products_list = Product.objects.filter(
                category=category).order_by("created_at")

    else:
        if 'sub_category' in req.GET:
            sub_categ = SubCategory.objects.get(slug=req.GET["sub_category"])
            products_list = Product.objects.filter(
                category=category, price__range=[int(req.GET["min"]), int(req.GET["max"])], sub_category=sub_categ).order_by("created_at")
        else:
            products_list = Product.objects.filter(
                category=category, price__range=[int(req.GET["min"]), int(req.GET["max"])]).order_by("created_at")

    page = req.GET.get('page', 1)
    paginator = Paginator(products_list, const_page_number)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/products_by_category.html", {"slug": slug, "products": products, "category": category})


def products_by_sub_category(req, slug):
    products = []
    products_list = []
    sub_category = SubCategory.objects.get(slug=slug)

    if sub_category is None:
        return render(req, "error404.html")
    # if 'max' not in req.GET or 'max' not in req.GET:
    products_list = Product.objects.filter(
        sub_category=sub_category).order_by("created_at")
    # else:
    # products_list = Product.objects.filter(
    # category=category, price__range=[int(req.GET["min"]), int(req.GET["max"])]).order_by("created_at")

    page = req.GET.get('page', 1)
    paginator = Paginator(products_list, const_page_number)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/products_by_sub_category.html", {"slug": slug, "products": products, "sub_category": sub_category})


def products(req):
    products = Product.objects.all()
    return render(req, "ecomapp/products_list.html", {"products": products})


def lastest_products(req):
    products = []
    products_list = []

    # if 'max' not in req.GET or 'max' not in req.GET:
    products_list = Product.objects.all().order_by("-created_at")
    # else:
    # products_list = Product.objects.filter(
    # category=category, price__range=[int(req.GET["min"]), int(req.GET["max"])]).order_by("created_at")

    page = req.GET.get('page', 1)
    paginator = Paginator(products_list, const_page_number)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(req, "ecomapp/latest_products.html", {"products": products})


def product_by_slug(req, slug):
    colors = []
    sizes = []
    reviews = []
    wishlist = False
    product = Product.objects.get(slug=slug)
    if product == None:
        return render(req, "error404.html")

    colors = product.color.all()
    sizes = product.size.all()
    if req.user.is_authenticated:
        wishlist_exist = Wishlist.objects.filter(
            product=product, customer=req.user)
        if (len(wishlist_exist) != 0):
            wishlist = True

    if req.method == "POST":
        review = req.POST["review_text"]
        rating = req.POST["rating_value"]
        if review is not None:
            if len(review) != 0:
                Reviews.objects.create(
                    user=req.user, product=product, rate=int(rating), review=review)

        return redirect("ecomapp:product_detail", slug=product.slug)

    reviews = Reviews.objects.filter(product=product)
    avg_rate = Reviews.objects.filter(
        product=product).aggregate(avg=Avg("rate"))["avg"]

    return render(req, "ecomapp/product_detail.html", {"product": product, "wishlist": wishlist,
                                                       "colors": colors, "sizes": sizes, "reviews": reviews, "average_rating": avg_rate})


@ login_required(login_url="login")
def wishlist_num(req):
    wishlist = Wishlist.objects.filter(customer=req.user)
    obj = {'number': len(wishlist)}
    return JsonResponse(obj)


@ login_required(login_url="login")
def addto_wishlist(req, pk):
    product = Product.objects.filter(id=pk)
    if len(product) != 0:
        wishlist_exist = Wishlist.objects.filter(
            product=product[0], customer=req.user)
        if len(wishlist_exist) == 0:
            Wishlist.objects.create(product=product[0], customer=req.user)
            return JsonResponse({"added_removed": 1})
        else:
            wishlist_exist.delete()
            return JsonResponse({"added_removed": 0})
    else:
        return JsonResponse(status=500, data={"error": "Product doesn't exist."})


@ login_required(login_url="login")
def checkout(req):
    return render(req, "ecomapp/checkout.html")


@ login_required(login_url="login")
def myorders(req):
    orders = Order.objects.filter(customer=req.user)
    page = req.GET.get('page', 1)

    paginator = Paginator(orders, const_page_number)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/orders.html", {"orders": orders})


@ login_required(login_url="login")
def order_details(req, order_id):
    order = Order.objects.get(order_id=order_id)

    return render(req, "ecomapp/order_details.html", {"order": order})


@ login_required(login_url="login")
def wishlist(req):
    if req.method == 'POST':
        if "delete_or_add_to_cart" in req.POST and "wishlist_id" in req.POST:
            if req.POST["delete_or_add_to_cart"] == "delete":
                wishlist = Wishlist.objects.get(id=req.POST["wishlist_id"])
                wishlist.delete()
        return redirect(reverse("ecomapp:wishlist"))
    wlists = Wishlist.objects.filter(customer=req.user)
    page = req.GET.get('page', 1)
    paginator = Paginator(wlists, const_page_number)

    try:
        wlists = paginator.page(page)
    except PageNotAnInteger:
        wlists = paginator.page(1)
    except EmptyPage:
        wlists = paginator.page(paginator.num_pages)

    return render(req, "ecomapp/wishlist.html", {"wlists": wlists})


def cart(req):
    return render(req, "ecomapp/shopping_cart.html")


@ login_required(login_url="login")
def successpage(req):
    state_name = req.GET.get('order_id', None)
    print(state_name)
    return render(req, "ecomapp/successpage.html")


@login_required(login_url="login")
def billing(req):
    locations = Location.objects.all()
    if req.method == "POST":
        first_name = req.POST["first_name"]
        last_name = req.POST["last_name"]
        email = req.POST["email"]
        phonenumber = req.POST["phonenumber"]
        location_input = req.POST["location_input"]
        zipcode = req.POST["zipcode"]
        total_cart_items = req.POST["total_cart_items"]
        coupon = req.POST["coupon"]

        # checkfor validation left
        if total_cart_items != 0:
            location = Location.objects.get(id=int(location_input))
            if location is None:
                return redirect("ecomapp:billing")
            order_items_total_price = 0
            order = Order.objects.create(
                first_name=first_name, customer=req.user,
                last_name=last_name, email=email,
                phone_number=phonenumber, location=location, zipcode=zipcode)

            for i in range(int(total_cart_items)):
                product_id = req.POST[f'product_id_{i+1}']
                quantity = int(req.POST[f'quantity_id_{i+1}'])
                product = Product.objects.get(id=product_id)
                OrderItems.objects.create(
                    order=order, customer=req.user, product=product, quantity=quantity, price=product.get_final_price_after_discount()*quantity)
                order_items_total_price += product.get_final_price_after_discount()*quantity

            order.order_itmes_price = order_items_total_price
            coup = Coupon.objects.filter(coupon_code=coupon)
            order.delivery_price_addition = location.price

            if len(coup) != 0:
                order.coupon_price_deduction = coup.discount
                order.final_price = order_items_total_price+location.price-coup.discount
            else:
                order.coupon_price_deduction = 0
                order.final_price = order_items_total_price+location.price

            order.save()

        else:
            print("empty cart")

            return redirect("ecomapp:billing")

    return render(req, "ecomapp/billing.html", {"locations": locations})


# @ login_required(login_url="login")
@csrf_exempt
def billing_api(req):
    # locations = Location.objects.all()
    if req.method == "POST" and req.user.is_authenticated:
        body = json.loads(req.body.decode("utf-8"))
        first_name = body["first_name"]
        last_name = body["last_name"]
        email = body["email"]
        phonenumber = body["phonenumber"]
        location_input = body["location_input"]
        zipcode = body["zipcode"]
        total_cart_items = body["total_cart_items"]
        coupon = body["coupon"]

        # checkfor validation left
        if total_cart_items != 0:
            location = Location.objects.get(id=int(location_input))
            print(location)
            if location is not None:
                # return JsonResponse({"error": "Such location doesnot exist."}, status=404, safe=False)
                order_items_total_price = 0
                order = Order.objects.create(
                    first_name=first_name, customer=req.user,
                    last_name=last_name, email=email,
                    phone_number=phonenumber, location=location, zipcode=zipcode)

                for i in range(int(total_cart_items)):
                    product_id = int(body["cart_items"][i]["product_id"])
                    quantity = int(body["cart_items"][i]["quantity"])
                    product = Product.objects.get(id=product_id)
                    OrderItems.objects.create(
                        order=order, customer=req.user, product=product, quantity=quantity, price=product.get_final_price_after_discount()*quantity)

                    order_items_total_price += product.get_final_price_after_discount()*quantity

                order.order_itmes_price = order_items_total_price
                coup = Coupon.objects.filter(coupon_code=coupon)
                order.delivery_price_addition = location.price

                if len(coup) != 0:
                    order.coupon = coup[0]
                    order.coupon_price_deduction = coup[0].discount
                    order.final_price = (order_items_total_price +
                                         location.price-((coup[0].discount/100)*order_items_total_price))
                else:
                    order.coupon_price_deduction = 0
                    order.final_price = order_items_total_price+location.price

                order.save()
                print(order)

                return JsonResponse({"success": "Successfully placed order."}, status=200, safe=False)
            else:
                return JsonResponse({"error": "Something Went Wrong."}, status=505, safe=False)

    else:
        return JsonResponse({"error": "Something Went Wrong."}, status=505, safe=False)


@csrf_exempt
def apply_coupon_code(req):
    if req.method == "POST" and req.user.is_authenticated:
        body = json.loads(req.body.decode("utf-8"))
        coupon = body["coupon"]
        cup = Coupon.objects.filter(coupon_code=coupon, valid=True)

        if len(cup) == 0:
            return JsonResponse({"error": "coupon not found."}, status=404, safe=False)
        data = serializers.serialize(
            "json", cup, fields=("coupon_code", "discount"))
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"error": "Something went wrong."}, status=504, safe=False)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@ login_required(login_url="login")
def orders_pdf(req, order_id):
    if req.user.is_superuser:
        template_path = 'ecomapp/orderpdf.html'

    # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
        template = get_template(template_path)
        order = Order.objects.get(order_id=order_id)
        context = {"order": order}
        html = template.render(context)

    # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
    # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    pdf = render_to_pdf('ecomapp/orderpdf.html', order)
    return HttpResponse(pdf, content_type='application/pdf')

    return reverse("ecomapp:home")


def logout_user(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect(reverse("ecomapp:home"))


def forgot_password_send_mail(req):

    if req.user.is_authenticated:
        return redirect(reverse("ecomapp:home"))

    if req.method == "POST":
        email = req.POST["email"]
        user = User.objects.get(email=email)
        if user is not None:
            random_number = str(random.randint(1000000000, 9999999999))
            user.verification_code = random_number
            user.verification_code_created_at = datetime.now()
            user.save()
            send_mail('That’s your subject',
                      f'Your password reset token is {random_number}',
                      'rozaibusiness@gmail.com',
                      recipient_list=[user.email],
                      auth_user='rozaibusiness',
                      auth_password='cxvfipykhkouodja',
                      fail_silently=False)

    return render(req, "ecomapp/forgot_password_mail_send.html")


def forgot_password(req):
    if req.user.is_authenticated:
        return redirect(reverse("ecomapp:home"))

    if req.method == "POST":
        # email = req.POST["email"]
        reset_token = req.POST["reset-token"]
        password = req.POST["password"]
        confirm_password = req.POST["confirm_password"]
        if password != confirm_password:
            messages.error(req, 'The two passwords donot match.')
        else:
            five_minutes_ago = datetime.now() + timedelta(minutes=-5)
            user = User.objects.filter(
                verification_code=reset_token, verification_code_created_at__gte=five_minutes_ago)
            if len(user) > 0:
                user = user[0]
                user.set_password(password)
                messages.error(req, 'Successfully reseted password.')

    return render(req, "ecomapp/forgot_password.html")


@ login_required(login_url="login")
def reset_password(req):
    if req.method == "POST":
        # email = req.POST["email"]
        old_password = req.POST["old-password"]
        password = req.POST["password"]
        confirm_password = req.POST["confirm_password"]
        if password != confirm_password:
            messages.error(req, 'The two passwords donot match.')

        else:
            user = User.objects.get(id=req.user.id)
            if user is not None:
                valid = user.check_password(old_password)
                if valid is True:
                    user.set_password(password)
                    user.save()
                    return redirect(reverse("ecomapp:home"))
                else:
                    messages.error(
                        req, 'Please enter the correct old password.')

    return render(req, "ecomapp/reset_password.html")
