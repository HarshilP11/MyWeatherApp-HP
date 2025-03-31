# If you wish to use data_wizard during development and testing, please feel
# free to do so. This does not carry any marks but may help you as you work on
# the project.

import data_wizard
from .models import City, WeatherReport
data_wizard.register(City)
data_wizard.register(WeatherReport)
