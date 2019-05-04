from django.test import TestCase
from .models import Book
# Create your tests here.


class BooksTestCase(TestCase):
    def setUp(self):
        self.b1 = Book.objects.create(book_no='100', subject='physics', title='COP', author='HCV', total='1')
        self.b2 = Book.objects.create(book_no='200', subject='bio', title='genetics', author='baba', total='2')

    def test_book_details(self):
        self.assertEqual(self.b1.book_no, "100")
        self.assertEqual(self.b2.book_no, "200")
        self.assertEqual(self.b1.subject, "physics")
        self.assertEqual(self.b2.subject, "bio")
        self.assertEqual(self.b1.title, "COP")
        self.assertEqual(self.b2.title, "genetics")
        self.assertEqual(self.b1.author, "HCV")
        self.assertEqual(self.b2.author, "baba")
        self.assertEqual(self.b1.total, "1")
        self.assertEqual(self.b2.total, "2")

    def test_book_details02(self):
        self.assertEqual(self.b1.book_no, "100")
        self.assertEqual(self.b2.book_no, "200")
        self.assertEqual(self.b1.subject, "physics")
        self.assertEqual(self.b2.subject, "bio")
        self.assertNotEqual(self.b1.title, "COPv")
        self.assertEqual(self.b2.title, "genetics")
        self.assertEqual(self.b1.author, "HCV")
        self.assertEqual(self.b2.author, "baba")
        self.assertEqual(self.b1.total, "1")
        self.assertEqual(self.b2.total, "2")