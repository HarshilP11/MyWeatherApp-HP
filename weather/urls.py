from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from django.contrib import admin, messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.views import APIView
from rest_framework.routers import DefaultRouter
from weather.views import (CityListView, CityCreateAjaxView, CityDeleteAjaxView)
from weather.api_views import CityViewSet, WeatherReportViewSet

def test_message_view(request):
    messages.success(request, "Test message works!")
    return redirect('city-list')

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'weather-reports', WeatherReportViewSet, basename='weatherreport')

class APIRootView(APIView):
    def get(self, request):
        base_url = request.build_absolute_uri('/api/')
        return Response({
            "cities": f"{base_url}cities/",
            "weather_reports": f"{base_url}weather-reports/",
        })

urlpatterns = [
 
    path('ajax/cities/<int:pk>/delete/', CityDeleteAjaxView.as_view(), name='ajax-city-delete'),
    
    path('datawizard/', include('data_wizard.urls')),
    
    path('api/', APIRootView.as_view(), name='api-root'),
   
    path('ajax/cities/add/', CityCreateAjaxView.as_view(), name='add-city'),
   
    path('cities/', CityListView.as_view(), name='city-list'),
   
    path('test-message/', test_message_view, name='test-message'),
   
    path('api/', include(router.urls)),
   
    path('', CityListView.as_view(), name='city-list'),
   
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)