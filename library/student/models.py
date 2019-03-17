from django.db import models


branch = [('CSE', 'Computer Science and Engineering'),
          ('Electrical', 'Electrical Engineering'),
          ('Mechanical', 'Mechanical Engineering'),
          ('Biotechnology', 'BioTechnology Engineering')]


class StudentProfile(models.Model):
    FirstName = models.CharField(max_length=15)
    MiddleName = models.CharField(blank=True, null=True, max_length=15)
    LastName = models.CharField(max_length=15)
    Branch = models.CharField(choices=branch, blank=True, null=True, default='CSE', max_length=25)
    RollNo = models.CharField(max_length=10, blank=True, null=True)
    Email = models.EmailField()
    Mobile = models.CharField(max_length=12)
    profilePicture = models.ImageField(upload_to='student/profile/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        ordering = ["FirstName"]

    def __str__(self):
        return '%s' % self.FirstName
