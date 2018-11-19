from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    #path('', RedirectView.as_view(url='parts/')),
    path('inventory/', views.PartListView.as_view(), name='inventory'),
    path('inventory/create/', views.PartCreate.as_view(), name='create'),
]
