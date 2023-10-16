import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import User


class UsersAppTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.anonymous_client = APIClient()

        cls.user1 = User.objects.create_user("User 1", "user1@gmail.com", "12345678")
        cls.user2 = User.objects.create_user("User 2", "user2@gmail.com", "12345678")

        token = Token.objects.get(user=cls.user1)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        cls.client1 = client

    def test_register(self):
        def sub_test(data, is_correct):
            users_count = User.objects.all().count()
            response = self.anonymous_client.post(reverse('user-register'), data=data)
            users_count_change = User.objects.all().count() - users_count

            self.assertEqual(response.status_code, 200 if is_correct else 400)
            self.assertEqual(users_count_change, 1 if is_correct else 0)

        with open('users/tests_data/register_test.json') as test_file:
            test_cases = json.load(test_file)

        for case in test_cases:
            sub_test(case['data'], case['isCorrect'])

    def test_auth(self):
        User.objects.create_user("Bob", "bob@mail.ru", "12345678")

        self.assertEqual(self.anonymous_client.login(username="Bob", password="12345678"), True)
        self.assertEqual(self.anonymous_client.login(username="bob@mail.ru", password="12345678"), True)
        self.assertEqual(self.anonymous_client.login(username="Another Bob", password="12345678"), False)

    def test_user_detail(self):
        response = self.client1.get(reverse('user-detail', kwargs={'user_id': self.user1.id}))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('username', None), self.user1.username)
        self.assertEqual(data.get('email', None), self.user1.email)

    def test_user_update(self):
        def update_user(client, user, new_username, new_email):
            return client.patch(
                reverse('user-detail', kwargs={'user_id': user.id}),
                data={"username": new_username, "email": new_email}
            )

        test_cases = (
            {
                "status_code": 200,
                "args": (self.client1, self.user1, "Pol", "Pol@mail.ru")
            },
            {
                "status_code": 400,
                "args": (self.client1, self.user1, self.user2.username, self.user2.email)
            },
            {
                "status_code": 403,
                "args": (self.client1, self.user2, "New name", "new@mail.ru")
            },
            {
                "status_code": 401,
                "args": (self.anonymous_client, self.user2, "New name", "new@mail.ru")
            },
        )

        for case in test_cases:
            response = update_user(*case["args"])
            self.assertEqual(response.status_code, case["status_code"])

    def test_user_delete(self):
        def delete_user(client, user):
            return client.delete(reverse('user-detail', kwargs={'user_id': user.id}), data={})

        test_cases = (
            {"status_code": 403, "args": (self.client1, self.user2)},
            {"status_code": 401, "args": (self.anonymous_client, self.user2)},
            {"status_code": 204, "args": (self.client1, self.user1)},
        )

        for case in test_cases:
            response = delete_user(*case["args"])
            self.assertEqual(response.status_code, case["status_code"])
