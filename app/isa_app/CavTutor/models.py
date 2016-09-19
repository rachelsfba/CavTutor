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

    def to_dict(self):
        user_dict = {
            'f_name': self.f_name,
            'l_name': self.l_name,
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'date_joined': self.date_joined
        }

        return user_dict

    def __str__(self):
        return self.l_name + ", " + self.f_name

class Course(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=16, verbose_name="class abbreviation")
    instructor = models.CharField(max_length=256)
    def __str__(self):
        return self.name + " (" + self.abbr + ")"

class Tutor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    adv_rate = models.DecimalField(max_digits=16, decimal_places=2, verbose_name="advertised hourly rate",)

    def __str__(self):
        return self.user.l_name + ", " + self.user.f_name + " (" + self.course.abbr + ")"

class Tutee(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    tutor = models.ForeignKey('Tutor', on_delete=models.CASCADE)
    # Deciding that this field would probably be better used in a search engine.
    #max_rate = models.DecimalField(max_digits=16, decimal_places=2,
    #        verbose_name="maximum hourly rate willing to pay")

    def __str__(self):
        return self.user.l_name + ", " + self.user.f_name + " (" + self.course.abbr + ")"

class Institution(models.Model):
    name = models.CharField(max_length=100)
    abbrv = models.CharField(max_length=16)
    # in future, subdivide this into many different fields, e.g. street_addr, state_province, country
    address = models.CharField(max_length=256)

    def __str__(self):
        return self.name
