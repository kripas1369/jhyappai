from pkgutil import extend_path
from django.contrib import admin
from django import forms
from django.contrib.admin.helpers import ActionForm
from ecomapp.firebaseurlgenerator import firebaseurlgenerator
from .models import Banner, Brand, Category, Colors, Coupon, Location, Order, OrderItems, Product, Reviews, Size, SubCategory, User, Wishlist
from django.template.defaultfilters import slugify

from ecom.settings import storage

admin.site.site_title = "Admin Panel"
admin.site.site_header = "Rozai"

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', ]
    readonly_fields = ['password', 'profile_id']


admin.site.register(User, UserAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', ]
    readonly_fields = ['upload_brand_image', 'show_image',
                       'created_at', 'updated_at', 'slug']

    def save_model(self, request, obj, form, change):
        if len(request.FILES) != 0:
            file = request.FILES.get(f'brand_image')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image = firebaseurlgenerator(nm)
                obj.thumbnail = None

        return super().save_model(request, obj, form, change)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Colors)
admin.site.register(Size)
admin.site.register(Location)


class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', ]
    # readonly_fields = ['', 'discount']


admin.site.register(Coupon, CouponAdmin)


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['title', ]
    readonly_fields = ["upload_category_image",
                       'show_image', "id", 'created_at', 'updated_at', 'slug']

    def save_model(self, request, obj, form, change):
        if len(request.FILES) != 0:
            file = request.FILES.get(f'category_image')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image = firebaseurlgenerator(nm)
                obj.thumbnail = None

        return super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):

    list_display = ['title', ]
    readonly_fields = ["upload_sub_category_image",
                       'show_image', "id", 'created_at', 'updated_at', 'slug']

    def save_model(self, request, obj, form, change):
        if len(request.FILES) != 0:
            file = request.FILES.get(f'sub_category_image')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image = firebaseurlgenerator(nm)
                obj.thumbnail = None

        return super().save_model(request, obj, form, change)


admin.site.register(SubCategory, SubCategoryAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    exclude = ('image1', 'image2', 'image3', 'image4', 'image5')
    readonly_fields = ('upload_first_image', 'first_image',
                       'upload_second_image', 'second_image',
                       'upload_third_image', 'third_image',
                       'upload_fourth_image', 'fourth_image',
                       'upload_fifth_image', 'fifth_image',
                       'created_at', 'updated_at', 'slug',)

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        if len(request.FILES) != 0:
            # first image
            file = request.FILES.get(f'image_1')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image1 = firebaseurlgenerator(nm)

            # second image
            file = request.FILES.get(f'image_2')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image2 = firebaseurlgenerator(nm)

             # third image
            file = request.FILES.get(f'image_3')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image3 = firebaseurlgenerator(nm)

            # fourth image
            file = request.FILES.get(f'image_4')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image4 = firebaseurlgenerator(nm)

             # fifth image
            file = request.FILES.get(f'image_5')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image5 = firebaseurlgenerator(nm)

        return super().save_model(request, obj, form, change)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rate",)
    readonly_fields = ("created_at",)


class OrderItemsInLine(admin.StackedInline):
    model = OrderItems
    extra = 0
    # can_delete=False
    readonly_fields = ("product", "customer",
                       "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order_status", "created_at",
                    'total_order_items', "order_pdf")
    inlines = [OrderItemsInLine, ]
    readonly_fields = ("customer", "total_items_quantities",
                       "coupon", "order_itmes_price", "coupon_price_deduction", "delivery_price_addition", "final_price", "order_pdf")

    def save_model(self, request, obj, form, change):
        if change == True:
            loc = Location.objects.filter(title=obj.location)
            if len(loc) != 0:
                obj.location = loc[0]
                obj.delivery_price_addition = loc[0].price
                obj.final_price = obj.order_itmes_price + \
                    loc[0].price-obj.coupon_price_deduction

        return super().save_model(request, obj, form, change)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['Sched_today'] = "Shuttt up"
        print(extra_context)
        return super(OrderAdmin, self).add_view(request, form_url, extra_context)


@ admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    readonly_fields = ("customer", "product", "each_price", "price")

    def save_model(self, request, obj, form, change):
        obj.price = obj.product.get_final_price_after_discount()*obj.quantity
        super().save_model(request, obj, form, change)


admin.site.register(Wishlist)


class BannerAdmin(admin.ModelAdmin):

    list_display = ['title', ]
    readonly_fields = ["upload_image", "banner_image"]

    def save_model(self, request, obj, form, change):
        if len(request.FILES) != 0:
            file = request.FILES.get(f'image_1')
            if file != None:
                nm = file.name.strip()
                s = storage.child(nm).put(file)
                obj.image = firebaseurlgenerator(nm)
                obj.thumbnail = None

        return super().save_model(request, obj, form, change)


admin.site.register(Banner, BannerAdmin)
