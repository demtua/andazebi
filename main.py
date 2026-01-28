from DB.db_manager import DB
import unicodedata






entered_word=None
gamocnobili_asoebi = []
andaza = None
defisiani = ''
araswori = 0

db = DB()

def show_word(aso, andaza):
    return ''.join(
        a if (a == aso or a in gamocnobili_asoebi) else '_'
        if a.isalpha() else a
        for a in andaza
    )

def start_game():
    print("გამოსაცნობი სიტყვა მზადაა!")

    andaza = db.get_random_andaza()[0]
    db.update_last_date(andaza)

    masked = ''.join(
        '_' if x.isalpha() else ' ' if x == ' ' else x
        for x in andaza
    )

    return andaza, masked


print("შეიყვანეთ ასო ან 'exit' გამოსასვლელად")
andaza, defisiani = start_game()
    
while entered_word != 'exit':
    print()
    print(defisiani)
    print()
    print(f"სიცოცხლე: {5-araswori}")
    entered_letter = input(f"შეიყვანეთ ასო ან 'exit' გამოსასვლელად  ")
    gamocnobili_asoebi.append(entered_letter)
    #arasworad gamocnoba
    if not entered_letter in andaza:
        print()
        print(f'არასწორი ასო {entered_letter}')
        print()
        araswori+=1


    
    defisiani = show_word(entered_letter, andaza)
    
    #wagebis cheki
    if 5 - araswori == 0:

        print('თქვენ დამარცხდით')
        
        print()

        again = input("გსურთ თავიდან თამაში? აკრიფეთ 'კი' ")
        if again == 'კი':
            andaza, defisiani = start_game()
        else:
            entered_word = 'exit'
            print()
            print('თქვენ გახვედით თამაშიდან')
    
