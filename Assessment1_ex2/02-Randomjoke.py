from tkinter import *
from PIL import ImageTk, Image
import random
import pygame
# k𖹭.ᐟ------------------giving instruction to open the .txt file---------------------------$𖹭.ᐟ
with open("ex2/randomjoke.txt", "r", encoding="utf-8") as f:
    jokes = [line.strip() for line in f.readlines() if "?" in line]

active_setup = ""
active_punchline = ""
# k𖹭.ᐟ------------------for creating the tkinter window ---------------------------$𖹭.ᐟ
root = Tk()
root.title("Joke with Kulsoom 𖹭.ᐟ")
root.geometry("900x600")
# k𖹭.ᐟ------------------for sound system---------------------------$𖹭.ᐟ
pygame.mixer.init()
# k𖹭.ᐟ------------------audio for background in all frames---------------------------$𖹭.ᐟ
pygame.mixer.music.load("ex2/audio/bgaudio.mp3")  
pygame.mixer.music.play(-1)  

# k𖹭.ᐟ------------------audio for all the remaining btn on all frmae (exit and no button)---------------------------$𖹭.ᐟ
all_button = pygame.mixer.Sound("ex2/audio/btn.mp3")
def all_click():
    all_button.play()
# k𖹭.ᐟ------------------audio for btn 1 on frame1 (play button)---------------------------$𖹭.ᐟ
play_button = pygame.mixer.Sound("ex2/audio/btn1.mp3")
def play_click():
    play_button.play()
# k𖹭.ᐟ------------------audio for btn 2 on frame2 (alexa button)---------------------------$𖹭.ᐟ
alexa_button = pygame.mixer.Sound("ex2/audio/btn2.mp3")
def alexa_click():
    alexa_button.play()
# k𖹭.ᐟ------------------audio for btn 2x on frame2 (next joke button)---------------------------$𖹭.ᐟ
next_button = pygame.mixer.Sound("ex2/audio/btn2x.mp3")
def next_click():
    next_button.play()
# k𖹭.ᐟ------------------audio for btn 2 on frame2 (alexa button)---------------------------$𖹭.ᐟ
punchline_button = pygame.mixer.Sound("ex2/audio/btn2k.mp3")
def punchline_click():
    punchline_button.play()

# k𖹭.ᐟ------------------function define for switching the frame---------------------------$𖹭.ᐟ
def frame_switch(frame):
    frame.tkraise()
# k𖹭.ᐟ------------------function define for picking up a random joke---------------------------$𖹭.ᐟ
def drop_joke():
    global active_setup, active_punchline
    joke = random.choice(jokes)
    parts = joke.split("?")
    active_setup = parts[0].strip()
    active_punchline = parts[1].strip()
# k𖹭.ᐟ------------------function define for displaying first joke---------------------------$𖹭.ᐟ
def spill_the_joke():
    drop_joke()
    drop_joke_label.config(text=active_setup + "?") 
    spill_punchline_label.config(text="") 
# k𖹭.ᐟ------------------function define for displaying punchline---------------------------$𖹭.ᐟ
def spill_punchline():
    if active_punchline:
        spill_punchline_label.config(text=active_punchline)
    else:
        spill_punchline_label.config(text="Please click the setup button first.")
# k𖹭.ᐟ------------------function define for displaying the next joke---------------------------$𖹭.ᐟ
def more_joke():
    spill_the_joke()

# k𖹭.ᐟ------------------This is my frame 1---------------------------$𖹭.ᐟ
frame1 = Frame(root, width=900, height=600)
frame1.place(x=0, y=0)
# k𖹭.ᐟ------------------background image for frame 1---------------------------$𖹭.ᐟ
frame1bg = ImageTk.PhotoImage(Image.open("ex2/background/bg1.jpg").resize((900, 595)))
Label(frame1, image=frame1bg).place(x=0, y=0)
# k𖹭.ᐟ------------------button image for frame 1 (play button)---------------------------$𖹭.ᐟ
btn1 = ImageTk.PhotoImage(Image.open("ex2/btn/button1.png").resize((75, 70)))
Button(frame1, image=btn1, borderwidth=0, highlightthickness=0,

bg=frame1["bg"], activebackground=frame1["bg"],
command=lambda: [play_click(), frame_switch(frame2)]).place(x=555, y=475)


# k𖹭.ᐟ------------------This is my frame 2---------------------------$𖹭.ᐟ
frame2 = Frame(root, width=900, height=600)
frame2.place(x=0, y=0)
# k𖹭.ᐟ------------------background image for frame 2---------------------------$𖹭.ᐟ
frame2bg = ImageTk.PhotoImage(Image.open("ex2/background/bg2.jpg").resize((900, 595)))
Label(frame2, image=frame2bg).place(x=0, y=0)

# k𖹭.ᐟ------------------label to display the jokes---------------------------$𖹭.ᐟ
drop_joke_label = Label(frame2, text="", bg="#e5e3e3", fg="black",
font=("Arial", 15), wraplength=245, justify="center")
drop_joke_label.place(x=158, y=140)   
# k𖹭.ᐟ------------------label to display the punchline---------------------------$𖹭.ᐟ
spill_punchline_label = Label(frame2, text="", bg="#e0dede", fg="black",
font=("Arial", 15), wraplength=200, justify="center")
spill_punchline_label.place(x=460, y=230)

# k𖹭.ᐟ------------------first button image for frame 2 (alexa tell me a joke)------------------$𖹭.ᐟ
btn2 = ImageTk.PhotoImage(Image.open("ex2/btn/button2.png").resize((164, 120)))
Button(frame2, image=btn2, borderwidth=0, highlightthickness=0,

bg=frame2["bg"], activebackground=frame2["bg"],
command=lambda: [alexa_click(), spill_the_joke()]).place(x=708, y=40)
# k𖹭.ᐟ------------------second button image for frame 2 (punchline)------------------$𖹭.ᐟ
btn2k = ImageTk.PhotoImage(Image.open("ex2/btn/button2k.png").resize((75, 50)))
Button(frame2, image=btn2k, borderwidth=0, highlightthickness=0,

bg=frame2["bg"], activebackground=frame2["bg"],
command=lambda: [punchline_click(), spill_punchline()]).place(x=337, y=253)
# k𖹭.ᐟ------------------third button image for frame 2 (next joke)------------------$𖹭.ᐟ
btn2x = ImageTk.PhotoImage(Image.open("ex2/btn/button2x.png").resize((75, 45)))
Button(frame2, image=btn2x, borderwidth=0, highlightthickness=0,

bg=frame2["bg"], activebackground=frame1["bg"],
command=lambda: [next_click(), more_joke()]).place(x=445, y=330)
# k𖹭.ᐟ------------------fourth button image for frame 2 (exit)------------------$𖹭.ᐟ
btn2d = ImageTk.PhotoImage(Image.open("ex2/btn/button2d.png").resize((95, 70)))
Button(frame2, image=btn2d, borderwidth=0, highlightthickness=0,

bg=frame2["bg"], activebackground=frame2["bg"],
command=lambda: [all_click(), frame_switch(frame3)]).place(x=10, y=500)

# k𖹭.ᐟ------------------This is my frame 3---------------------------$𖹭.ᐟ
frame3 = Frame(root, width=900, height=600)
frame3.place(x=0, y=0)
# k𖹭.ᐟ------------------background image for frame 3---------------------------$𖹭.ᐟ
frame3bg = ImageTk.PhotoImage(Image.open("ex2/background/bg3.jpg").resize((900, 595)))
Label(frame3, image=frame3bg).place(x=0, y=0)
# k𖹭.ᐟ------------------button image for frame 3 (yes button)---------------------------$𖹭.ᐟ
btn3 = ImageTk.PhotoImage(Image.open("ex2/btn/button3.png").resize((91, 85)))
Button(frame3, image=btn3, borderwidth=0, highlightthickness=0,

bg=frame3["bg"], activebackground=frame3["bg"],
command=root.destroy).place(x=507, y=448)
# k𖹭.ᐟ------------------button image for frame 3 (no button)---------------------------$𖹭.ᐟ
btn3k = ImageTk.PhotoImage(Image.open("ex2/btn/button3k.png").resize((97, 80)))
Button(frame3, image=btn3k, borderwidth=0, highlightthickness=0,

bg=frame3["bg"], activebackground=frame3["bg"],
command=lambda: [all_click(), frame_switch(frame1)]).place(x=511, y=170)


frame_switch(frame1)
root.mainloop()