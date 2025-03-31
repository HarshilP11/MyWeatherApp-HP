from .models import City, WeatherReport
from django import forms

# Form for creating or updating a weather report instance
class WeatherReportForm(forms.ModelForm):
    class Meta:
        model = WeatherReport
        fields = ['temperature', 'icon_url', 'condition', 'city']

# Form for creating or updating a city instance
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
    
    # Custom validation for the city name field
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
        return name

    # Custom validation for the weather condition field
    def clean_condition(self):
        condition = self.cleaned_data.get('condition')
        if not condition:
            raise forms.ValidationError("The given weather condition cannot remain empty.")
        return condition
    
    # Custom validation for the temperature field
    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature is not None:
            if temperature < -150 or temperature > 150:
                raise forms.ValidationError("The given temperature must be in the range of -150 and 150°C.")
        return temperature
