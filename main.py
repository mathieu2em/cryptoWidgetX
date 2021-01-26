import PySimpleGUI as sg
import sched, time
import requests
import json
from RepeatedTimer import RepeatedTimer

BTCval = ''
bitcoin = 'BTCBUSD'
ada = 'ADABUSD'

def main() :
    global BTCval
    global window

    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  #[sg.Text('coinList'),sg.Text('currencyChoiceList'), sg.Button('addCoinToTicker') ],
                #[sg.Text('Bitcoin :'), sg.Text('coinAbbrevName'), sg.Text('smallGraphOfCoinEvolution')],
                [sg.Text('', size=(22,1), key='BTC_output')],
                [sg.Text('', size=(22,1), key='ADA_output'), sg.Button('x')]]

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

    responseBitcoin = tikBinance(bitcoin)
    responseAda = tikBinance(ada)

    print(responseBitcoin.text)
    print(responseAda.text)

    us_val = float(json.loads(tikCAD2USD())['rates']['USD'])

    BTCval = float(json.loads(responseBitcoin.text)['price'])
    ADAval = float(json.loads(responseAda.text)['price'])

    BTC_VALUE = BTCval*(1/us_val)
    ADA_VALUE = ADAval*(1/us_val)

    #textToShow = BTCval['base'] + ': ' + BTCval['amount'] + '$ ' + BTCval['currency']
    btcTextToShow = 'BTC: ' + str(BTC_VALUE) + '$ CAD'
    adaTextToShow = 'ADA: ' + str(ADA_VALUE) + '$ CAD'
    window['BTC_output'].update(btcTextToShow)   
    window['ADA_output'].update(adaTextToShow)

def tikCAD2USD():
    url = "https://api.exchangeratesapi.io/latest?base=CAD&symbols=USD"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def convert(price, baseCurr, foreignCurr) :
    return price*(baseCurr/foreignCurr)

def tikBinance(currency):
    URL = "https://api.binance.com/api/v3/avgPrice?symbol="
    
    payload={}
    headers = {}
    response = requests.request("GET", URL+currency, headers=headers, data=payload)
    return response

main()