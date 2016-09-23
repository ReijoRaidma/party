from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from parties import views

router = DefaultRouter()
router.register(r'parties', views.PartyViewSet, base_name='party')
router.register(r'guests', views.GuestViewSet, base_name='guest')
router.register(r'users', views.UserViewSet, base_name='user')

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^$', views.party_list, name='party_list'),
    url(r'add_party', views.add_party, name='add_party'),
    url(r'(?P<pk>[0-9a-z-]+)/edit_party', views.edit_party, name='edit_party'),
    url(r'(?P<pk>[0-9a-z-]+)/', views.party_detail, name='detail'),


]


