from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Tutor)
admin.site.register(Tutee)
admin.site.register(Course)
admin.site.register(Institution)

