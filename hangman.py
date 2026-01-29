from DB.db_manager import DB
import os
import sys




class Hangman:
    def __init__(self):
        self.db = DB()
        self.gamocnobili_asoebi=[]

    def show_word(self, aso):
        self.gamocnobili_asoebi.append(aso)
        return ''.join(
            a if (a == aso or a in self.gamocnobili_asoebi) else '-'
            if a.isalpha() else "   "
            for a in self.andaza
        )
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    
    def start_game(self):
        print("გამოსაცნობი სიტყვა მზადაა!")
        self.gamocnobili_asoebi = []
        andaza = self.db.get_random_andaza()[0]
        self.db.update_last_date(andaza)

        defisiani = ''.join(
            '-' if x.isalpha() else '   ' if x == ' ' else x
            for x in andaza
        )
        self.defisiani = defisiani
        self.andaza = andaza

        return andaza, defisiani