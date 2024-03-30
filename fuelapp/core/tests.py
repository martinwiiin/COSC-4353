from django.test import TestCase, Client
from django.urls import reverse
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

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_signup_view = reverse('signup')
        self.test_profile_view = reverse('profile')
        self.test_fqf_view = reverse('FQF')
        

    def test_signup_view(self):

        response = self.client.get(self.test_signup_view)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')

    def test_profile_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_login(user)
        response = self.client.get(self.test_profile_view)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')


    def test_fqf_submission(self):
        form_data = {
            'gallons_requested': 100,
            'delivery_address': '123 Main St',
            'delivery_date': '2024-04-01',
        }
        response = self.client.post(self.test_fqf_view, data= form_data)
    
    def test_fqh_view(self):
        response = self.client.get(reverse('FQH'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/FQH.html')


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
    
    def test_models_Profile(self):
        profile = Profile.objects.create(
            full_name='John Doe',
            address1='123 Main St',
            address2='Apt 101',
            city='Anytown',
            state='CA',
            zip_code='12345'
        )
        self.assertEqual(profile.full_name, 'John Doe')
        self.assertEqual(profile.address1, '123 Main St')
        self.assertEqual(profile.address2, 'Apt 101')
        self.assertEqual(profile.city, 'Anytown')
        self.assertEqual(profile.state, 'CA')
        self.assertEqual(profile.zip_code, '12345')

    def test_models_FuelQuote(self):
        fq = FuelQuote.objects.create(
            gallons_requested=100,
            delivery_address='123 Main St',
            delivery_date='2024-04-01',
            suggested_price=2.5,
            total_amount_due=250
        )
        self.assertEqual(fq.gallons_requested, 100)
        self.assertEqual(fq.delivery_address, '123 Main St')
        self.assertEqual(fq.delivery_date, '2024-04-01')
        self.assertEqual(fq.suggested_price, 2.5)
        self.assertEqual(fq.total_amount_due, 250)


