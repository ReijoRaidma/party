from django.conf.urls import url
from parties import views


urlpatterns = [
    url(r'pealeht', views.party_list, name='party_list'),
    url(r'add_party', views.add_party, name='add_party'),
    url(r'(?P<pk>\d+)/edit_party', views.edit_party, name='edit_party'),
    url(r'(?P<pk>\d+)/', views.party_detail, name='detail'),

]
