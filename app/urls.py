from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout_user),
    path('quotes', views.show_quotes),
    path('quotes/create', views.create_quote),
    path('quotes/<int:quote_id>/like', views.mark_quote_as_like),
    path('quotes/<int:quote_id>/unlike', views.mark_quote_as_unlike),
    path('quotes/edit/<int:email_id>', views.user_edit),
    path('quotes/<int:email_id>', views.user_quotes),
    path('quotes/<int:email_id>/update', views.user_update),
    path('quotes/<int:quote_id>/delete', views.quote_destroy),	   
]