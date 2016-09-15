from django.db import models

# Create your models here.
class User:
    id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=32)
    password = # ??????
    date_
class Course:
    # implement TODO

class Tutor:
    # implement TODO

class Tutee:
    # implement TODO

class Institution:
    # implement TODO

class Review:
    #implement
