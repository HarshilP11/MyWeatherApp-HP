from django.db import models

class City(models.Model):
    name = models.CharField(
        max_length=100,  
        unique=True,     
        help_text="Name of the city."
    )
    added_at = models.DateTimeField(
        auto_now_add=True,  # This will set the field to the current date or time when the object is first created
        help_text="When the city was added."
    )
    def __str__(self):
        return self.name
    def latest_weather_report(self):
        # Orders related weather reports by the 'last_updated' field in descending order and returns the first record, which is the latest one
        return self.weather_reports.order_by('-last_updated').first()


# Weather Report model stores the weather information for a specific city
class WeatherReport(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,  # If the city is deleted, this will delete all its weather reports
        related_name='weather_reports', 
        help_text="The city for which this weather report belongs."
    )
    temperature = models.FloatField(
        help_text="Temperature in Celsius."
    )
    condition = models.CharField(
        max_length=100,  # Maximum allowed length for the condition description
        help_text="Weather condition description."
    )
    # THis part stores a URL pointing to an icon image representing the weather condition
    icon_url = models.URLField(
        max_length=200,  
        blank=True,      
        null=True,       
        help_text="Optional URL for a weather icon."
    )
    last_updated = models.DateTimeField(
        auto_now=True,  
        help_text="When this report was last updated."
    )

    def __str__(self):
        return f"{self.city.name} - {self.temperature}°C, {self.condition}"

    # Meta options for the WeatherReport model
    class Meta:
        # Ensures that weather reports are ordered with the most recently updated first
        ordering = ['-last_updated']
