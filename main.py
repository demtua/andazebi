from DB.db_manager import DB
import unicodedata






entered_word=None
gamocnobili_asoebi = []
andaza = None
defisiani = ''
araswori = []

db = DB()

def show_word(aso, andaza):
    return ''.join(
        a if (a == aso or a in gamocnobili_asoebi) else '_'
        if a.isalpha() else a
        for a in andaza
    )

def start_game():
    print("გამოსაცნობი სიტყვა მზადაა!")
    print("შეიყვანეთ ასო ან 'exit' გამოსასვლელად")

    andaza = db.get_random_andaza()[0]
    db.update_last_date(andaza)

    masked = ''.join(
        '_' if x.isalpha() else ' ' if x == ' ' else x
        for x in andaza
    )

    return andaza, masked
andaza, defisiani = start_game()
    
while entered_word != 'exit':
    print()
    print(defisiani)
    print()
    print(f"სიცოცხლე: {5-len(araswori)}")
    entered_letter = input(f"შეიყვანეთ ასო ან 'exit' გამოსასვლელად  ")
    if not entered_letter in andaza:
        print()
        print(f'არასწორი ასო {entered_letter}')
        print()
        araswori.append(entered_letter)
    gamocnobili_asoebi.append(entered_letter)
    defisiani = show_word(entered_letter, andaza)
        
    if len(araswori) < 1:

        print('თქვენ დამარცხდით')
        
        print()
        print()
        start_game()
    
