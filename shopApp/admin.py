from django.contrib import admin
from .models import User, Category, Product, History

# Register your models here.
# admin.site.register(User)
admin.site.register(Category)


# admin.site.register(Product)
# admin.site.register(History)


@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'email', 'is_staff')


@admin.register(Product)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'stock', 'sale')
    list_filter = ('category',)

    def saleview(self, obj):
        return obj.saleview > 75

    saleview.boolean = False


@admin.register(History)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'data')
