from django.urls import path
from . import views
from .middlewares.auth_user import simple_middleware

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('fil/<int:id>/', views.Index.as_view(), name="fil"),
    path('signup/', views.signup.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),
    path('cart/', views.Cart.as_view(), name="cart"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),
    path('placeorder/', views.Placeorder.as_view(), name="placeorder"),
]
