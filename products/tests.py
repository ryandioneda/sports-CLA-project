from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Equipment, Review
from .forms import EquipmentFilterForm, ReviewForm


class ProductTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.equipment = Equipment.objects.create(
            name="Test Equipment",
            description="Test Description",
            price_per_day=7.00,
            condition="new",
            category="ball",
            brand="Test Brand",
            is_available=True,
            owner=self.user,
        )
        self.review = Review.objects.create(
            equipment=self.equipment,
            user=self.user,
            text="Test Review",
            rating=5,
        )

    def test_equipment_model(self):
        self.assertEqual(str(self.equipment), "Test Equipment")

    def test_review_model(self):
        self.assertEqual(self.review.text, "Test Review")
        self.assertEqual(self.review.rating, 5)

    def test_equipment_filter_form(self):
        form_data = {
            "search": "Test",
            "category": "ball",
            "condition": "new",
            "min_price": 5.00,
            "max_price": 15.00,
        }
        form = EquipmentFilterForm(form_data)
        self.assertTrue(form.is_valid())

    def test_review_form(self):
        form_data = {
            "text": "Test Review",
            "rating": 4,
        }
        form = ReviewForm(form_data)
        self.assertTrue(form.is_valid())
