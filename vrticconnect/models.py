from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Vrtic(models.Model):
    Naziv = models.CharField(max_length=100)
    Adresa = models.TextField(max_length=500)

    def __str__(self):
        return self.Naziv

class Grupa(models.Model):
    Naziv = models.CharField(max_length=100)
    Vrtic = models.ForeignKey(Vrtic, on_delete=models.CASCADE)

    def __str__(self):
        return self.Naziv

class User(AbstractUser):
    Grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE, null=True)
    Zaposlen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Objava(models.Model):
    Naslov = models.CharField(max_length=200)
    Tekst = models.TextField(max_length=1000)
    Datum_objave = models.DateTimeField("date published")
    Autor = models.ForeignKey(User, on_delete=models.CASCADE)
    Grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return self.Naslov
    
class Poruka(models.Model):
    Tekst_poruka = models.TextField(max_length=1000)
    Datum_objave = models.DateTimeField("date published")
    Autor = models.ForeignKey(User, on_delete=models.CASCADE)
    Grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return (self.Tekst + " - " +
                str(self.Autor.username) + " - " +
                str(self.Tekst_poruka))

class Aktivnost(models.Model):
    Naziv = models.CharField(max_length=200)
    Datum_aktivnosti = models.DateField()
    Grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return self.Naziv
    
class Fotografija(models.Model):
    Naslov = models.CharField(max_length=100)
    Fotografija = models.ImageField(upload_to='fotografije/')
    Datum_spremanja = models.DateTimeField(auto_now_add=True)
    Grupa = models.ForeignKey(Grupa, on_delete=models.CASCADE,  null=True)

    def __str__(self):
        return self.Naslov