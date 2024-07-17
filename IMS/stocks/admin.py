from django.contrib import admin
from stocks.models import *

admin.site.register(Products)
admin.site.register(Variant)
admin.site.register(SubVariant)