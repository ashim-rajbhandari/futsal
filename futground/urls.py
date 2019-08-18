
from django.urls import path
from .import views


app_name = 'futground'


urlpatterns = [
     path('home/', views.home, name='fut-home'),
     path('list/', views.list, name='fut-list'),
     path('search/', views.search, name='fut-search'),
     path('search/list/futground/<int:ground_id>/', views.detail, name='fut-searchdetail'),
     path('list/futground/<int:ground_id>/', views.detail, name='fut-detail'),
     path('list/futground/<int:reservation_id>/delete/',views.deletereservation,name='fut-delete'),
     #path('list/futground/<int:ground_id>/khalti/', views.khalti, name='fut-khalti'),

     path('recommend/', views.recommend, name='fut-recommend'),
     path('recommned/list/futground/<int:ground_id>/', views.detail, name='fut-recommenddetail'),
     path('rate/<int:ground_id>/', views.rate, name='fut-rate'),

]
