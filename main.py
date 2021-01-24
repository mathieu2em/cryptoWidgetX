import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('coinList'),sg.Text('currencyChoiceList'), sg.Button('addCoinToTicker') ],
            [sg.Text('Coin 1 :'), sg.Text('coinAbbrevName'), sg.Text('smallGraphOfCoinEvolution')],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('cryptoWidgetX', layout,
        no_titlebar=True,
        grab_anywhere=True,
        keep_on_top=True,
        background_color='white',
        alpha_channel=.6,
        margins=(0,0))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()

