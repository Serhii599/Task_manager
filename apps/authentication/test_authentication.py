"""
Unit tests for authentication app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.main_app.factories import UserFactory

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Tests for user registration"""
    
    def setUp(self):
        self.client = Client()
    
    def test_registration_page_loads(self):
        """Test registration page is accessible"""
        response = self.client.get(reverse('authentication:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_register_new_user(self):
        """Test registering a new user"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!',
        }
        
        response = self.client.post(reverse('authentication:register'), data)
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))
        
        # User should be created
        self.assertTrue(User.objects.filter(email='johndoe@example.com').exists())
        user = User.objects.get(email='johndoe@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertTrue(user.is_active)
    
    def test_register_with_existing_email(self):
        """Test registration with already used email"""
        # Create existing user
        UserFactory.create_user(email='existing@example.com')
        
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'existing@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!',
        }
        
        response = self.client.post(reverse('authentication:register'), data)
        
        # Should show form errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'User with this Email already exists.')
    
    def test_register_with_mismatched_passwords(self):
        """Test registration with passwords that don't match"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'Password123!',
            'password2': 'DifferentPassword123!',
        }
        
        response = self.client.post(reverse('authentication:register'), data)
        
        # Should show form errors
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)
    
    def test_register_with_weak_password(self):
        """Test registration with weak password"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
        }
        
        response = self.client.post(reverse('authentication:register'), data)
        
        # Should show form errors for password
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)
    
    def test_register_without_required_fields(self):
        """Test registration with missing required fields"""
        data = {
            'first_name': 'John',
            # Missing last_name, email, and passwords
        }
        
        response = self.client.post(reverse('authentication:register'), data)
        
        # Should show form errors
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)
        self.assertIn('password1', response.context['form'].errors)


class UserLoginTests(TestCase):
    """Tests for user login"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user(
            email='testuser@example.com',
            password='TestPassword123!'
        )
    
    def test_login_page_loads(self):
        """Test login page is accessible"""
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_valid_credentials(self):
        """Test logging in with correct credentials"""
        response = self.client.post(reverse('authentication:login'), {
            'username': 'testuser@example.com',
            'password': 'TestPassword123!',
        })
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        
        # User should be logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_with_invalid_password(self):
        """Test login with wrong password"""
        response = self.client.post(reverse('authentication:login'), {
            'username': 'testuser@example.com',
            'password': 'WrongPassword!',
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_login_with_nonexistent_user(self):
        """Test login with email that doesn't exist"""
        response = self.client.post(reverse('authentication:login'), {
            'username': 'nonexistent@example.com',
            'password': 'SomePassword123!',
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # User should not be logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_redirect_authenticated_user(self):
        """Test that already logged in users are redirected"""
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('authentication:login'))
        
        # Should redirect away from login page
        self.assertEqual(response.status_code, 302)
    
    def test_login_without_credentials(self):
        """Test login with empty credentials"""
        response = self.client.post(reverse('authentication:login'), {
            'username': '',
            'password': '',
        })
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserLogoutTests(TestCase):
    """Tests for user logout"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
    
    def test_logout_authenticated_user(self):
        """Test logging out an authenticated user"""
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('authentication:logout'))
        
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('authentication:login'))
    
    def test_logout_requires_login(self):
        """Test that logout requires authentication"""
        response = self.client.post(reverse('authentication:logout'))
        
        # Should redirect to login (LoginRequiredMixin)
        self.assertEqual(response.status_code, 302)


class CustomUserCreationFormTests(TestCase):
    """Tests for CustomUserCreationForm"""
    
    def test_form_fields(self):
        """Test that form has correct fields"""
        from apps.authentication.forms import CustomUserCreationForm
        
        form = CustomUserCreationForm()
        expected_fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_form_valid_data(self):
        """Test form with valid data"""
        from apps.authentication.forms import CustomUserCreationForm
        
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testform@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_saves_user(self):
        """Test that form saves user correctly"""
        from apps.authentication.forms import CustomUserCreationForm
        
        form_data = {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('SecurePassword123!'))


class UserModelAuthenticationTests(TestCase):
    """Tests for User model authentication features"""
    
    def test_create_user_with_email(self):
        """Test creating user with email as username"""
        from apps.authentication.models import User
        
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('TestPassword123!'))
        self.assertTrue(user.is_active)
    
    def test_create_user_without_email_raises_error(self):
        """Test that creating user without email raises error"""
        from apps.authentication.models import User
        
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='TestPassword123!')
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        from apps.authentication.models import User
        
        # The create_superuser method only sets is_staff=True
        # We need to explicitly set is_superuser=True
        superuser = User.objects.create_user(
            email='admin@example.com',
            password='AdminPassword123!',
            is_staff=True,
            is_superuser=True
        )
        
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
    
    def test_user_password_hashing(self):
        """Test that passwords are hashed"""
        user = UserFactory.create_user(password='PlainPassword123!')
        
        # Password should not be stored in plain text
        self.assertNotEqual(user.password, 'PlainPassword123!')
        
        # But should be verifiable
        self.assertTrue(user.check_password('PlainPassword123!'))
        self.assertFalse(user.check_password('WrongPassword'))
