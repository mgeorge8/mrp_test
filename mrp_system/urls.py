from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.TypeListView.as_view(), name='list_types'),
    path('type/create/', views.TypeCreate.as_view(), name='create_type'),
    url(r'^type/edit/(?P<type_id>\d+)/$',
        views.EditType.as_view(),
        name='edit_type'),
    
    url(r'^parts/(?P<type_id>\d+)/$',
        views.ListParts.as_view(),
        name='list_parts'),
    url(r'^part/create/(?P<type_id>\d+)/$',
        views.PartCreate,
        name='create_part'),
    url(r'^part/edit/(?P<type_id>\d+)/(?P<id>\d+)$',
        views.PartEdit,
        name='edit_part'),
    
    path('manufacturer/create/',
         views.CreateManufacturer.as_view(),
         name='create_manufacturer'),
    path('location/create/',
         views.CreateBin.as_view(),
         name='create_location'),
    
    
]
