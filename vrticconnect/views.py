# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_http_methods
from datetime import date, timedelta

User = get_user_model()

@login_required
def SignUpView(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            dodan_korisnik = True
            form = CustomUserCreationForm(request.POST)
            context={'grupa':grupa, 'Zaposlen':Zaposlen, 'form': form, 'dodan_korisnik':dodan_korisnik}
            return render(request, "registration/signup.html", context)

    else:
        form = CustomUserCreationForm()
    context={'grupa':grupa, 'Zaposlen':Zaposlen, 'form': form}
    return render(request, "registration/signup.html", context)

@login_required
def portal(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    objave_lista = Objava.objects.filter(Grupa__Naziv__contains=grupa).order_by("-Datum_objave")
    paginator = Paginator(objave_lista, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    users = User.objects.filter( Grupa__Naziv__contains=grupa )
    start_date =  date.today() - timedelta(days=14)
    end_date = date.today() + timedelta(weeks=25)
    aktivnosti = Aktivnost.objects.filter(Grupa__Naziv__contains=grupa).filter(Datum_aktivnosti__range=(start_date, end_date)).order_by('Datum_aktivnosti')
    if request.method == 'POST':
        form = ObjavaForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.Autor = User.objects.get(username=request.user.username)
            obj.Grupa = grupa
            obj.Datum_objave = timezone.now()
            obj.save()
            return redirect("/")

    else:
        form = ObjavaForm()
    poruke = Poruka.objects.filter(Grupa__Naziv__contains=grupa).order_by('Datum_objave')
    context = {'Zaposlen':Zaposlen, "page_obj": page_obj,'poruke':poruke, 'grupa':grupa, 'users':users, 'aktivnosti':aktivnosti, 'form': form}
    return render(request, 'vrticconnect/portal.html', context)

def objave_list(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    objave_lista = Objava.objects.filter(Grupa__Naziv__contains=grupa).order_by("-Datum_objave")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    paginator = Paginator(objave_lista, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    users = User.objects.filter( Grupa__Naziv__contains=grupa )
    context = {'Zaposlen':Zaposlen, "page_obj": page_obj, 'grupa':grupa, 'users':users}
    return render(request, 'partials/objave.html', context)

@require_http_methods(['DELETE'])
def delete_user(request, id):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    User.objects.filter(id=id).delete()
    users = User.objects.filter( Grupa__Naziv__contains=grupa )
    context = {'grupa':grupa, 'users':users}
    return render(request, 'partials/user_list.html', context)

@require_http_methods(['DELETE'])
def delete_objava(request, id):
    Objava.objects.filter(id=id).delete()
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    objave_lista = Objava.objects.filter(Grupa__Naziv__contains=grupa).order_by("-Datum_objave")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    paginator = Paginator(objave_lista, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    users = User.objects.filter( Grupa__Naziv__contains=grupa )
    context = {'Zaposlen':Zaposlen, "page_obj": page_obj, 'grupa':grupa, 'users':users}
    return render(request, 'partials/objave.html', context)

def objava_edit(request, id):
    objava = Objava.objects.get(id=id)
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    if request.method == 'POST':
            form = ObjavaForm(request.POST, instance=objava)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.Autor = User.objects.get(username=request.user.username)
                obj.Grupa = grupa
                obj.Datum_objave = timezone.now()
                obj.save()
                return redirect("/")
    else:
        form = ObjavaForm(instance=objava)
    context={'grupa':grupa, 'form': form, 'Zaposlen':Zaposlen, 'id':id}
    return render(request, 'partials/dodaj_objavu.html', context)

@login_required
def dodaj_objavu(request):
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    grupa =  getattr(User.objects.get(username=request.user.username), "Grupa")
    if request.method == 'POST':
        form = ObjavaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/")

    else:
        form = ObjavaForm()
    context={'grupa':grupa, 'form': form, 'Zaposlen':Zaposlen}
    return render(request, 'partials/dodaj_objavu.html', context)

def chat(request):
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    grupa =  getattr(User.objects.get(username=request.user.username), "Grupa")
    poruke = []
    poruke = Poruka.objects.filter(Grupa__Naziv__contains=grupa).order_by('-Datum_objave')
    context = {'Zaposlen':Zaposlen,'grupa':grupa, 'poruke':poruke}
    return render(request, 'partials/chat.html', context)
        
@login_required
def korisnik_profil(request):
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(to='vrticconnect:portal')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    context = {'Zaposlen':Zaposlen,'grupa':grupa, 'user_form': user_form}
    return render(request, 'vrticconnect/korisnik_profil.html', context)

@login_required
def profil_edit(request, id):
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            users = User.objects.filter( Grupa__Naziv__contains=grupa )
            context = {'Zaposlen':Zaposlen, 'users': users, 'grupa': grupa}
            return render(request, 'partials/user_list.html',context)
    else:
        user_form = CustomUserChangeForm(instance=user)
    context = {'Zaposlen':Zaposlen,'grupa':grupa, 'user_form': user_form, 'id':id}
    return render(request, 'partials/profil_edit.html', context)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'vrticconnect/password_change_form.html'
    success_url = reverse_lazy('vrticconnect:korisnik_profil')

def dodaj_aktivnost(request):
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    grupa =  getattr(User.objects.get(username=request.user.username), "Grupa")
    if request.method == 'POST':
        form = AktivnostForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.Grupa = grupa
            obj.save()    
            start_date =  date.today() - timedelta(days=14)
            end_date = date.today() + timedelta(weeks=25)
            aktivnosti = Aktivnost.objects.filter(Grupa__Naziv__contains=grupa).filter(Datum_aktivnosti__range=(start_date, end_date)).order_by('Datum_aktivnosti')
            context={'grupa':grupa, 'aktivnosti': aktivnosti, 'Zaposlen':Zaposlen}
            return render(request, 'partials/aktivnost_list.html',context)

    else:
        form = AktivnostForm()
    context={'grupa':grupa, 'form': form, 'Zaposlen':Zaposlen}
    return render(request, 'partials/dodaj_aktivnost.html', context)

@require_http_methods(['DELETE'])
def aktivnost_delete(request, id):
    Aktivnost.objects.filter(id=id).delete()
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    start_date =  date.today() - timedelta(days=14)
    end_date = date.today() + timedelta(weeks=25)
    aktivnosti = Aktivnost.objects.filter(Grupa__Naziv__contains=grupa).filter(Datum_aktivnosti__range=(start_date, end_date)).order_by('Datum_aktivnosti')
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    context={'grupa':grupa, 'aktivnosti': aktivnosti, 'Zaposlen':Zaposlen}
    return render(request, 'partials/aktivnost_list.html',context)

def aktivnost_list(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    start_date =  date.today() - timedelta(days=14)
    end_date = date.today() + timedelta(weeks=25)
    aktivnosti = Aktivnost.objects.filter(Grupa__Naziv__contains=grupa).filter(Datum_aktivnosti__range=(start_date, end_date)).order_by('Datum_aktivnosti')
    context = {'Zaposlen':Zaposlen, 'grupa':grupa, 'aktivnosti':aktivnosti}
    return render(request, 'partials/aktivnost_list.html', context)

@login_required
def user_list(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    users = User.objects.filter( Grupa__Naziv__contains=grupa )
    context = {'Zaposlen':Zaposlen,'grupa':grupa, 'users':users}
    return render(request, 'partials/user_list.html', context)

def foto(request):
    grupa = getattr(User.objects.get(username=request.user.username), "Grupa")
    Zaposlen =  getattr(User.objects.get(username=request.user.username), "Zaposlen")
    fotografije = Fotografija.objects.filter(Grupa__Naziv__contains=grupa).order_by("-Datum_spremanja")
    paginator = Paginator(fotografije, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        grupa =  getattr(User.objects.get(username=request.user.username), "Grupa")
        if form.is_valid():
            obj = form.save(commit=False)
            obj.Datum_spremanja = timezone.now()
            obj.Grupa = grupa
            obj.save() 
            form.save()
            return redirect(to='vrticconnect:foto')
    else:
        form = FotoForm()
    context = {'Zaposlen':Zaposlen,'grupa':grupa, 'fotografije': page_obj, 'form':form}
    return render(request, 'vrticconnect/foto.html', context)
