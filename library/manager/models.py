import datetime
from django.db import models


year_choice = []
for r in range(1980, (datetime.datetime.now().year+1)):
    year_choice.append((r, r))

subject_choice = ('Computer', 'Math', 'Chemistry', 'Physics', 'Biology')


class Book(models.Model):
    book_no = models.PositiveIntegerField()
    subject = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    total = models.PositiveIntegerField()
    year = models.IntegerField(choices=year_choice, default=datetime.datetime.now().year)
    CoverPicture = models.ImageField(upload_to='manager/book/coverPic/%Y/%m/%d/', blank=True,  null=True)
    BookPDF = models.FileField(upload_to='manger/book/pdf/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        ordering = ["book_no"]

    def __str__(self):
        return '%d %s' % (self.book_no, self.subject)




