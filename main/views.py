from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
from bs4 import BeautifulSoup

def content(request):
    city = request.POST['city']
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/74.0.3729.169 Safari/537.36 "
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').content
    return html_content


def home(request):
    if request.method == "GET":
        return render(request, "main/home.html")
    else:
        html_content = content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        obj = soup.find(id="wob_loc")
        if obj is not None:
            result = dict()
            result['region'] = soup.find(id="wob_loc").text
            result['day_time'] = soup.find(id="wob_dts").text
            result['temperature'] = soup.find(id="wob_tm").text
            result['status'] = soup.find(id="wob_dc").text
            result['wind'] = soup.find(id="wob_ws").text
        else:
            result = 0

        return render(request, "main/home.html", {'result': result})
