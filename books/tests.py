from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="124124124")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="124124125")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="124124126")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description='Description1', isbn="17245124")

        respopnse = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(respopnse, book.title)
        self.assertContains(respopnse, book.description)

        # book authorga test jaziw kerek

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="124124124")
        book2 = Book.objects.create(title="Dug", description="Description2", isbn="124124125")
        book3 = Book.objects.create(title="Shoe", description="Description3", isbn="124124126")

        response = self.client.get(reverse("books:list") + "?q=Sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Dug")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Shoe")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='12471289')
        user = CustomUser.objects.create(
            username='ikram',
            first_name='Ikrambek',
            last_name='Eldashbaev',
            email='yeldashbaev@gmail.com'
        )
        user.set_password('somepass')
        user.save()
        self.client.login(username='ikram', password='somepass')

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            'stars_given': 3,
            'comment': 'Nice Book'
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice Book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)




