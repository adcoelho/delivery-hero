from django.conf.urls import url
from restaurants import views

urlpatterns = [
    url(r'^restaurants/$', views.RestaurantList.as_view()),
    url(r'^restaurants/(?P<pk>[0-9]+)/$', views.RestaurantDetail.as_view()),
]
