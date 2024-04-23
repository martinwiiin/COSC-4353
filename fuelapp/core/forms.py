from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, FuelQuote
from django import forms
from django.core.validators import MaxLengthValidator

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProfileForm(forms.ModelForm):

    STATE_CHOICES = (
        ('', 'Select a state'),
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
    )
    zip_code = forms.CharField(
        max_length=5,
        validators=[MaxLengthValidator(5)],
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True}),
    )
    class Meta:
        model = Profile
        fields = ['full_name', 'address1', 'address2', 'city', 'state', 'zip_code']
        labels = {
            'full_name': 'Full Name',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'city': 'City',
            'state': 'State',
            'zip': 'Zipcode'
        }
        widgets = {
            'fullName': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'state': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'zip': forms.TextInput(attrs={'class': 'form-control', 'required': True})  # Making zip code required
        }

class FuelQuoteForm(forms.ModelForm):
    class Meta:
        model = FuelQuote
        fields = ['gallons_requested', 'delivery_address', 'delivery_date']
        labels = {
            'gallons_requested': 'Gallons Requested',
            'delivery_address': 'Delivery Address',
            'delivery_date': 'Delivery Date',
        }
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'gallons_requested': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }

    def clean_gallons_requested(self):
        gallons_requested = self.cleaned_data.get('gallons_requested')
        if gallons_requested and gallons_requested <= 0:
            raise forms.ValidationError("Gallons requested must be greater than 0.")
        return gallons_requested

