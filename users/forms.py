from django import forms
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from crispy_forms.layout import Submit, Layout, Div
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div('username', css_class='mb-4'),
            Div('password', css_class='mb-4'),
        )
        self.helper.add_input(Submit('submit', 'Login', css_class='btn btn-primary w-full mt-4'))


class ProfileForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name'
        })
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Profile', css_class='btn btn-primary w-full mt-4'))


class SignupForm(ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password'
        })
    )
    terms_accepted = forms.BooleanField(
        required=True,
        error_messages={'required': 'You must accept the terms and conditions'},
        widget=forms.CheckboxInput(attrs={'class': 'checkbox'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'phone': 'Phone Number',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits')
        if len(phone) != 10:
            raise ValidationError('Phone number must be 10 digits')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError('This phone number is already registered')
        
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div('first_name', css_class='mb-4'),
            Div('last_name', css_class='mb-4'),
            Div('email', css_class='mb-4'),
            Div('phone', css_class='mb-4'),
            Div('password1', css_class='mb-4'),
            Div('password2', css_class='mb-4'),
            Div('terms_accepted', css_class='mb-4'),
        )
        self.helper.add_input(Submit('submit', 'Sign Up', css_class='btn btn-primary w-full mt-4'))
