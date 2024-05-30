from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()
REGISTER_USER_URL = reverse("user:register")
LOGIN_USER_URL = reverse("user:login")
LOGOUT_USER_URL = reverse("user:logout")
CHANGE_PASSWORD_URL = reverse("user:change_password")
RESET_PASSWORD_URL = reverse("user:password_reset")
PROFILE_USER_URL = reverse("user:profile")


def get_reset_password_confirm_url(uid: str, token: str) -> str:
    return reverse(
        "user:password_reset_confirm",
        kwargs={"uid": uid, "token": token}
    )


def create_user(**params):
    return User.objects.create_user(**params)


class PublicUserAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user_data = {
            "email": "user@user.com",
            "password": "1234test",
        }

    def test_register_valid_user_success(self):
        self.user_data["password_2"] = "1234test"
        res = self.client.post(REGISTER_USER_URL, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.user_data.get("email"))
        self.assertTrue(user.check_password(self.user_data.get("password")))
        self.assertNotIn("password", res.data)

    def test_register_invalid_user_credentials(self):
        invalid_data_cases = [
            {
                "email": "user@user.com",
                "password": "1234test",
                "password_2": "test1234",
            },
            {
                "email": "",
                "password": "1234test",
                "password_2": "1234test",
            },
            {
                "email": "user@user.com",
                "password": "",
                "password_2": "",
            },
            {
                "email": "user@user.com",
                "password": "123",
                "password_2": "123",
            },
            {
                "email": "bad-email",
                "password": "1234test",
                "password_2": "1234test",
            }
        ]

        for case in invalid_data_cases:
            with self.subTest(case=case):
                res = self.client.post(REGISTER_USER_URL, case)

                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_user(self):
        create_user(**self.user_data)
        self.user_data["password_2"] = "1234test"

        res = self.client.post(REGISTER_USER_URL, self.user_data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_user_success(self):
        create_user(**self.user_data)

        res = self.client.post(LOGIN_USER_URL, self.user_data)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_invalid_user_credentials(self):
        res = self.client.post(LOGIN_USER_URL, self.user_data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_valid_user(self):
        create_user(**self.user_data)
        data = {"email": self.user_data.get("email")}

        res = self.client.post(RESET_PASSWORD_URL, data)
        email = mail.outbox[0]

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, "Password Reset")
        self.assertIn("Use the link below to reset your password:", email.body)
        self.assertEqual(email.to, [self.user_data.get("email")])

    def test_password_reset_invalid_user(self):
        data = {"email": "wrong@gmail.com"}
        res = self.client.post(RESET_PASSWORD_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_reset_password_confirm_success(self):
        user = create_user(**self.user_data)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = get_reset_password_confirm_url(uid=uid, token=token)
        new_password = "newpass1234"
        data = {
            "new_password": new_password,
            "new_password_2": new_password,
        }

        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))


class PrivateUserApiTest(TestCase):

    def setUp(self) -> None:
        self.user = create_user(
            email="user@user.com",
            password="1234test",
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_logout_user_success(self):
        res = self.client.post(LOGOUT_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"message": "You successfully logged out"})

    def test_change_password_success(self):
        new_password = "test@1234"
        data = {
            "old_password": "1234test",
            "new_password": new_password,
            "new_password_2": new_password,
        }

        res = self.client.put(CHANGE_PASSWORD_URL, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_change_password_invalid_user_credentials(self):
        invalid_data_cases = [
            {
                "old_password": "wrongpassword1234",
                "new_password": "test@1234",
                "new_password_2": "test@1234",
            },
            {
                "old_password": "1234test",
                "new_password": "123a",
                "new_password_2": "123a",
            },
            {
                "old_password": "1234test",
                "new_password": "",
                "new_password_2": "",
            },
            {
                "old_password": "",
                "new_password": "test@1234",
                "new_password_2": "test@1234",
            },
        ]

        for case in invalid_data_cases:
            with self.subTest(case=case):
                res = self.client.put(CHANGE_PASSWORD_URL, case, format="json")

                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
                self.user.refresh_from_db()
                self.assertTrue(self.user.check_password("1234test"))

    def test_update_user_profile_success(self):
        data = {
            "username": "new_username",
            "email": "new_email@email.com",
        }
        res = self.client.patch(PROFILE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_username")
        self.assertEqual(self.user.email, "new_email@email.com")

    def test_update_user_profile_image_success(self):
        image = Image.new("RGB", (100, 100), "white")
        tmp_file = BytesIO()
        image.save(tmp_file, "png")
        tmp_file.seek(0)
        avatar = SimpleUploadedFile(
            "avatar.png",
            tmp_file.read(),
            content_type="image/png"
        )

        data = {"avatar": avatar}
        res = self.client.patch(PROFILE_USER_URL, data, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.avatar)
