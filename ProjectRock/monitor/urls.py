from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('stream/', views.live_stream_view, name='stream'),
    path('toggle/', views.toggle_adapter_view, name='toggle'),
    path('download/', views.download_pcap, name='download'),
]