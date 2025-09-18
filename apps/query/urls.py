# query_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Path for the API endpoint (for JavaScript's fetch requests)
    path('api/query/', views.query_builder_api, name='query_builder_api'),

    # Path for serving the main HTML page
    path('', views.query_builder_page, name='query_builder_page'),
]