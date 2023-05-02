from django.urls import path
from . import views
from products.views import ProductView

urlpatterns = [
    path("products/", views.ProductView.as_view()),
    #path("products/<int:pk>/songs/", song_views.SongView.as_view()),
]
