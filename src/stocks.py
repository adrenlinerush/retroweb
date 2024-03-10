import requests
from shared_functions import config
from flask import Blueprint

stocks = Blueprint('stocks', __name__)

STOCKTOKEN=config['MAIN']['StockApiToken']
@stocks.route('/stocks')
def stockUpdates():
    SYMBOLS=config['stocks']
    html_return = []
    html_return.append("<table>")
    for (SYM, display) in SYMBOLS.items():
        SYM=SYM.upper()
        r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + SYM + '&token=' + STOCKTOKEN)
        try:
            stock = r.json()
        except Exception as e:
            print(r.text)
            print(e)
            continue
        if 'error' in stock.keys():
           print(stock['error'])
           continue
        color = ''
        img = ''
        change = ''
        if stock['c'] > stock['pc']:
            color = 'green'
            img = '/static/images/up.jpg'
            change = "+" + str(round(stock['c'] - stock ['pc'],2))
        else:
            color = 'red'
            img = '/static/images/down.jpg'
            change = "-" + str(round(stock['pc'] - stock ['c'],2))
        html_return.append("<tr><font color=\"" + color + "\"><td><img src=\"" + img + "\" height=\"25\"></td>")
        html_return.append("<td>" + SYM + "</td>")
        html_return.append("<td>" + display + "</td>")
        html_return.append("<td>" + change + "</td>")
        html_return.append("<td>" + str(round(stock['c'],2)) + "</td></font></tr>")
    html_return.append("</table>")
    html = "\n".join(html_return)
    return html