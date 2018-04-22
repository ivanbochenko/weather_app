from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=9d876cb5ca6a083813fe8d82a45882e0'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        try:
            r = requests.get(url.format(city)).json()

            city_weather = {
                'city': city,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }
            weather_data.append(city_weather)
        except KeyError:
            print('Not a valid name!')

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)


def delete(request, city_id):
    City.objects.filter(id=city_id).delete()

    return redirect('index')
