from rest_framework import serializers
from .models import City, WeatherReport

class WeatherReportSerializer(serializers.ModelSerializer):
    location_name = serializers.ReadOnlyField(source='city.name')
# Read-only field that shows the related city's name and location_name is derived from the name attribute of the related city instance
    class Meta:
        model = WeatherReport
        fields = ['id', 'city', 'location_name', 'temperature', 'condition', 'icon_url', 'last_updated']
        read_only_fields = ['last_updated', 'location_name']

# This SerializerMethodField is used for obtaining the most recent and a list of all the weather reports and this field is computed using the get_current_weather method and get_reports_list method
class CitySerializer(serializers.ModelSerializer):
    current_weather = serializers.SerializerMethodField(read_only=True)
    reports_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'added_at', 'current_weather', 'reports_list']
        read_only_fields = ['added_at', 'current_weather', 'reports_list']
# Method to retrieve and serialize the lastest and  also all weather reports for the city
    def get_current_weather(self, obj):
        report = obj.latest_weather_report()
        if report:
            return WeatherReportSerializer(report).data
        return None
    def get_reports_list(self, obj):
        reports = obj.weather_reports.all().order_by('-last_updated')
        return WeatherReportSerializer(reports, many=True).data

