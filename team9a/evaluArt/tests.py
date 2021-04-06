from django.test import TestCase
from evaluArt.models import Category
from django.conf import settings
from django.db import models
from evaluArt import forms
import evaluArt
import os
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from django.urls import reverse, resolve
import re

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

#used to create a user
def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

#make an admin
def create_super_user_object():
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

#returns template as string
def get_template(path_to_template):
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

#checks if all required apps are installed
class installedAppsTests(TestCase):
    def test_installed_apps(self):
        self.assertTrue('django.contrib.admin' in settings.INSTALLED_APPS)
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)
        self.assertTrue('django.contrib.contenttypes' in settings.INSTALLED_APPS)
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)
        self.assertTrue('django.contrib.messages' in settings.INSTALLED_APPS)
        self.assertTrue('django.contrib.staticfiles' in settings.INSTALLED_APPS)
        self.assertTrue('evaluArt' in settings.INSTALLED_APPS)

 #check if category correctly made into slu       
class CategoryMethodTests(TestCase):
    def test_slug_line_creation(self):
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')

#Check profile made correctly
class profileModelTests(TestCase):
    #is class in models and are all attributes present
    def test_userprofile_class(self):
        self.assertTrue('UserProfile' in dir(evaluArt.models))

        user_profile = evaluArt.models.UserProfile()
        
        #create user profile
        expected_attributes = {
            'description': 'just some words',
            'picture': 'default/default.jpg',
            'user': create_user_object(),
        }

        expected_types = {
            'description': models.fields.TextField,
            'picture': models.fields.files.ImageField,
            'experience': models.fields.CharField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0
        
        #iterates through profile meta fields
        for attr in user_profile._meta.fields:
            attr_name = attr.name

            #iterates through expected attributes counting when they are found
            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1
                    #check if attribute is the correct type
                    self.assertEqual(type(attr), expected_types[attr_name], 
                    f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; it should be '{expected_types[attr_name]}'. Check UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        #check there are the correct number of attributes
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}there was {found_count} attributes found but there should be {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        user_profile.save()
    
    #checks if userprofile is accesible
    def test_model_admin_interface_inclusion(self):
        super_user = create_super_user_object()
        self.client.login(username='admin', password='testpassword')

        response = self.client.get('/admin/evaluArt/userprofile/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}wrong status code{FAILURE_FOOTER}")

class RegisterFormClassTests(TestCase):
    #check userform done correctly
    def test_user_form(self):
        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}UserForm isnt in forms.py{FAILURE_FOOTER}")
        
        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}UserForm does not matchthe User model. Check Meta definition.{FAILURE_FOOTER}")

        fields = user_form.fields
        
        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not in the UserForm form.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")
    
    #check userprofile form done correctly
    def test_user_profile_form(self):
        self.assertTrue('UserProfileForm' in dir(forms), f"{FAILURE_HEADER}Couldn't find the UserProfileForm class in forms.py module.{FAILURE_FOOTER}")
        
        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), evaluArt.models.UserProfile, f"{FAILURE_HEADER}UserProfileForm does not match up the UserProfile model. Check Meta definition.{FAILURE_FOOTER}")

        fields = user_profile_form.fields

        expected_fields = {
            'description': django_fields.CharField,
            'picture': django_fields.ImageField,
            'experience': django_fields.TypedChoiceField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")

class RegistrationTests(TestCase):
    #check register view is in the correct location
    def test_new_registration_view_exists(self):
        url = ''

        try:
            url = reverse('evaluArt:register')
        except:
            pass
        
        self.assertEqual(url, '/evaluArt/register/', f"{FAILURE_HEADER}evaluArt:register isn't mapped correctly to url.{FAILURE_FOOTER}")
    
    #is register template in the correct place and inherit from the base template
    def test_registration_template(self):

        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        template_path = os.path.join(template_base_path, 'register.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}Couldn't find 'register.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)evaluArt(\s*|\n*)-(\s*|\n*)Register(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('evaluArt:register'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'evaluArt:register' is not correct.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is register.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")

    #check the register form is correct
    def test_registration_get_response(self):

        request = self.client.get(reverse('evaluArt:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<h1>Register for EvaluArt</h1>' in content, f"{FAILURE_HEADER}ouldn't find the '<h1>Register for evaluArt</h1>' header tag in your register template.{FAILURE_FOOTER}")
        self.assertTrue('enctype="multipart/form-data"' in content, f"{FAILURE_HEADER}Is register.html template using 'multipart/form-data' for the <form>'s 'enctype'?{FAILURE_FOOTER}")
        self.assertTrue('action="/evaluArt/register/"' in content, f"{FAILURE_HEADER}Is <form> in register.html pointing to the correct URL for registering a user?{FAILURE_FOOTER}")
        self.assertTrue('<input type="submit" name="submit" value="Register" />' in content, f"{FAILURE_HEADER}ouldn't find the markup for the form submission button in register.html.{FAILURE_FOOTER}")
        self.assertTrue('<p><label for="id_password">Password:</label> <input type="password" name="password" required id="id_password"></p>' in content, f"{FAILURE_HEADER}Checking a random form field in register.html (password), the markup didn't match what was expected.{FAILURE_FOOTER}")
        
    #check response to a blank form
    def test_bad_registration_post_response(self):

        request = self.client.post(reverse('evaluArt:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)
    
    #check for register successfully
    def test_good_form_creation(self):

        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'experience':'1','description': 'just some words', 'picture': 'default/default.jpg'}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data. Check UserForm.{FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data. Check UserProfileForm.{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()
        
        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()
        
        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}Was expecting User object to be created, but it didn't appear. Check your UserForm implementation, and try again.{FAILURE_FOOTER}")
        self.assertEqual(len(evaluArt.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}Was a UserProfile object created, but it didn't appear. Check UserProfileForm implementation.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}Couldn't log sample user in during the tests. Check implementation of UserForm and UserProfileForm.{FAILURE_FOOTER}")
   
    #check link added to base template
    def test_base_for_register_link(self):

        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        base_path = os.path.join(template_base_path, 'base.html')
        template_str = get_template(base_path)
        self.assertTrue('<a href={% url \'evaluArt:register\' %}>Register</a>' in template_str)

#test login functionality
class LoginTests(TestCase):
    #test view is in correct place
    def test_login_url_exists(self):

        url = ''

        try:
            url = reverse('evaluArt:login')
        except:
            pass
        
        self.assertEqual(url, '/evaluArt/login/', f"{FAILURE_HEADER}login not mapped correctly.{FAILURE_FOOTER}")
    
    #test template exists and that it inherits from the base template
    def test_login_template(self):

        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}couldn't find the 'login.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)evaluArt(\s*|\n*)-(\s*|\n*)Login(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('evaluArt:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'evaluArt:login' is not correct.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is login.html using template inheritance?{FAILURE_FOOTER}")
    
    #test for the content of login template
    def test_login_template_content(self):

        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}Couldn't find the 'login.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('<h1>Login to EvaluArt</h1>' in template_str, f"{FAILURE_HEADER}Couldn't find the '<h1>Login to EvaluArt</h1>' in the login.html template.{FAILURE_FOOTER}")
        self.assertTrue('action="{% url \'evaluArt:login\' %}"' in template_str, f"{FAILURE_HEADER}Couldn't find the url lookup for 'evaluArt:login' in your login.html <form>.{FAILURE_FOOTER}")
        self.assertTrue('<input type="submit" value="submit" />' in template_str, f"{FAILURE_HEADER}Couldn't find the submit button in your login.html template.{FAILURE_FOOTER}")

#test logout functionality  
class LogoutTests(TestCase):

    #tests that logout redirects to the login page
    def test_bad_request(self):

        response = self.client.get(reverse('evaluArt:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('evaluArt:login'))
    
    #tests that logout successfully logs out the user from the profile
    def test_good_request(self):

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Attempted to log in with user ID {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. check login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Check login() view.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('evaluArt:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user didnt cause a redirect{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('evaluArt:login'), f"{FAILURE_HEADER}Did not redirect to login.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}User wasnt logged out.{FAILURE_FOOTER}")

 #tests that all templates are in the correct location
class templateTests(TestCase):
    
    def test_template_directory(self):
        
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        
        about_path = os.path.join(template_base_path, 'about.html')
        artwork_list_path = os.path.join(template_base_path, 'artwork_list.html')
        base_path = os.path.join(template_base_path, 'base.html')
        contact_us_path = os.path.join(template_base_path, 'contact_us.html')
        my_account_path = os.path.join(template_base_path, 'my_account.html')
        search_path = os.path.join(template_base_path, 'search.html')
        show_account_path = os.path.join(template_base_path, 'show_account.html')
        show_artwork_path = os.path.join(template_base_path, 'show_artwork.html')
        upload_artwork_path = os.path.join(template_base_path, 'upload_artwork.html')
        
        self.assertTrue(os.path.exists(about_path), f"{FAILURE_HEADER}Couldn't find the 'about.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(artwork_list_path), f"{FAILURE_HEADER}Couldn't find the 'artwork_list.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(base_path), f"{FAILURE_HEADER}Couldn't find the 'base.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(contact_us_path), f"{FAILURE_HEADER}Couldn't find the 'contact_us.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(my_account_path), f"{FAILURE_HEADER}Couldn't find the 'my_account.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(search_path), f"{FAILURE_HEADER}Couldn't find the 'search.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(show_account_path), f"{FAILURE_HEADER}Couldn't find the 'show_account.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(show_artwork_path), f"{FAILURE_HEADER}Couldn't find the 'show_artwork.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        self.assertTrue(os.path.exists(upload_artwork_path), f"{FAILURE_HEADER}Couldn't find the 'upload_artwork.html' template in the 'templates/evaluArt/' directory.{FAILURE_FOOTER}")
        
#tests that base template contains the required links
class baseTests(TestCase):
    
    def test_links(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'evaluArt')
        base_path = os.path.join(template_base_path, 'base.html')
        template_str = get_template(base_path)
        self.assertTrue('<a class="nav-link" href={% url \'evaluArt:artwork_list\' %}' in template_str)
        self.assertTrue('<a class="nav-link" href={% url \'evaluArt:about\' %}>About</a>' in template_str)
        self.assertTrue('<a class="nav-link" href={% url \'evaluArt:contact_us\' %}>Contact Us</a>' in template_str)
