from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import City, WeatherReport
from .serializers import CitySerializer, WeatherReportSerializer
from django.shortcuts import get_object_or_404

class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]   
    # This will allow public access to this particular viewset

    def get_queryset(self):
        return City.objects.all().order_by('name')
    # This will return all city objects ordered alphabetically

    @action(detail=False, methods=['get'], url_path='by-name/(?P<name_param>[^/.]+)')
    def retrieve_by_name(self, request, name_param=None):
        city_instance = get_object_or_404(self.get_queryset(), name__iexact=name_param)
        serializer = self.get_serializer(city_instance)
        return Response(serializer.data)
       # THe purpose of this is to return the serialized data in the HTTP response

class WeatherReportViewSet(viewsets.ModelViewSet):
    serializer_class = WeatherReportSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return WeatherReport.objects.all().order_by('-last_updated')
        # Return all WeatherReport objects ordered by latest update (descending)

    @action(detail=False, methods=['get'], url_path='latest/(?P<city_id>[^/.]+)')
    def retrieve_latest(self, request, city_id=None):
        city_instance = get_object_or_404(City, pk=city_id)
        latest_report = city_instance.weather_reports.order_by('-last_updated').first()
        if not latest_report:
            raise ValidationError("There are no weather reports available for this city.")
        serializer = self.get_serializer(latest_report)
        return Response(serializer.data)


