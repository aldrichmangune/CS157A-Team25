from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login-request/$', views.login_request, name='login-request'),
    url(r'^register/$', views.register, name='register'),
    url(r'^myprofile/$', views.my_profile, name='myprofile'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^textbook/(?P<textbook_id>[0-9]+)/$', views.product_page, name='product-page'),
    url(r'^profile/(?P<account_username>[a-zA-Z0-9]+)/$', views.view_profile, name='view_profile'),
    url(r'^add-listing/$', views.add_listing, name="add-listing"),
    url(r'^add-listing-request/$', views.add_listing_request, name="add-listing-request"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
