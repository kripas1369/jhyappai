from ecomapp.views import (addto_wishlist, apply_coupon_code, billing_api, brand_list, cart, category_list, contactus, forgot_password, forgot_password_send_mail, home, aboutus,
                           checkout, lastest_products, myorders, order_details, orders_pdf, product_by_slug, products, products_by_brand, products_by_category, products_by_search, products_by_sub_category, reset_password, successpage, wishlist, wishlist_num, billing)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


app_name = "ecomapp"

urlpatterns = [
    path("", home, name="home"),
    path("billing/", billing, name="Billing"),
    # path("aboutus/", aboutus, name="about"),
    path("contact-us/", contactus, name="contact"),
    path("checkout/", checkout, name="checkout"),
    path("cart/", cart, name="cart"),
    path("success-page/", successpage, name="successpage"),
    path("billing/", billing, name="billing"),
    path("billing_api/", billing_api, name="billing_api"),
    path("apply-coupon-code/", apply_coupon_code, name="apply-coupon-code"),
    path("search/", products_by_search, name="search"),
    path("my-orders/", myorders, name="myorders"),
    path("order-pdf/<str:order_id>", orders_pdf, name="orderpdf"),
    path("order-details/<str:order_id>", order_details, name="order_details"),
    path("wishlist/", wishlist, name="wishlist"),
    path("latest-products/", lastest_products, name="lastest_products"),
    path("wishlist_num/", wishlist_num, name="wishlist_num"),
    path("add_to_wishlist/<int:pk>", addto_wishlist, name="addto_wishlist"),
    path("brands/", brand_list, name="brand_list"),
    path("brand/<slug:slug>", products_by_brand, name="brand_detail"),
    path("categories/", category_list, name="category_list"),
    path("category/<slug:slug>", products_by_category, name="category_detail"),
    path("sub_category/<slug:slug>", products_by_sub_category,
         name="sub_category_detail"),
    path("products/", products, name="products_list"),
    path("send-mail/", forgot_password_send_mail,
         name="forgot-password-mail-send"),
    path("forgot-password-reset/", forgot_password,
         name="forgot-password"),
    path("reset-password/", reset_password,
         name="reset-password"),

    path("product/<slug:slug>", product_by_slug, name="product_detail"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
