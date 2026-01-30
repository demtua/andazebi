from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty,NumericProperty, StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from hangman import Hangman
import os
import sys
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

class GameScreen(Screen):
    keyboard_layout = ObjectProperty()
    gamocnobili_asoebi = ListProperty()

    timer = StringProperty('0:30')
    time_left = NumericProperty(30)  # 5 min 30 sec

    _timer_event = None


    defisiani = StringProperty()
    andaza = StringProperty()    
    score = NumericProperty(0)
    mistake = NumericProperty(0)
    image = StringProperty(f'assets/lives/{mistake}.png')

    def __init__(self, **kw):
        super().__init__(**kw)
        self.anbani = [
            "ა", "ბ", "გ", "დ", "ე", "ვ", "ზ", "თ", "ი", "კ",
            "ლ", "მ", "ნ", "ო", "პ", "ჟ", "რ", "ს", "ტ", "უ",
            "ფ", "ქ", "ღ", "ყ", "შ", "ჩ", "ც", "ძ", "წ", "ჭ",
            "ხ", "ჯ", "ჰ"
        ]
        Clock.schedule_once(lambda x: self.add_keyboard(),0.1)
        
        self.hangman = Hangman()
        self.andaza, self.defisiani = self.hangman.start_game()
        self.notifier = Notifier()
        self.timeup = TimeUp()


        
    def time_restart(self):
        self.timer = '0:10'
        self.time_left = App.get_running_app().timer_time 
        self.start_timer()
        self.start_game()
        self.score = 0


    def start_timer(self):
        self.stop_timer()
        self.time_left = App.get_running_app().timer_time 
        self.update_timer_text()
        self._timer_event = Clock.schedule_interval(self.tick, 1)




    def stop_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None





    def tick(self, dt):
        print(self.time_left)
        self.time_left -= 1
        self.update_timer_text()

        if self.time_left <= 0:
            self.timer = "00:00"
            self.stop_timer()
            self.timer_ended()
            return False
    

    def timer_ended(self):
        self.timeup.update(f'{self.score}')
        self.timeup.open()
        self.notifier.title = " დრო ამოიწურა"
        self.notifier.update(f'შენი ქულა არის {self.score}')
        print('timer ended')


    def update_timer_text(self):
        m, s = divmod(max(0, self.time_left), 60)
        self.timer = f"{m:02}:{s:02}"
    
    
    def start_game(self):
        self.mistake = 0
        self.add_keyboard()

        self.andaza, self.defisiani = self.hangman.start_game()
        self.image = self.resource_path(f'assets/lives/{self.mistake}.png')

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def on_enter(self):
        # This runs every time you switch to this screen
        # Clear it first so you don't get double keyboards if you exit/re-enter
        # self.keyboard.clear_widgets() 
        self.add_keyboard()
        self.start_timer()

    def on_leave(self, *args):
        self.stop_timer()

    def add_keyboard(self):
        # This is the main container for all your rows
        keyboard_layout = self.ids.get('keyboard_layout') 
        keyboard_layout.clear_widgets()
        
        # Ensure the main container stacks rows vertically
        keyboard_layout.orientation = 'vertical'
        keyboard_layout.spacing = dp(5)

        row1 = "ქ,წ,ე,რ,ტ,ყ,უ,ი,ო,პ".split(',')
        row2 = "ა,ს,დ,ფ,გ,ჰ,ჯ,კ,ლ".split(',')
        row3 = "ზ,ხ,ც,ვ,ბ,ნ,მ,შ,ჩ,ღ,თ,ძ,ჭ,ჟ".split(',')

        all_rows = [row1, row2, row3]

        for row_data in all_rows:
            # 1. Create a standard BoxLayout (or MDBoxLayout)
            row_container = BoxLayout(
                orientation='horizontal',
                spacing=dp(3),
                size_hint=(None, None),  # Disable auto-scaling
                height=dp(45),
                pos_hint={'center_x': 0.5} # This only works if size_hint_x is None
            )

            # 2. This is the manual version of 'adaptive_width'
            # It tells the container: "Stay exactly as wide as the buttons inside you"
            row_container.bind(minimum_width=row_container.setter('width'))

            for char in row_data:
                key = Button(
                    text=char,
                    font_name=self.resource_path('assets/BPG2.ttf'),
                    font_size='18sp',
                    size_hint=(None, None),
                    size=(dp(35), dp(45))
                )
                key.bind(on_release=self.button_press)
                row_container.add_widget(key)

            keyboard_layout.add_widget(row_container)
    
    def lose(self):
        self.notifier.title = 'წააგე'
        self.notifier.update(f' \n {self.andaza}')

    def win(self):
        self.score += (5-int(self.mistake))
        self.notifier.title = ('მოიგე')
        self.notifier.update(f'გილოცავ \n {self.andaza}')

    def button_press(self, instance):
        instance.disabled = True
        aso = instance.text

        if aso not in self.andaza:
            self.mistake +=1

        if self.mistake > 4:
            self.lose()

        print(self.andaza)
        print(self.defisiani)
        self.defisiani = self.hangman.show_word(aso)
        if not "-" in self.defisiani:
            self.win()

        



class Notifier(Popup):

    text = StringProperty()

    def update(self, text):
        self.text = text        
        self.title_font = self.resource_path("assets/BPG2.ttf")
        self.open()
    
    def cont(self):
        App.get_running_app().game_screen.start_game()
        
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    


class TimeUp(Popup):
    score = StringProperty()
    def update(self, score):
        self.score = score
        self.title_font = self.resource_path("assets/BPG2.ttf")
    
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    