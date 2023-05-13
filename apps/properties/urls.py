from django.urls import path

from apps.properties.views import ListAllPropertiesAPIView, ListAgentsPropertyAPIView, create_property_api_view, \
    PropertyDetailView, update_property_api_view, delete_property_api_view, PropertySearchAPIView

urlpatterns = [
    path('all/', ListAllPropertiesAPIView.as_view(), name='all_properties'),
    path('agents/', ListAgentsPropertyAPIView.as_view(), name='agent-properties'),
    path('create/', create_property_api_view, name='property-create'),
    path('details/<slug:slug>/', PropertyDetailView.as_view(), name='details'),
    path('update/<slug:slug>/', update_property_api_view, name='update-property-api'),
    path('delete/<slug:slug>/', delete_property_api_view, name='delete-property-api'),
    path('search/', PropertySearchAPIView.as_view(), name='property-search'),

]