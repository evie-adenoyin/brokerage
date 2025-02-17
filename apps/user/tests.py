# from django.urls import reverse
# from django.contrib.auth.models import User

# from rest_framework.test import APITestCase
# from .models import UserProfile


# class UserRegistrationTestCase(APITestCase):
#     def test_user_registration(self):
#         data = {
#             "email": "testuser@example.com",
#             "password": "testpass123",
#         }
#         url = reverse("user-registration")

#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 201)

#         user = User.objects.get(username="testuser")
#         profile = UserProfile.objects.get(user=user)

#         self.assertEqual(user.email, "testuser@example.com")
#         self.assertEqual(profile.user.email, "testuser@example.com")


# class AuthenticationTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpass123"
#         )

#     def test_jwt_authentication(self):
#         # Test obtaining JWT tokens
#         url = reverse("token_obtain_pair")
#         data = {"username": "testuser", "password": "testpass123"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("access", response.data)
#         self.assertIn("refresh", response.data)

#         # Test accessing a protected view with JWT
#         # access_token = response.data["access"]
#         # profile_url = reverse("user-profile-detail")
#         # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
#         # response = self.client.get(profile_url)
#         # self.assertEqual(response.status_code, 200)
