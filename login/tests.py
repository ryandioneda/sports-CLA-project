from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, CustomPerms


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            fname="Test",
            lname="User",
            birth_date="2000-01-01",
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.fname, "Test")
        self.assertEqual(self.profile.lname, "User")
        self.assertEqual(self.profile.birth_date, "2000-01-01")

    def test_custom_perms_meta(self):
        self.assertFalse(CustomPerms._meta.managed)
        self.assertEqual(CustomPerms._meta.default_permissions, ())
        self.assertEqual(
            CustomPerms._meta.permissions,
            (
                ("borrower_perms", "Global borrower permissions"),
                ("lender_perms", "Global lender permissions"),
            ),
        )
