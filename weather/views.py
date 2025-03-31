from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
from .models import WeatherReport, City
from .forms import CityForm
# A list of default cities to ensure they will always be available on the website. IF the user deletes then and then they reload the page will come back
default_cities = ['Tokyo', 'New York', 'London']
# The function here is to fetch weather data for any city using the Visual Crossing API
def fetch_weather_for_city(city_name):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    api_key = settings.VISUAL_CROSSING_API_KEY  # MY API key is stored in settings.py
    url = f"{base_url}{city_name}?unitGroup=metric&key={api_key}&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
# This part is responisble to update a city's weather report by fetching current data while also saving it
def update_weather_report(city):
    data = fetch_weather_for_city(city.name)
    if data and 'days' in data and len(data['days']) > 0:
        today = data['days'][0]
        temperature = today.get('temp')
        condition = today.get('conditions')
        icon_url = today.get('icon', '')
        WeatherReport.objects.create(
            city=city,
            temperature=temperature,
            condition=condition,
            icon_url=icon_url
        )
# View below is used to display a list of cities, as weather cards, while making sure default cities are present
class CityListView(LoginRequiredMixin, ListView):
    model = City
    template_name = 'cities/city_list.html'
    context_object_name = 'cities'
# Overriding get_queryset to add default cities if they don't exist or were removed by the user 
    def get_queryset(self):
        for city_name in default_cities:
            if not City.objects.filter(name__iexact=city_name).exists():
                new_city = City.objects.create(name=city_name)
                update_weather_report(new_city)
        return City.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for city in context['cities']:
            city.report_count = city.weather_reports.count()
        return context

class CityCreateAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            if City.objects.filter(name__iexact=city_name).exists():
                return JsonResponse({
                    'status': 'error',
                    'errors': {'name': ['City with this name already exists.']}
                }, status=400)
            city = form.save()
            update_weather_report(city)
            return JsonResponse({
                'status': 'success',
                'city': {'id': city.id, 'name': city.name}
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
# AJAX view is reponsible for the creation of a new city
class CityDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        return self.delete(request, pk, *args, **kwargs)
    
    def delete(self, request, pk, *args, **kwargs):
        city = get_object_or_404(City, pk=pk)
        city.delete()
        return JsonResponse({'status': 'success'})

