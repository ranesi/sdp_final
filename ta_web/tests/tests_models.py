from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError as IE
from text_analysis.ta_web.models import Document


class TestUserObject(TestCase):
    def test_user_required_fields(self):
        user = User(username=None)
        with self.assertRaises(IE):
            user.save()

        user = User(username='a')
        with self.assertRaises(IE):
            user.save()

        user = User(password='zxcvzxcv')
        with self.assertRaises(IE):
            user.save()

    def unique_username_required(self):
        user_info = dict(
            username='asd',
            password='zxcvzxcv'
        )

        user1 = User(user_info)
        user1.save()

        user2 = User(user_info)
        with self.assertRaises(IE):
            user2.save()

    def username_case_insensitive(self):
        u1 = dict(
            username='asd',
            password='zxcvzxcv'
        )

        u2 = dict(
            username='ASD',
            password='zxcvzxcv'
        )

        user1 = User(u1)
        user1.save()

        user2 = User(u2)
        with self.assertRaises(IE):
            user2.save()
