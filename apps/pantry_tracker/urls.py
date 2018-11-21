from django.conf.urls import url
from . import views

urlpatterns = [

  #Where we start. If logged in will redirect to dash
    #If not logged in - ask to log in or register
    url(r'^$', views.landing),

    #log out clears session user_id
    url(r'logout$', views.logout),

    #Takes user to render the login screen
    url(r'login$', views.login),

    #Processes user name and pw
    url(r'loginUser$', views.loginUser),

    #Draw registration form
    url(r'register$', views.register),

    #Process to validate and save the form's data
    url(r'registerUser$', views.registerUser),

    #Our homepage after you log in
    url(r'dashboard$', views.dashboard),
#**********************************************************

    #Allows user to edit their profile
    url(r'editProfile/(?P<id>\d+)$', views.editProfile),

    #Send changed user data to the DB
    url(r'update_profile/(?P<id>\d+)$', views.update_profile),

#**********************************************************

    #Admin page for User, Product, Recipe CRUD
    url(r'admin_dash$', views.admin_dash),

    url(r'user_delete/(?P<id>\d+)$',views.user_delete),

    #Add a Product to the DB
    url(r'add_product$', views.add_product),
    
#**********************************************************
    #add a built recipe to the db
    url(r'complete_recipe$',views.complete_recipe),

    #push some product instances into the session
    url(r'add_to_recipe$',views.add_to_recipe),
    url(r'recip_incr/(?P<id>\d+)$',views.recip_incr),
    url(r'recip_decr/(?P<id>\d+)$',views.recip_decr),
    url(r'recip_remove/(?P<id>\d+)$',views.recip_remove),

    url(r'recipe_clear$',views.recipe_clear),

    #render separate page for complex recipe building
    url(r'recipe_builder$',views.recipe_builder),

    #Searching for a product redirect
    url(r'recipe_search$', views.recipe_search),
    url(r'recipe_search_clear$',views.recipe_search_clear),
    
#**********************************************************
    #render shopping list page
    url(r'shopping_list/(?P<id>\d+)$',views.shopping_list),

    #chosen groceries go to the list
    url(r'add_groceries$',views.add_groceries),
    url(r'grocery_incr/(?P<id>\d+)$',views.grocery_incr),
    url(r'grocery_decr/(?P<id>\d+)$',views.grocery_decr),
    url(r'grocery_remove/(?P<id>\d+)$',views.grocery_remove),
    url(r'grocery_search$',views.grocery_search),
    url(r'shop_search_clear',views.shop_search_clear),
    #submit shopping list to the pantry
    url(r'done_shopping/(?P<id>\d+)$',views.done_shopping),
    #**********************************
    #pantry manipulation
    url(r'reduce_in_pantry/(?P<id>\d+)$',views.reduce_in_pantry),
    url(r'remove_from_pantry/(?P<id>\d+)$',views.remove_from_pantry),
]