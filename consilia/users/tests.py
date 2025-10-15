# users/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileUserViewTest(TestCase):
    def setUp(self):
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="secret123",
        )
        self.url = reverse("users:profile")  # ← убедитесь, что имя URL именно такое!

    def test_login_required(self):
        """Неавторизованный пользователь должен быть перенаправлен на страницу входа"""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_profile_page_loads_for_authenticated_user(self):
        """Авторизованный пользователь видит страницу профиля"""
        self.client.login(username="testuser", password="secret123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    # def test_context_contains_default_image_and_user(self):
    #     """Контекст содержит default_image и текущего пользователя"""
    #     self.client.login(username='testuser', password='secret123')
    #     response = self.client.get(self.url)
    #     self.assertIn('default_image', response.context)
    #     self.assertEqual(response.context['default_image'], app_settings.DEFAULT_USER_IMAGE)
    #
    #     self.assertIn('user', response.context)
    #     self.assertEqual(response.context['user'], self.user)

    # @override_settings(DEFAULT_USER_IMAGE='images/default.png')
    # def test_default_image_from_settings(self):
    #     """Проверка, что используется значение из settings"""
    #     self.client.login(username='testuser', password='secret123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.context['default_image'], settings.DEFA)

    def test_get_object_returns_current_user(self):
        """Метод get_object() возвращает текущего пользователя"""
        self.client.login(username="testuser", password="secret123")
        response = self.client.get(self.url)
        # Форма должна быть привязана к текущему пользователю
        self.assertEqual(response.context["form"].instance, self.user)

    # def test_successful_form_update(self):
    #     """Успешное обновление профиля перенаправляет на index"""
    #     self.client.login(username='testuser', password='secret123')
    #     new_email = 'updated@example.com'
    #     response = self.client.post(self.url, {
    #         'email': new_email,
    #         # добавьте другие поля из ProfileUserForm, если они есть, например:
    #         # 'first_name': 'NewName',
    #     })
    #
    #     # Проверяем редирект
    #     self.assertRedirects(response, reverse('index'))
    #
    #     # Проверяем, что данные обновились
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.email, new_email)

    # def test_invalid_form_does_not_update_user(self):
    #     """Невалидная форма не обновляет данные и возвращает ошибки"""
    #     self.client.login(username='testuser', password='secret123')
    #     response = self.client.post(self.url, {
    #         'email': '',  # допустим, email обязателен
    #     })
    #
    #     self.assertEqual(response.status_code, 200)  # остаёмся на той же странице
    #     self.assertFormError(response, 'form', 'email', 'This field is required.')
    #
    #     # Проверяем, что данные не изменились
    #     self.user.refresh_from_db()
    #     self.assertEqual(self.user.email, 'test@example.com')
