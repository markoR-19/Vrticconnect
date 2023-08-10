from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import User, Grupa, Vrtic, Objava, Aktivnost, Fotografija

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username",]
# Register your models here.
model_list = [User, Grupa, Vrtic, Objava, Aktivnost, Fotografija ]
admin.site.register(model_list)