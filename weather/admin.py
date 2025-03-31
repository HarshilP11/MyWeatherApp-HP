from django.contrib import admin
from .models import City, WeatherReport
# Inline admin interface is used for displaying the weather reports for a given city
class CityReportInline(admin.TabularInline):
    model = WeatherReport
    extra = 0
    readonly_fields = ('temperature', 'condition', 'icon_url', 'last_updated')
# Admin configuration for the city model
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'added_at', 'report_count')
    search_fields = ('name',)
    list_filter = ('added_at',)
    inlines = [CityReportInline]
    def report_count(self, obj):
        return obj.weather_reports.count()
    report_count.short_description = "Weather Report Count"
# Admin configuration again for the weather report model
@admin.register(WeatherReport)
class WeatherReportAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'condition', 'last_updated')
    list_filter = ('city', 'condition', 'last_updated')
    search_fields = ('city__name', 'condition')
