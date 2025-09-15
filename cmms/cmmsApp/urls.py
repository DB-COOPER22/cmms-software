# In iEngApp/urls.py
from django.urls import path
from . import views
from .views import contact_section
app_name = 'cmmsApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('factory/', views.factory, name='factory'),
    path('healthcare/', views.healthcare, name='healthcare'),
    path('facility/', views.facility, name='facility'),
    path('city/', views.city, name='city'),
    path('transport/', views.transport, name='transport'),
    # path('contact/', views.contact, name='contact'),
    path("contacts/", views.contact_section, name="contact_section"),
    path("contacts/thanks/", views.contact_thanks, name="contact_thanks"),
    path("iot/", views.iot, name="iot"),
    path('eam/', views.eam, name='eam'),
    path('apm/', views.apm, name='apm'),
    path('mobility/', views.mobility, name='mobility'),
    path('plans/', views.plans, name='plans'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contact_section, name='contact_section'),
    path('contacts/thanks/', views.contact_thanks, name='contact_thanks'),
    path('workorder/', views.workorder, name='workorder'),
    path('compliance/', views.compliance, name='compliance'),
    path('gis/', views.gis, name='gis'),
    path('scada/', views.scada, name='scada'),
    path('erpsync/', views.erpsync, name='erpsync'),
    # More URLs
]
