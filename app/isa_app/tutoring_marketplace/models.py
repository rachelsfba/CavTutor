from django.db import models

# Create your models here.
class User(models.Model):
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=32)
    # should define password field more strictly in the future
    password = models.CharField(max_length=256)
    date_joined = models.DateTimeField(auto_now=True)

class Course(models.Model):
    inst_id = models.ForeignKey('Institution', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    abbrv = models.CharField(max_length=16)

class Tutor(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    adv_rate = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="advertised hourly rate",)

class Tutee(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    tutor_id = models.ForeignKey('Tutor', on_delete=models.CASCADE)
    # Deciding that this field would probably be better used in a search engine.
    #max_rate = models.DecimalField(max_digits=16, decimal_places=2,
    #        verbose_name="maximum hourly rate willing to pay")

class Institution(models.Model):
    name = models.CharField(max_length=100)
    abbrv = models.CharField(max_length=16)
    # in future, subdivide this into many different fields, e.g. street_addr, state_province, country
    address = models.CharField(max_length=256)

