import datetime
from django.db import models

# Create your models here.
year_choice =[]
for r in range(1980, (datetime.datetime.now().year+1)):
    year_choice.append((r,r))


class Book(models.Model):
    book_no = models.PositiveIntegerField()
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    total = models.PositiveIntegerField()
    year = models.IntegerField(choices=year_choice, default=datetime.datetime.now().year)

    class Meta:
        ordering = ["book_no"]

    def __self__(self):
        return self.book_no


class Manager_profile(models.Model):
    name = models.CharField(max_length=30)
    college_id = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=12)
    year = models.IntegerField(choices=year_choice, default=datetime.datetime.now().year)

    def __self__(self):
        return self.name









