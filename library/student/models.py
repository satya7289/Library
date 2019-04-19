import datetime
from django.db import models

from account.models import Student, User
from manager.models import Book


class Cart(models.Model):
    Book = models.ManyToManyField(Book)
    CheckIn = models.BooleanField(default=False)
    CheckOut = models.BooleanField(default=False)
    CheckInTime = models.DateField(blank=True, null=True)
    CheckOutTime = models.DateField(blank=True, null=True)
    User = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.UserId.user.username

