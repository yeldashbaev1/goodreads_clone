from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "ikrambek",
                "first_name": "Ikrambek",
                "last_name": "Eldashbaev",
                "email": "yeldashbaev@gmail.com",
                "password": "ikram1124"
            }
        )

        user = CustomUser.objects.get(username="ikrambek")

        self.assertEqual(user.first_name, "Ikrambek")
        self.assertEqual(user.last_name, "Eldashbaev")
        self.assertEqual(user.email, "yeldashbaev@gmail.com")
        self.assertNotEqual(user.password, "ikram1124")
        self.assertTrue(user.check_password("ikram1124"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Ikrambek",
                "email": "yeldashbaev@gmail.com",
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "ikrambek",
                "first_name": "Ikrambek",
                "last_name": "Eldashbaev",
                "email": "invaild-email",
                "password": "ikram1124"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username='ikrambek', first_name='Ikrambek')
        user.set_password('some11')
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "ikrambek",
                "first_name": "Ikrambek",
                "last_name": "Eldashbaev",
                "email": "yeldashbaev@gmail.com",
                "password": "ikram1124"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="ikram", first_name="Ikrambek")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successfully_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "ikram",
                "password": "somepass"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentail(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "ikram",
                "password": "wrong-pass"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="ikram", password="somepass")

        self.client.get(reverse("users:logout"))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="ikram",
            first_name="Ikrambek",
            last_name="Eldashbaev",
            email="yeldashbaev@gmail.com"
        )

        user.set_password('somepass')
        user.save()

        self.client.login(username='ikram', password='somepass')

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='ikram', first_name='Ikrambek', last_name="Eldashbaev", email='yeldashbaev@gmail.com'
        )

        user.set_password('somepass')
        user.save()

        self.client.login(username='ikram', password='somepass')

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "ikram",
                "first_name": "Ikrambek",
                "last_name": "bak",
                "email": "yeldashbaev1@gamil.com"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "bak")
        self.assertEqual(user.email, 'yeldashbaev1@gamil.com')
        self.assertEqual(response.url, reverse("users:profile"))
