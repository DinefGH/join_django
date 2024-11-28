 
from django.test import TestCase
from join_backend.forms import ContactForm
from join_backend.models import Contact



class ContactFormTest(TestCase):
    """
    ContactFormTest:

    A test case class that verifies the validity of the ContactForm under different conditions, 
    ensuring that the form behaves as expected when given valid or invalid input.
    """
    def test_valid_contact_form(self):
        form_data = {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '1234567890', 'color': '#FF5733'}
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_contact_form(self):
        form_data = {'name': '', 'email': 'invalid-email', 'phone': '1234567890', 'color': '#FF5733'}
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)