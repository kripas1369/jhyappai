from email.policy import default
from enum import unique
from pyexpat import model
from this import d
from unicodedata import category
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ecomapp.managers import UserManager
from tinymce.models import HTMLField
from django.db.models import Avg, Sum
from django.utils.html import format_html
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.template.defaultfilters import slugify

# OVERRIDING BASE USER MODEL


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    verification_code = models.CharField(
        max_length=30, blank=True, null=True, default="")
    verification_code_created_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        return
        # send_mail(subject, message, from_email, [self.email], **kwargs)return
        # send_mail(subject, message, from_email, [self.email], **kwargs)


# BRAND OF PRODUCT MODEL
class Brand(models.Model):
    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)

    thumbnail = models.ImageField(
        upload_to="brand_upload_images/", blank=True, null=True)
    image = models.CharField(
        max_length=10000, blank=False, null=False, default="", editable=False)

    slug = models.SlugField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def full_image_url(self):
        return f'{settings.MEDIA_URL}{self.thumbnail}'

    def show_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image}" alt="Img3"/>')

    def upload_brand_image(self):
        return format_html("<input required name='brand_image' type='file'/>")

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ecomapp:brand_detail', kwargs={'slug': self.slug})

 # CATEGORY OF PRODUCT MODEL


class Category(models.Model):

    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    thumbnail = models.ImageField(upload_to="category_upload_images/")
    image = models.CharField(
        max_length=10000, blank=False, null=False, default="", editable=False)

    in_home = models.BooleanField(default=False, null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def full_image_url(self):
        return f'{settings.MEDIA_URL}{self.thumbnail}'

    def show_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image}" alt="Img3"/>')

    def upload_category_image(self):
        return format_html("<input required name='category_image' type='file'/>")

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ecomapp:category_detail', kwargs={'slug': self.slug})

    def get_all_sub_categories(self):
        return SubCategory.objects.filter(category=self)

    def has_any_sub_categ(self):
        if len(self.get_all_sub_categories()) == 0:
            return False
        return True


class Colors(models.Model):
    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    color_code_hex = models.CharField(
        max_length=7, blank=False, null=False, default="#004002")

    def __str__(self):
        return self.title


class Coupon(models.Model):
    coupon_code = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    valid = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.coupon_code


class Size(models.Model):
    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)

    def __str__(self):
        return self.title


class Location(models.Model):
    title = models.CharField(
        max_length=250, unique=True, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to="subcategory_upload_images/", null=True, blank=True)

    image = models.CharField(
        max_length=10000, blank=False, null=False, default="", editable=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def full_image_url(self):
        return f'{settings.MEDIA_URL}{self.thumbnail}'

    def show_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image}" alt="Img3"/>')

    def upload_sub_category_image(self):
        return format_html("<input required name='sub_category_image' type='file'/>")

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    img = models.ImageField(upload_to="kam_nalagney/", blank=True, null=True)
    description = HTMLField(default="")
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    color = models.ManyToManyField(Colors, blank=True)
    size = models.ManyToManyField(Size, blank=True)
    delivery_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    image1 = models.CharField(
        max_length=10000, blank=False, null=False, default="", editable=False)

    image2 = models.CharField(max_length=10000)
    image3 = models.CharField(max_length=10000)
    image4 = models.CharField(max_length=10000)
    image5 = models.CharField(max_length=10000)
    in_stock = models.BooleanField(default=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs): # new
    #     self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)

    def get_discount_price(self):
        return (self.discount/100)*self.price

    def get_final_price_after_discount(self):
        return self.price-self.get_discount_price()

    def upload_first_image(self):
        return format_html("<input required name='image_1' type='file'/>")

    def first_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image1}" alt="Img1"/>')

    def upload_second_image(self):
        return format_html("<input required name='image_2' type='file'/>")

    def second_image(self):
        return format_html(f'<img width="300" height="300px" src="{self.image2}" alt="Img2"/>')

    def upload_third_image(self):
        return format_html("<input name='image_3' type='file'/>")

    def third_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image3}" alt="Img3"/>')

    def upload_fourth_image(self):
        return format_html("<input name='image_4' type='file'/>")

    def fourth_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image4}" alt="Img4"/>')

    def upload_fifth_image(self):
        return format_html("<input name='image_5' type='file'/>")

    def fifth_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image5}" alt="Img5"/>')

    def get_absolute_url(self):
        return reverse('ecomapp:product_detail', kwargs={'slug': self.slug})

    def avg_rating(self):
        ratings = Reviews.objects.filter(product=self).aggregate(Avg('rate'))
        if ratings["rate__avg"] == None:
            return 0.0
        return ratings["rate__avg"]

    def put_url_in_img(self, i):
        return


class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.email


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(choices=RATING_CHOICES, default=5)
    review = models.CharField(
        max_length=550, blank=False, null=False, default="")

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        if self.user.first_name == "" or self.user.last_name == "":
            return f'{self.user.email} rates {self.product.title} a {self.rate}.'
        else:
            return f'{self.user.first_name} {self.user.last_name} rates {self.product.title} a {self.rate}.'

    def average_rating(self, id):
        prod = Product.objects.filter(id=id)
        avg_rate = Reviews.objects.filter(
            product=prod).aggregate(avg=Avg("rate"))

        return 10


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
)


class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    invoice_number = models.CharField(
        max_length=250, blank=True, null=True, default="")
    location = models.ForeignKey(
        Location, blank=False, null=False, on_delete=models.CASCADE)
    # address1 = models.CharField(max_length=500, blank=False, null=False)
    # address2 = models.CharField(max_length=500, blank=False, null=False)
    coupon = models.ForeignKey(
        Coupon, blank=True, null=True, on_delete=models.SET_NULL)

    order_itmes_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)

    coupon_price_deduction = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)

    delivery_price_addition = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)

    final_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)

    zipcode = models.CharField(max_length=5, validators=[
                               MinLengthValidator(5)], blank=False, null=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, blank=False, null=False, default="Pending")
    phone_number = models.CharField(max_length=10, validators=[
                                    MinLengthValidator(10)], default="0000000000")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

    def order_status(self):
        if self.status == "Pending":
            return format_html('<img width="30" height="30" src="/static/admin/img/icon-no.svg" alt="True">')

        return format_html('<img width="30" height="30"  src="/static/admin/img/icon-yes.svg" alt="True">')

    def total_order_items(self):
        orders = OrderItems.objects.filter(order=self)
        return len(orders)

    def total_items_quantities(self):
        orders = OrderItems.objects.filter(
            order=self).aggregate(Sum('quantity'))
        return orders["quantity__sum"]

    def price_after_coupon(self):
        return self.order_itmes_price-((self.coupon.discount/100)*self.order_itmes_price)

    def total_price_of_order(self):
        orders = OrderItems.objects.filter(order=self).aggregate(Sum('price'))
        return orders["price__sum"]

    def get_first_order_item(self):
        return OrderItems.objects.filter(order=self)[0]

    def all_order_items(self):
        return OrderItems.objects.filter(order=self)

    def final_price_after_coupon(self):
        if self.coupon == None:
            return self.total_price_of_order()
        return self.total_price_of_order()-(self.coupon.discount*100)

    def order_pdf(self):
        return format_html(f'<a href="/order-pdf/{self.order_id}" target="_blank"><input type="button" value="View Pdf"  name="_save"></a>')
        # return format_html('<a href="/order-pdf" class="default"><input style="color:red" value="View Pdf"/></a>')


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=False, null=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    def __str__(self):
        return f'{self.customer_name()} ordered {self.quantity} {self.product.title}'

    def customer_name(self):
        if self.customer.first_name == "" or self.customer.last_name == "" or self.customer.first_name == None or self.customer.last_name == None:
            return self.customer.email
        return f'{self.customer.first_name} {self.customer.last_name}'

    def tt_p(self):
        return self.quantity*self.product.get_final_price_after_discount()

    def each_price(self):
        return self.product.get_final_price_after_discount()


class Banner(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    thumbnail = models.ImageField(
        upload_to="kaam_nalagney/", null=True, blank=True)
    image = models.CharField(
        max_length=10000, blank=False, null=False, default="", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def upload_image(self):
        return format_html("<input required name='image_1' type='file'/>")

    def banner_image(self):
        return format_html(f'<img width="300" height="300" src="{self.image}" alt="Img1"/>')