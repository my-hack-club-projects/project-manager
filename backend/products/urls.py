from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('list/', views.ProductList.as_view()),
    path('prices/', views.PriceList.as_view()),
    path('keys/', views.KeyList.as_view()),

    path('confirm/', views.ConfirmPayment.as_view()),
]