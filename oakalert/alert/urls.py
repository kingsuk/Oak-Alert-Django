from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/main', views.api_main, name='api_main'),
    path('api/v1/main-deep-dive', views.api_main_deep_dive_output, name='api_main_deep_dive_output'),
    path('api/v1/get-meter-list', views.get_meter_list, name='get_meter_list'),
    path('api/v1/get-alert-report', views.get_alert_report, name='get_alert_report'),
    path('api/v1/get-deep-dive-report', views.get_deep_dive_report, name='get-deep-dive-report'),
    path('api/v1/get-summary-table-report', views.get_summary_table_report, name='get-summary-table-report'),
    path('<int:username>/', views.index, name='index'),
]