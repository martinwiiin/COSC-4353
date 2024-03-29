from django.test import TestCase
from django.contrib.auth.models import User
from .forms import SignUpForm,ProfileForm,FuelQuoteForm
from .models import Profile,FuelQuote


class SignUpFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertEqual(form.errors['password2'], ['This field is required.'])


    def test_username_exists(self):
        # Create a user with the same username
        existing_user = User.objects.create_user(username='testuser', password='testpassword123')
        form_data = {
            'username': 'testuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['A user with that username already exists.'])
class ProfileFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'full_name': 'John Doe',
            'address1': '123 Main St',
            'address2': 'Apt 101',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '12345'
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = ProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], ['This field is required.'])
        self.assertEqual(form.errors['address1'], ['This field is required.'])
        self.assertEqual(form.errors['city'], ['This field is required.'])
        self.assertEqual(form.errors['state'], ['This field is required.'])
        self.assertEqual(form.errors['zip_code'], ['This field is required.'])

    def test_invalid_state(self):
        form_data = {
            'full_name': 'John Doe',
            'address1': '123 Main St',
            'city': 'Anytown',
            'state': 'InvalidState',
            'zip_code': '12345'
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['state'], ['Select a valid choice. InvalidState is not one of the available choices.'])

    def test_zip_code_length(self):
        # Test case where zip code is too long
        form_data = {
            'full_name': 'John Doe',
            'address1': '123 Main St',
            'city': 'Anytown',
            'state': 'CA',
            'zip_code': '123456'
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        
class FuelQuoteFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'gallons_requested': 100,
            'delivery_address': '123 Main St',
            'delivery_date': '2024-04-01',
            'suggested_price': 2.5,
            'total_amount_due': 250
        }
        form = FuelQuoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = FuelQuoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['gallons_requested'], ['This field is required.'])
        self.assertEqual(form.errors['delivery_address'], ['This field is required.'])
        self.assertEqual(form.errors['delivery_date'], ['This field is required.'])
        self.assertEqual(form.errors['suggested_price'], ['This field is required.'])
        self.assertEqual(form.errors['total_amount_due'], ['This field is required.'])

    def test_invalid_gallons_requested(self):
        # Test case where gallons requested is negative
        form_data = {
            'gallons_requested': -100,
            'delivery_address': '123 Main St',
            'delivery_date': '2024-04-01',
            'suggested_price': 2.5,
            'total_amount_due': 250
        }
        form = FuelQuoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['gallons_requested'], ['Gallons requested must be greater than 0.'])

