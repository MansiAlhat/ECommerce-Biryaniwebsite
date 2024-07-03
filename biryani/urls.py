# urls.py
from django.urls import path
from .views import main_page, sign_up, signin, logout, submit_review

urlpatterns = [
    path('', main_page, name='main_page'),
    path('sign_up/', sign_up, name='sign_up'),  # Define the URL pattern for the sign_up view
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('submit_review/', submit_review, name='submit_review'),
]