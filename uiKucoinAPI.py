import PySimpleGUI as sg




sg.theme('DarkAmber')

input_frame = [
    [
        sg.Frame('', [
            [sg.Input(key='pair', size=(4, 1)), sg.Text('Pair', size=(4, 1))],
            [sg.Button('SUBMIT', font='verdana 15 bold', button_color='black on ')]
        ])
    ]
]


layout = [
    input_frame
]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Show':
        window['-OUTPUT-'].update(values['-IN-'])

window.close()