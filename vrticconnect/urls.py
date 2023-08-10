# accounts/urls.py
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = "vrticconnect"

urlpatterns = [
    path("signup/", SignUpView, name="signup"),
    path('', portal, name='portal'),
    path('vrticconnect/dodaj_objavu/', dodaj_objavu, name='dodaj_objavu'),
    path('vrticconnect/chat/', chat, name='chat'),
    path('vrticconnect/korisnik_profil/', korisnik_profil, name='korisnik_profil'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('vrticconnect/<int:id>/delete/', delete_user, name='delete_user'),
    path('vrticconnect/<int:id>/profil_edit/', profil_edit, name='profil_edit'),
    path('vrticconnect/objave_list/', objave_list, name='objave_list'),
    path('vrticconnect/objave_list/delete/<int:id>', delete_objava, name='delete_objava'),
    path('vrticconnect/objave_list/objava_edit/<int:id>', objava_edit, name='objava_edit'),
    path('vrticconnect/dodaj_aktivnost/', dodaj_aktivnost, name='dodaj_aktivnost'),
    path('vrticconnect/aktivnost_delete/<int:id>/', aktivnost_delete, name='aktivnost_delete'),
    path('vrticconnect/aktivnost_list/', aktivnost_list, name='aktivnost_list'),
    path('vrticconnect/user_list/', user_list, name='user_list'),
    path('vrticconnect/foto/', foto, name='foto'),
    path('vrticconnect/<int:id>/foto_delete/', foto_delete, name='foto_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)