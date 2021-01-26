import PySimpleGUI as sg
import sched, time
import requests
import json
from RepeatedTimer import RepeatedTimer

URL = "https://api.binance.com/api/v3/avgPrice?symbol=BTCBUSD"

BTCval = ''

def main() :
    global BTCval
    global window

    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  #[sg.Text('coinList'),sg.Text('currencyChoiceList'), sg.Button('addCoinToTicker') ],
                #[sg.Text('Bitcoin :'), sg.Text('coinAbbrevName'), sg.Text('smallGraphOfCoinEvolution')],
                [sg.Text('', size=(22,1), key='output'), sg.Button('x')]]

    # Create the Window
    window = sg.Window('cryptoWidgetX', layout,
            no_titlebar=True,
            grab_anywhere=True,
            keep_on_top=True,
            background_color='white',
            alpha_channel=.6,
            margins=(0,0),
            finalize=True)

    tikBTC()
    rt = scheduleTask()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'x': # if user closes window or clicks cancel
            rt.stop()
            break
        print('You entered ', values[0])

    window.close()

def scheduleTask():
    global BTCval
    rt = RepeatedTimer(3, tikBTC)
    return rt

def tikBTC():
    global BTCval
    global window
    
    payload={}
    headers = {}
    response = requests.request("GET", URL, headers=headers, data=payload)

    print(response.text)

    us_val = float(json.loads(tikCAD2USD())['rates']['USD'])
    

    BTCval = float(json.loads(response.text)['price'])

    VALUE = BTCval*(1/us_val)

    #textToShow = BTCval['base'] + ': ' + BTCval['amount'] + '$ ' + BTCval['currency']
    textToShow = 'BTC: ' + str(VALUE) + '$ CAD'
    window['output'].update(textToShow)   

def tikCAD2USD():
    url = "https://api.exchangeratesapi.io/latest?base=CAD&symbols=USD"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def convert(price, baseCurr, foreignCurr) :
    return price*(baseCurr/foreignCurr)

main()