from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.TypeListView.as_view(), name='list_types'),
    path('type/create/', views.TypeCreate.as_view(), name='create_type'),
    
    url(r'^parts/(?P<type_id>\d+)/$',
        views.ListParts.as_view(),
        name='list_parts'),
    url(r'^create_part/(?P<type_id>\d+)/$',
        views.PartCreate,
        name='create_part'),
    
    path('manufacturer/create/',
         views.CreateManufacturer.as_view(),
         name='create_manufacturer'),
    path('location/create/',
         views.CreateLocation.as_view(),
         name='create_location'),
    
    
]
