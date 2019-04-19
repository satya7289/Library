from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .models import *


class TestUrls(SimpleTestCase):
    def test_list_url(self, LoginView=None):
       url = reverse('login')
       self.assertEquals(resolve(url).func.view_class, LoginView)