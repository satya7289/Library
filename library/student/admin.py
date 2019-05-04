from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'CheckIn', 'CheckOut')
    list_filter = ('CheckIn', 'CheckOut')


admin.site.register(Cart, CartAdmin)
