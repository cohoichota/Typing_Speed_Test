from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import math
import requests


timer = None
start = False
click = 0
text_to_show = ""


def get_quote():
    global text_to_show
    response = requests.get(url="https://api.kanye.rest")
    response.raise_for_status()
    data = response.json()
    text_to_show = data["quote"]
    canvas.itemconfig(quote_text, text=text_to_show)


def reset_timer():
    global start, timer
    typing_field.delete("1.0", "end")
    start = False
    button_start['text'] = "START"
    button_start.configure(bg="forestgreen")
    l1_text.set("Click START to enable the typing field.")
    timer_text['fg'] = 'blue'
    timer_text['text'] = 'Timer Ready!'
    typing_field['state'] = 'disabled'
    window.after_cancel(timer)


def start_timer():
    global start, timer, click
    click += 1
    if click % 2 == 1:
        get_quote()
    if not start:
        start = True
        button_start['text'] = "RESET"
        button_start.configure(bg="blue")
        l1_text.set("Click RESET to stop and reset")
        typing_field.delete("1.0", "end")
        typing_field['state'] = 'normal'
        count_up(0)
    else:
        reset_timer()


def count_up(secs):
    global timer, start
    if start:
        count_min = math.floor(secs / 60)
        count_sec = secs % 60
        timer_text['text'] = f"0{count_min}:{count_sec}"
        if secs >= 0:
            timer = window.after(1000, count_up, secs + 1)
            if count_sec < 10:
                timer_text['text'] = f"0{count_min}:0{count_sec}"


def calculate_typing_speed():
    time_total = int(timer.split("#")[-1])
    text_list = text_to_show.strip().split()
    typed_list = typing_field.get("1.0", "end").strip().split()

    valid_words = 0

    for i in range(len(typed_list)):
        if typed_list[i] in text_list:
            valid_words += 1

    accuracy_percentage = round(valid_words / len(typed_list) * 100, 2)

    messagebox.showinfo(
        title="Results",
        message=f"""Total words typed: {len(typed_list)}
        \nAccuracy Percentage: {accuracy_percentage}%
        \nTotal time: {time_total} seconds""")


window = Tk()
window.title("Typing Speed Test")
window.config(bg="#f7f5dd")

BG_COLOR = "#f7f5dd"

canvas = Canvas(width=500, height=550)

image = Image.open("images/card_back.png")

resized_image = image.resize((340, 340))

card_image = ImageTk.PhotoImage(resized_image)
text_card_background = canvas.create_image(200, 250, image=card_image)
quote_text = canvas.create_text(200, 250, text=text_to_show, font=("Ariel", 15), width=150)
canvas.config(bg=BG_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, padx=30, rowspan=3)

l1_text = StringVar()
l1_text.set("Click START to enable the typing field.")
l1 = Label(textvariable=l1_text, bg=BG_COLOR, font=("Arial", 20))
l1.grid(row=0, column=1, columnspan=2)

button_start = Button(text="Start", highlightthickness=0, command=start_timer, fg="white", bg="forestgreen", width=10)
button_start.grid(column=1, row=1)

button_reset = Button(text="Submit", highlightthickness=0, command=calculate_typing_speed, fg="white", bg="red", width=10)
button_reset.grid(column=2, row=1)

timer_text = Label(text="00:00", bg=BG_COLOR, font=("Arial", 25), fg="blue")
timer_text.grid(row=2, column=1)

typing_field = Text(width=40, height=10, padx=35, pady=35, font=("Arial", 13))
typing_field['state'] = 'disabled'
typing_field.grid(row=3, column=1)

window.mainloop()
