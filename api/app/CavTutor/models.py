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

    def _prune_invalid_fields(fields):
        valid_fields = []

        for field in fields:
            try:
                valid_fields.append(this._meta.get_field(field))
            except FieldDoesNotExist:
                pass

        return valid_fields

    """
    # fields is a list of strings
    def update(self, fields):
        # real_fields is a list of valid field instances
        real_fields = _prune_invalid_fields(fields)

        for field in fields:
            # return the field instance for each field in fields
            field_inst = this._meta.get_field(field)
    """

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

    def get_num_courses(self):
        return self.course_set.count()

    def __str__(self):
        return "{} ({} courses)".format(self.name, self.get_num_courses())



