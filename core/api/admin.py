from django.contrib import admin

from .models import *

admin.site.register(Event)
admin.site.register(EventVoucher)
admin.site.register(Voucher)
admin.site.register(User)
admin.site.register(Wallet)

