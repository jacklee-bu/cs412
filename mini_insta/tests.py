from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CreateProfileFlowTests(TestCase):
    """Verify that anonymous users can create profiles."""

    def test_create_profile_success(self):
        """Anonymous visitor can register and create a profile."""
        response = self.client.post(
            reverse('mini_insta:create_profile'),
            {
                'user-username': 'integrationtester',
                'user-password1': 'StrongPass123!',
                'user-password2': 'StrongPass123!',
                'profile-username': 'integrationtester_profile',
                'profile-display_name': 'Integration Tester',
                'profile-bio_text': 'Testing the create profile flow.',
                'profile-profile_image_url': 'https://example.com/avatar.png',
            },
            follow=False,
        )

        # the POST should succeed and redirect to the profile detail page
        self.assertEqual(response.status_code, 302)

        # The Django user and the profile should both exist
        self.assertTrue(User.objects.filter(username='integrationtester').exists())
        profile = User.objects.get(username='integrationtester').profile_set.first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.username, 'integrationtester_profile')
        self.assertEqual(profile.user.username, 'integrationtester')
