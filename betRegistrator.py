from os.path import abspath as path
import json
import PySimpleGUI as sg



class betManager():

    def __init__(self):
        self.database = json.load(open(path('C:/Users/amurha_p/bets.json')))
        self.bet_example = self.database.get('bets').get('1')
        self.total_wagered = 0.0
        self.win_percentage = 0.0
        self.average_bet_ratio = 0.0
        self.total_profit = 0.0
        self.win_counting = [0,0]

        self.update_values()    
        self.UI()



    def update_values(self):

        for bet_num in range(1, len(self.database.get('bets'))+1):
            self.total_wagered += self.database.get('bets').get(str(bet_num)).get('wagered') 
            
            self.win_counting[0] += 1 if self.database.get('bets').get(str(bet_num)).get('succession') else 0 # win == index 0
            self.win_counting[1] += 1 if not self.database.get('bets').get(str(bet_num)).get('succession') else 0 # loss == index 1

            total_bets = self.database.get('bets').get(str(bet_num)).get('total_bets').split('/') # spliting '100/400' into ['100', '400'] 

        self.average_bet_ratio = (self.average_bet_ratio + (int(total_bets[0]) / (int(total_bets[0]) + int(total_bets[1])))*100)/2 \
            if self.average_bet_ratio>0 else \
                (int(total_bets[0]) / (int(total_bets[0]) + int(total_bets[1])))*100 
        # calculating percentage of winning based on total bets
        # one equation if average_bet_ratio is >0 and another if not

        self.win_percentage = (self.win_counting[0] / (self.win_counting[0] + self.win_counting[1]))*100 # wins / all bets * 100
        self.total_profit = (self.win_counting[0] - self.win_counting[1]) * self.database.get('range') # (win - loss) * bet range



    def update_database(self):

        add_bet_log = dict()

        for key in self.bet_example:

            add_bet_log[key] = bool(self.values[key]) if self.values[key] in 'True' else float(self.values[key]) if '.' in self.values[key] else str(self.values[key])
            # if value is '' or 'True', then bool() it
            # elif value has '.', then float() it
            # else str() it

        self.database['bets'][f'{len(self.database.get("bets"))+1}'] = add_bet_log
        self.update_values()

        # update values in UI
        self.window['totalwagered'].update(round(self.total_wagered, 4))
        self.window['winpercentage'].update(round(self.win_percentage, 2))
        self.window['averagebetratio'].update(round(self.average_bet_ratio, 2))
        self.window['totalprofit'].update(round(self.total_profit, 4))

        



    def UI(self):

        stats_font = 'arial 12 bold' # default font for stats_frame
        sg.theme('DarkAmber')
        
        stats_frame = [
            sg.Frame( 'All Stats', [
                [
                    sg.Text('Total Wagered', text_color='white', font=stats_font, size=(0, 2)), 
                    sg.Push(), # 'push()' pushes the text to the side of the frame
                    sg.Text(str(round(self.total_wagered, 4)), key='totalwagered', font=stats_font, size=(30, 2))],
                [
                    sg.Text('Win Percentage', text_color='white', font=stats_font, size=(0, 2)), 
                    sg.Push(), 
                    sg.Text(f'{round(self.win_percentage, 2)}%', key='winpercentage', font=stats_font, size=(30, 2))],

                [
                    sg.Text('Average Bet Ratio', text_color='white', font=stats_font, size=(0, 6)), 
                    sg.Push(), 
                    sg.Text(f'{round(self.average_bet_ratio, 2)}%', key='averagebetratio', font=stats_font, size=(30, 6))
                ],
                [
                    sg.Text('Total Profit', text_color='white', font=stats_font, size=(0, 1)), 
                    sg.Push(), 
                    sg.Text(str(round(self.total_profit, 4)), key='totalprofit', font=stats_font, size=(30, 1))
                ]
            ])
        ] 

        input_frame = [
            [sg.Text('', size=(15, 1))], # header for alignment

            [sg.Input(key='succession', size=(10, 1)), sg.Text('Succession', size=(11, 1))], 
            [sg.Input(key='wagered', size=(10, 1)), sg.Text('Wagered', size=(11, 1))], 
            [sg.Input(key='total_bets', size=(10, 1)), sg.Text('Total Bets', size=(11, 1))],

            [sg.Text('\n\n\n\n\n')], # pysimplegui simply doesn't want me to align the button, then i did this.
            [sg.Button('SUBMIT', font='verdana 25 bold', button_color='black on ')]
        ]

        layout = [        
            [sg.Frame('', [
                    [
                        sg.Column(input_frame, size=(200, 300), vertical_alignment = 't'), # column with inputs and the submit button

                        sg.Column([], size=(30, 0)), # separation column for item alignment

                        sg.Column([[sg.Push()], stats_frame], vertical_alignment = 'b', justification='right', size=(300, 275)) # column with stats frame
                    ]
            ], size=(550, 300))] 
        ]
    #
    #
    #
        self.window = sg.Window('Bet Log Manager', layout)

        while True:  # Event Loop
            event, self.values = self.window.read()
            print(event, self.values)
            if event == sg.WIN_CLOSED:
                break
            if event == 'SUBMIT':
                
                self.update_database()

        json.dump(self.database, open(path('C:/Users/amurha_p/bets.json'), 'w'), indent=4)
        self.window.close()
#
#
#
if __name__ == '__main__':
    betManager()