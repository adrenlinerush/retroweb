import requests
import xmltodict
from flask import request, Blueprint
import shared_functions

weather = Blueprint('weather', __name__)

def prntTemp(temps,cnt):
    if temps['@type'] == 'minimum':
        label="Low"
    if temps['@type'] == 'maximum':
        label="High"
    return "<td>" + label + ": " + temps['value'][cnt] + "</td>"

@weather.route('/weather', methods=['POST'])
def findLocAndGetWeather():
    loc=request.form['loc']
    api_key=shared_functions.config['MAIN']['geoapi_key']
    location=requests.get('https://api.opencagedata.com/geocode/v1/json?q='+loc+'&key='+api_key)
    loc_dict=location.json()
    lat=str(loc_dict['results'][0]['bounds']['northeast']['lat'])
    lng=str(loc_dict['results'][0]['bounds']['northeast']['lng'])
    print(lat)
    print(lng)
    print(loc_dict['results'][0]['formatted'])
    return renderWeather(lat,lng)


@weather.route('/weather/<lat>/<lon>', methods=['GET'])
def getWeather(lat,lon):
    return renderWeather(lat,lon)


def renderWeather(lat,lon):
    forecast_xml = requests.get('https://forecast.weather.gov/MapClick.php?lat=' + lat + '&lon=' + lon + '&unit=0&lg=english&FcstType=dwml')
    forecast_dict = xmltodict.parse(forecast_xml.text)
    html_return = []
    html_return.append("<body BGCOLOR=\"blue\">")

    html_return.append("<h2>Current Weather for: " + forecast_dict['dwml']['data'][1]['location']['area-description'] + "</h2>")
    try:
        html_return.append(shared_functions.saveImageToCache(forecast_dict['dwml']['data'][1]['parameters']['conditions-icon']['icon-link'], new_h = 100))
    except:
        print("No icon for current weather.")
    html_return.append("<p>")
    html_return.append ("Weather: " + forecast_dict['dwml']['data'][1]['parameters']['weather']['weather-conditions'][0]['@weather-summary'] + "<br/>")
    html_return.append("Temperature: <br/>")
    for temp in forecast_dict['dwml']['data'][1]['parameters']['temperature']:
        html_return.append(temp['@type'] + ": " + str(temp['value']) + temp['@units'] + "<br/>")
    html_return.append("Wind: <br/>")
    for wind in forecast_dict['dwml']['data'][1]['parameters']['wind-speed']:
        html_return.append(wind['@type'] + ": " + str(wind['value']) + wind['@units'] + "<br/>")
    html_return.append("</p>")

    html_return.append("<hr>")
    try:
        html_return.append("<h2>Forecast for: " + forecast_dict['dwml']['data'][0]['location']['description'] + "</h2>")
    except:
        print("No location Description")
    html_return.append("<table>")
    html_return.append("<tr>")
    for layout in forecast_dict['dwml']['data'][0]['time-layout']:
        print(layout['layout-key'])
        if 'k-p12h' in layout['layout-key']:
            for day in layout['start-valid-time']:
                html_return.append("<td><bold>" + day['@period-name'] + "</bold></td>")
    html_return.append("</tr><tr>")
    for icon in forecast_dict['dwml']['data'][0]['parameters']['conditions-icon']['icon-link']:
        html_return.append("<td>" + shared_functions.saveImageToCache(icon,new_h=100) + "</td>")
    html_return.append("</tr><tr>")
    for weather in forecast_dict['dwml']['data'][0]['parameters']['weather']['weather-conditions']:
        html_return.append("<td>" + weather['@weather-summary'] + "</td>")
    html_return.append("</tr><tr>")
    itms=len(forecast_dict['dwml']['data'][0]['parameters']['temperature'][0]['value'])
    for cnt in range(0,int(itms)):
        try:
            html_return.append(prntTemp(forecast_dict['dwml']['data'][0]['parameters']['temperature'][0],cnt))
            html_return.append(prntTemp(forecast_dict['dwml']['data'][0]['parameters']['temperature'][1],cnt))
        except:
                print(Exception)
    html_return.append("</tr><tr>")
    for verbage in forecast_dict['dwml']['data'][0]['parameters']['wordedForecast']['text']:
        html_return.append("<td>" + verbage + "</td>")
    html_return.append("</tr><tr>")
    html_return.append("</table>")
    html_return.append("</body>")
    html = "\n".join(html_return)
    return html
