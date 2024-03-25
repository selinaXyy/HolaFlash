from tkinter import *
import pandas as pd
import random, os

BACKGROUND_COLOR = "#B1DDC6"
flip_timer = None

#generate data
new_path = "./data/words_to_learn.csv"
data = pd.read_csv(new_path if os.path.exists(new_path) else "./data/es_to_en_300.csv")
to_learn = data.to_dict(orient="records") #return an dict list
current_card = {}

#funcs
def next_card():
    global current_card, flip_timer
    #if at least one word is generated
    if flip_timer != None:
        #cancel the current after method
        window.after_cancel(flip_timer)

    current_card = random.choice(to_learn) #a single dict
    
    canvas.itemconfig(flashcard, image=img_flashcard_front)
    canvas.itemconfig(txt_language, text="Spanish", fill="black")
    canvas.itemconfig(txt_word, text=current_card["Spanish"], fill="black")
    btn_wrong["state"] = DISABLED

    #reveal answer after 3 seconds
    flip_timer = window.after(3000, func=reveal_answer) 

def reveal_answer():
    global current_card
    canvas.itemconfig(flashcard, image=img_flashcard_back)
    canvas.itemconfig(txt_language, text="English", fill="white")
    canvas.itemconfig(txt_word, text=current_card["English"], fill="white")
    btn_wrong["state"] = NORMAL

def is_known():
    global to_learn
    to_learn.remove(current_card) #remove current card dict from to_learn list
    save_progress()
    next_card()

def save_progress():
    updated_data = pd.DataFrame(to_learn)
    updated_data.to_csv(new_path, index=False) #create a file if no file exists at this path

window = Tk()
window.title("HolaFlash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

#img conversions
img_flashcard_front = PhotoImage(file="./images/card_front.png")
img_flashcard_back = PhotoImage(file="./images/card_back.png")
img_correct = PhotoImage(file="./images/correct.png")
img_wrong = PhotoImage(file="./images/wrong.png")

#flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR) 
flashcard = canvas.create_image(400,263)
canvas.grid(row=0, column=0, columnspan=2)
#txts
txt_language = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
txt_word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))

#btns
btn_wrong = Button(image=img_wrong, highlightthickness=0, borderwidth=0, command=next_card)
btn_correct = Button(image=img_correct, highlightthickness=0, borderwidth=0, command=is_known)
btn_wrong.grid(row=1, column=0)
btn_correct.grid(row=1, column=1)

#start with es(front), then reveal answer in en(back) after 3 sec
next_card()

window.mainloop()