import PySimpleGUI as sg
import sched, time
import requests
import json
from RepeatedTimer import RepeatedTimer

def main() :
    global window
    sg.theme('DarkAmber')   # Add a touch of color

    rowsCurrencies = ['BTCBUSD','ADABUSD']

    # All the stuff inside your window.
    layout = [  *[[sg.Text('', size=(22,1), key=curr+'_output' )] for curr in rowsCurrencies],
                [sg.InputText()],
                [sg.Button('add', key='add'), sg.Button('exit')]]

    # Create the Window
    window = sg.Window('cryptoWidgetX', layout,
            no_titlebar=True,
            grab_anywhere=True,
            keep_on_top=True,
            background_color='white',
            alpha_channel=.6,
            margins=(0,0),
            finalize=True)

    # number of buttons to add
    rows_number = 0

    tikBTC(rowsCurrencies.copy())

    rt = scheduleTask(rowsCurrencies.copy(), window)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'exit': # if user closes window or clicks cancel
            rt.stop()
            break
        if event == 'add':
            
            rt.stop()

            rowsCurrencies.append(values[0])

            rows_number += 1

            layout = [*[[sg.Text('', size=(22,1), key=curr+'_output' )] for curr in rowsCurrencies],
                      [sg.Button('add', key='add'), sg.Button('exit')]]

            window1 = sg.Window('cryptoWidgetX', layout,
                                location=window.CurrentLocation(),
                                no_titlebar=True,
                                grab_anywhere=True,
                                keep_on_top=True,
                                background_color='white',
                                alpha_channel=.6,
                                margins=(0,0),
                                finalize=True)

            rt = RepeatedTimer(3, tikBTC, rowsCurrencies)

            window.Close()
            window = window1
    window.close()

def scheduleTask(currencies, window):
    rt = RepeatedTimer(3, tikBTC, currencies)
    return rt

def tikBTC(currencies):
    global window

    print(currencies)

    partial_results = (tikBinance(curr) for curr in currencies)

    us_val = float(json.loads(tikCAD2USD())['rates']['USD'])

    results = (float(json.loads(currency_response.text)['price'])*(1/us_val) 
                for currency_response in partial_results)

    textsToShow = ((curr[0:3] + " " + str(result)[0:8] + " " + '$ CAD') for curr,result in zip(currencies, results))

    for curr,text in zip(currencies, textsToShow):
        print("curr",curr)
        print("text", text)
        window[curr + '_output'].update(text)    

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