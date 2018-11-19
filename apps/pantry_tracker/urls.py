from django.conf.urls import url
from . import views

urlpatterns = [
    #log out clears session user_id
    url(r'logout$', views.logout),

    
    #edit pantry allows user to edit their current pantry
    url(r'editPantry$', views.editPantry),

    
    #My pantry holds all of the items in your home's pantry
    url(r'myPantry$', views.myPantry),

    
    #View Product show the product information that was clicked on
    url(r'viewProduct$', views.viewProduct),

    
    #Products shows a list of the products available
    url(r'products$', views.products),

    
    #Allows user to edit the shopping list
    url(r'editShoppingList$', views.editShoppingList),

    
    #Displays the current ShoppingList
    url(r'shoppingList$', views.shoppingList),

    
    #Allows user to edit their profile
    url(r'editProfile$', views.editProfile),

    
    #Allows all users to view a user's profile
    url(r'profile$', views.profile),

    
    #Our homepage after you log in
    url(r'dashboard$', views.dashboard),

    
    #Process to validate and save the form's data
    url(r'registerUser$', views.registerUser),

    
    #Form for a new user to register
    url(r'register$', views.register),

    
    #Checks the form's data to the Database to check if the user has an account, password is correct
    url(r'loginUser$', views.loginUser),

    
    #Form for a returning user to login
    url(r'login$', views.login),

    
    #Landing page for when a user is not signed in
    url(r'^$', views.landing),
]