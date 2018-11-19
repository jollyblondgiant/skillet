from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class Validator(models.Manager):
    def registrator_validator(self, postData):
        errors = {}
        regex_email_valid = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        emailCheckTable = []
        for user in User.objects.all():
            emailCheckTable.append(user.email)
        
        if len(postData['first_name'])==False:
            errors['first_name_null'] = "'First Name' field is required"
        elif len(postData['first_name']) < 3:
            errors['first_name_len'] = 'Name must be 3 letters or more' 
        if len(postData['last_name'])==False:
            errors['last_name_null'] = "'Last Name' field is required"
        elif len(postData['last_name']) < 3:
            errors['last_name_len'] = 'Name must be 3 letters or more'
        elif postData['last_name'].isalpha() == False or postData['first_name'].isalpha() == False:
            errors['name_alpha'] = "'Name' fields can only contain letters"
        if len(postData['email'])==False:
            errors['email_null'] = "'Email' field is required"
        elif postData['email'] in emailCheckTable:
            errors['dup_email'] = "Email already in use"
        elif regex_email_valid.match(postData['email']) == None:
            errors['invalid_email'] = "Email format invalid"
        if len(postData['password'])==False:
            errors['password_null'] = "'Password' field is required"
        elif len(postData['password']) < 8:
            errors['password_len'] = "Choose a password at elast 8 characters in length"
        if 'password_confirm' not in postData:
            errors['password_confirm_null'] = "confirm password"
        elif postData['password'] != postData['password_confirm']:
            errors['password_confirm_mismatch'] = "'Password' and 'Confirm Password' must match"
        return errors
        
    def login_validator(self, postData):
        errors = {}
        if len(postData['loginEmail'])==False:
            errors['email_null'] = "'Email' field required"
        elif not User.objects.filter(email=postData['loginEmail']).exists():
                errors['Null_user'] = "Please register"

        elif len(postData['loginPassword'])==False:
            errors['password_null'] = "Please enter Password"
        elif not bcrypt.checkpw(postData['loginPassword'].encode(), User.objects.get(email=postData['loginEmail']).password.encode()):
            errors['bad_pw']="Incorrect Password"
        return errors
    

class Pantry(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Product(models.Model):
    pantry = models.ForeignKey(Pantry, related_name = "product")
    name = models.CharField(max_length=255)
    quantity = models.PositiveSmallIntegerField()
    measure = models.CharField(max_length = 255, default = "unit")        # use this attr. to establish values such as "quart" or "tsp" or "pound". we need to be DILLIGENT to be CONSISTENT so we can search/filter by this field
    description = models.CharField(max_length=255)
    image = models.CharField(max_length = 255, default = "please link to static img")    # use this field to link to static img file, update default once we have a default watermark to use instead
    price = models.PositiveSmallIntegerField()          # represent price in cents, present to user after dividing by 100
    shelf_life = models.PositiveSmallIntegerField()     # Product.shelf_life should be expressed in days // HOW TO EXPRESS NON-PERISHABLE? **FOR NOW, USE (AND {IF-CHECK} FOR) 0**
    # there exists a ManyToMany with Diet below
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    pantry = models.ForeignKey(Pantry, related_name = "user")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Validator()

class GroceryList(models.Model):
    product = models.ForeignKey(Product, related_name = "product_grocery_list")
    user = models.OneToOneField(User, related_name = "user_grocery_list")
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
class Diet(models.Model):
    user = models.ForeignKey(User, related_name = "diet")
    preference = models.CharField(max_length = 255)
    products = models.ManyToManyField(Product, related_name="diets")
    # ManyToMany with Product, as explained above
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Restriction(models.Model):
    name = models.CharField(max_length=255)
    diet = models.OneToOneField(Diet, on_delete=models.CASCADE)
    # A restriction is a more specific form of diet, and should be reserved for when a user CANNOT allow that object, eg allergy.
    # OneToMany documentation: https://docs.djangoproject.com/en/2.1/topics/db/examples/one_to_one/
    # when creating an instance with a restriction, it MUST HAVE a diet in its declaration, and that diet SHOULD HAVE a user associated with it.
    # in this way, a user's restrictions can be accessed the same way we access that user's diet: User.objects.get({{value}}).diet.restriction
    # Users can be accessed through Restricion.diet.user
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
# class "user" is not yet set up to accept any relationships or input related to the rest of the app


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    #probably won't need the 'author' field,
    #adding it, just in case
    author = models.ForeignKey(User, related_name="recipes_submitted")
    #this field we'll definitely need:
    added_by = models.ManyToManyField(User, related_name='added_recipes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

#This is for linking product types with recipes
#stores quantity required and text notes, again
#just in case
class RecipeComponents(models.Model):
    product = models.ForeignKey(Product, related_name='used_in_recipe')
    recipe = models.ForeignKey(Recipe, related_name="components")
    quantity = models.IntegerField()
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
<<<<<<< HEAD
=======

>>>>>>> origin/andy
