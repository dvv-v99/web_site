from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignupTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse('signup'), {
            'username': 'ivan',
            'first_name': 'Иван',
            'email': 'Ivan@Example.com',
            'password1': 'Slozhnyy-Parol-2026',
            'password2': 'Slozhnyy-Parol-2026',
        })

        user = User.objects.get(username='ivan')

        self.assertRedirects(response, reverse('account'))
        self.assertTrue(user.check_password('Slozhnyy-Parol-2026'))
        self.assertEqual(user.email, 'ivan@example.com')
        self.assertEqual(user.first_name, 'Иван')

        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_signup_rejects_duplicate_email(self):
        User.objects.create_user(
            username='petr', email='taken@example.com', password='Slozhnyy-Parol-2026'
        )

        response = self.client.post(reverse('signup'), {
            'username': 'ivan',
            'email': 'Taken@Example.com',
            'password1': 'Slozhnyy-Parol-2026',
            'password2': 'Slozhnyy-Parol-2026',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='ivan').exists())
        self.assertContains(response, 'уже зарегистрирован')

    def test_signup_rejects_weak_password(self):
        response = self.client.post(reverse('signup'), {
            'username': 'ivan',
            'email': 'ivan@example.com',
            'password1': '123',
            'password2': '123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='ivan').exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan',
            email='ivan@example.com',
            password='Slozhnyy-Parol-2026',
        )

    def test_login_with_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'ivan',
            'password': 'Slozhnyy-Parol-2026',
        })

        self.assertRedirects(response, reverse('account'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_with_email(self):
        response = self.client.post(reverse('login'), {
            'username': 'Ivan@Example.com',
            'password': 'Slozhnyy-Parol-2026',
        })

        self.assertRedirects(response, reverse('account'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_with_unknown_email_does_not_leak_existence(self):
        unknown_email = self.client.post(reverse('login'), {
            'username': 'nobody@example.com',
            'password': 'Slozhnyy-Parol-2026',
        })

        wrong_password = self.client.post(reverse('login'), {
            'username': 'ivan',
            'password': 'nope-nope-nope',
        })

        def errors(response):
            form = response.context['form']
            return {k: [str(m) for m in v] for k, v in form.errors.items()}

        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEqual(unknown_email.status_code, 200)
        self.assertEqual(errors(unknown_email), errors(wrong_password))

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'ivan',
            'password': 'nope-nope-nope',
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_authenticated_user_is_redirected_from_login(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('login'))

        self.assertRedirects(response, reverse('account'))

    def test_login_honours_next_parameter(self):
        response = self.client.post(
            reverse('login') + '?next=/about/',
            {'username': 'ivan', 'password': 'Slozhnyy-Parol-2026'},
        )

        self.assertRedirects(response, '/about/')


class AccountAccessTests(TestCase):
    def test_anonymous_is_redirected_to_login(self):
        response = self.client.get(reverse('account'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('account')}",
        )

    def test_authenticated_sees_own_username(self):
        User.objects.create_user(
            username='ivan', email='ivan@example.com', password='Slozhnyy-Parol-2026'
        )
        self.client.login(username='ivan', password='Slozhnyy-Parol-2026')

        response = self.client.get(reverse('account'))

        self.assertContains(response, 'ivan')
        self.assertContains(response, 'ivan@example.com')


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ivan', password='Slozhnyy-Parol-2026'
        )
        self.client.login(username='ivan', password='Slozhnyy-Parol-2026')

    def test_logout_requires_post(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_by_post(self):
        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)