from django.test import TestCase

# Create your tests here.
from .forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'first_name', 'last_name' ,'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
