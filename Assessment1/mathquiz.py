from tkinter import * # for making buttons, frames, windows and etc..
from PIL import ImageTk, Image # for importing images
from tkinter import messagebox # for pop up msg
import random # this is for picking random numbers 
import pygame # this is use for playing sound or music
import tkinter as tk # another way of using tkinter


# ------------*---------- Root Setup -----------*-----------
root = Tk() # this is to create the main window 
root.title("Math Quiz") # naming the window as "math quiz"
root.geometry("900x600") # and this is the size of the window 
root.iconphoto(False, ImageTk.PhotoImage(file="bgimage/logo.jpg")) # this the logo for the window

# ---------------------- Game Variables ----------------------
score = 0 #score for the user 
question_no = 0 # current question num
attempt = 1 # current attempts 
total_questions = 10 #total questions in the my math quiz
difficulty = "easy"  # default difficulty level
answer = 0 # ans correct for the current question

# ------------------Bg and button sound controls--------------
pygame.mixer.init() #for sound system 


current_volume = 1.0  # Volume ranges
pygame.mixer.music.set_volume(current_volume) #applying starting volume
current_volume = 1.0  # default volume

#function for increase volume
def increase_volume():
    global current_volume
    if current_volume < 1.0:
        current_volume += 0.1
        if current_volume > 1.0:
            current_volume = 1.0
        pygame.mixer.music.set_volume(current_volume)
#function for lower the volume 
def decrease_volume():
    global current_volume
    if current_volume > 0.0:
        current_volume -= 0.1
        if current_volume < 0.0:
            current_volume = 0.0
        pygame.mixer.music.set_volume(current_volume)
# this function is for turning the volume on and off
def toggle_music():
    global current_volume
    if current_volume > 0:
        pygame.mixer.music.set_volume(0)
        current_volume = 0
        volume_button.config(text="🔇")
    else:
        current_volume = 1.0
        pygame.mixer.music.set_volume(current_volume)
        volume_button.config(text="🔊")
# function to add volume button controls on the exiting frame 
def add_volume_buttons(frame):
    global increase_button, decrease_button, volume_button
# this is to increase the volume button 
    increase_button = Button(frame, text="🔊+", font=("Arial", 16, "bold"),fg="black", bg="#ffecf6", activebackground="#ffecf6",borderwidth=0, command=increase_volume)
    increase_button.place(x=845, y=10)
# this is to lower the volume 
    decrease_button = Button(frame, text="🔊-", font=("Arial", 16, "bold"),fg="black", bg="#ffecf6", activebackground="#ffecf6",borderwidth=0, command=decrease_volume)
    decrease_button.place(x=805, y=10)
# this is to turn the music on and off
    volume_button = Button(frame, text="🔊", font=("Arial", 16, "bold"),fg="black", bg="#ffecf6", activebackground="#ffecf6",borderwidth=0, command=toggle_music)
    volume_button.place(x=765, y=10)




pygame.mixer.music.load("sound/bg_audio.mp3")  # this audio is used as a background music which will be played in all frames 
pygame.mixer.music.play(-1)  # this will play the music in loop
#play button voice
play_button = pygame.mixer.Sound("sound/letsgo.mp3") #this sound will be used when the play button is clicked on frame 1
def play_click():
    play_button.play()

#reules button voice 
rules_button = pygame.mixer.Sound("sound/rule.mp3") #this sound will be used when clicked on rules button on frame 2
def rules_click():
    rules_button.play()
#rest all the button voice 
all_button = pygame.mixer.Sound("sound/click.mp3")
def all_click():
    all_button.play()







# ---------------------- Functions for the game quiz ----------------------
def switch_to_frame(frame):
    frame.tkraise() # this brings the given function in front

def set_difficulty(level):
    global difficulty, score, question_no
    difficulty = level #choose the difficulty level(easy,moderate and advanced)
    score = 0 #rest the score for the user 
    question_no = 0 # reset the questions 
    update_score_label() #this will update the score on the screen
    next_question() # this will show the new question
    switch_to_frame(frame5) # move to the quiz screen

def randomInt():
    # Return a random number based on difficulty level
    if difficulty == "easy":
        return random.randint(1, 9)
    elif difficulty == "moderate":
        return random.randint(10, 99)
    elif difficulty == "advanced":
        return random.randint(1000, 9999)
# this will choose  random + and - for the questions 
def decideOperation():
    return random.choice(["+", "-"])

def next_question():
    global num1, num2, operation, answer, question_no, attempt

    if question_no < total_questions:
        question_no += 1 #this will move to the next question
        attempt = 1 # this will reset the attempt count 
        num1 = randomInt() #this will generate the random num for number 1 
        num2 = randomInt() # this will generate random number for mnumber 2 
        operation = decideOperation()

        # avoid negative numbers for subtraction
        if operation == "-" and num2 > num1:
            num1, num2 = num2, num1

        answer = num1 + num2 if operation == "+" else num1 - num2 # this will calculate the correct answer
# in this the question will update and clear the previous feedbacks 
        question_label.config(text=f"Question {question_no} of {total_questions}")
        equation_label.config(text=f"{num1} {operation} {num2} = ?")
        feedback_label.config(text="")
        answer_entry.delete(0, END)
        answer_entry.focus()

    else:
        displayResults() # final score will display when all the questions are answered 

def check_answer():
    global score, attempt
    user_ans = answer_entry.get()
# this will check if the input is numbers 
    try:
        user_ans = int(user_ans)
    except ValueError:
        feedback_label.config(text="Enter a valid number!", fg="red")
        root.after(1000, lambda: feedback_label.config(text=""))
        return
# ✅ Correct answer
    if user_ans == answer:
        if attempt == 1:
            score += 10
            feedback_label.config(text="+10 points! Correct 🎉", fg="green")
        else:
            score += 5
            feedback_label.config(text="+5 points! Correct 🎯", fg="orange")
        update_score_label()
        root.after(1200, next_question)
# ❌ Incorrect answer
    else:
        if attempt == 1:
            feedback_label.config(text="Wrong ❌ Try again!", fg="red")
            attempt += 1
            root.after(1000, lambda: feedback_label.config(text=""))
        else:
            feedback_label.config(text="0 points ❌", fg="red")
            root.after(1200, next_question)

def update_score_label():
    # refresh the score display
    score_label.config(text=f"Score: {score}")

def displayResults():
    global score
# these will be the score and grade based on the questions the user attempts 
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"
# this will show the score and grades
    score_number_label.config(text=f"{score}")
    grade_label.config(text=f"{grade}")
    switch_to_frame(frame6) # this will go to the score frame 
# Update scoreboard text
    score_text_label.config({score})
    switch_to_frame(frame6)

# this will rest the quiz with questions and scores 
def reset_quiz():
    global score, question_no
    score = 0
    question_no = 0
    update_score_label()

# ---------------------- FRAME 1 ----------------------
frame1 = Frame(root, width=900, height=600)
frame1.place(x=0, y=0)
# bg for the frame 1
bg_photo1 = ImageTk.PhotoImage(Image.open("bgimage/page1.jpg").resize((900, 595)))
Label(frame1, image=bg_photo1).place(x=0, y=0)
# button for the frame 1 
button_photo1 = ImageTk.PhotoImage(Image.open("btnimage/button1.png").resize((95, 95)))
Button(frame1, image=button_photo1, borderwidth=0, highlightthickness=0,
    bg=frame1["bg"], activebackground=frame1["bg"],
    command=lambda: [play_click(), switch_to_frame(frame2)]).place(x=430, y=450)

# ---------------------- FRAME 2 ----------------------
frame2 = Frame(root, width=900, height=600)
frame2.place(x=0, y=0)
bg_photo2 = ImageTk.PhotoImage(Image.open("bgimage/page2.jpg").resize((900, 595)))
Label(frame2, image=bg_photo2).place(x=0, y=0)
# button one for frame 2
button_photo2 = ImageTk.PhotoImage(Image.open("btnimage/button2.png").resize((290, 154)))
Button(frame2, image=button_photo2, borderwidth=0, highlightthickness=0,
bg=frame2["bg"], activebackground=frame2["bg"],
    command=lambda: [rules_click(), switch_to_frame(frame3)]).place(x=138, y=191)
# this is the second button for the farme 2 
button_photo2a = ImageTk.PhotoImage(Image.open("btnimage/button2a.png").resize((255, 105)))
Button(frame2, image=button_photo2a, borderwidth=0, highlightthickness=0,
    bg=frame2["bg"], activebackground=frame2["bg"],
    command=lambda: [all_click(), switch_to_frame(frame7)]).place(x=540, y=240)

# ---------------------- FRAME 3 ----------------------
frame3 = Frame(root, width=900, height=600)
frame3.place(x=0, y=0)
bg_photo3 = ImageTk.PhotoImage(Image.open("bgimage/page3.jpg").resize((900, 595)))
Label(frame3, image=bg_photo3).place(x=0, y=0)
# first butotn for the frame 3
button_photo3 = ImageTk.PhotoImage(Image.open("btnimage/buttonn3.png").resize((240, 100)))
Button(frame3, image=button_photo3, borderwidth=0, highlightthickness=0,
    bg=frame3["bg"], activebackground=frame3["bg"],
    command=lambda: [all_click(), switch_to_frame(frame4)]).place(x=380, y=450)
# second button for frame 3
button_photo3a = ImageTk.PhotoImage(Image.open("btnimage/button3a.png").resize((250, 62)))
Button(frame3, image=button_photo3a, borderwidth=0, highlightthickness=0,
    bg=frame3["bg"], activebackground=frame3["bg"],
    command=lambda: [all_click(), switch_to_frame(frame7)]).place(x=630, y=478)

# ---------------------- FRAME 4 (Difficulty Select) ----------------------
frame4 = Frame(root, width=900, height=600)
frame4.place(x=0, y=0)
bg_photo4 = ImageTk.PhotoImage(Image.open("bgimage/page4.jpg").resize((900, 595)))
Label(frame4, image=bg_photo4).place(x=0, y=0)
button_photo4 = ImageTk.PhotoImage(Image.open("btnimage/button4.png").resize((180, 52)))
button_photo4a = ImageTk.PhotoImage(Image.open("btnimage/button4a.png").resize((180, 59)))
button_photo4b = ImageTk.PhotoImage(Image.open("btnimage/button4b.png").resize((190, 60)))

Button(frame4, image=button_photo4, borderwidth=0,highlightthickness=0, bg=frame4["bg"], command=lambda: [all_click(), set_difficulty("easy")]).place(x=120, y=396)
Button(frame4, image=button_photo4a, borderwidth=0,highlightthickness=0, bg=frame4["bg"], command=lambda: [all_click(), set_difficulty("moderate")]).place(x=360, y=390)
Button(frame4, image=button_photo4b, borderwidth=0,highlightthickness=0, bg=frame4["bg"], command=lambda: [all_click(), set_difficulty("advanced")]).place(x=620, y=390)

# ---------------------- FRAME 5 (Quiz) ----------------------
frame5 = Frame(root, width=900, height=600)
frame5.place(x=0, y=0)
bg_photo5 = ImageTk.PhotoImage(Image.open("bgimage/page5.jpg").resize((900, 595)))
Label(frame5, image=bg_photo5).place(x=0, y=0)
# button for easy on frame 5
button_image5 = Image.open("btnimage/button5.png")   
button_image5 = button_image5.resize((150, 90))  
button_photo5 = ImageTk.PhotoImage(button_image5)
circle_button5 = Button(frame5, image=button_photo5, borderwidth=0,highlightthickness=0,
                        bg=frame5["bg"], activebackground=frame5["bg"],
                        command=check_answer)
circle_button5.place(x=330, y=349)
# button for moderate on frame 5
button_image5a = Image.open("btnimage/button5a.png")   # Your circular image file
button_image5a = button_image5a.resize((141, 45))   # Resize if needed
button_photo5a = ImageTk.PhotoImage(button_image5a)

circle_button5a = Button(frame5, image=button_photo5a, borderwidth=0, highlightthickness=0,
                    bg=frame5["bg"], activebackground=frame5["bg"],
                    command=lambda: [all_click(), switch_to_frame(frame7)])
circle_button5a.place(x=600, y=380)



# label to show the current question num
question_label = Label(frame5, text="Question 1 of 10", font=("Arial", 20), bg="#e5e4da")
question_label.place(x=450, y=140)
#label to show the math equation
equation_label = Label(frame5, font=("Arial", 40), bg="#e5e4da")
equation_label.place(x=375, y=220)
# entry box for user to write their answers 
answer_entry = Entry(frame5, font=("Arial", 20))
answer_entry.place(x=350, y=280, width=200)
# label to show the feedback for wrong and corect ans
feedback_label = Label(frame5, text="", font=("Arial", 16), bg="#e5e4da")
feedback_label.place(x=350, y=330)
# label to display the score 
score_label = Label(frame5, text="Score: 0", font=("Arial", 16), bg="#e5e4da")
score_label.place(x=350, y=100)

# ---------------------- FRAME 6 (Scoreboard) ----------------------
frame6 = Frame(root, width=900, height=600)
frame6.place(x=0, y=0)
bg_photo6 = ImageTk.PhotoImage(Image.open("bgimage/page6.jpg").resize((900, 595)))
Label(frame6, image=bg_photo6).place(x=0, y=0)

#score label
score_number_label = Label(frame6, text="", font=("Arial", 20, "bold"), bg="#e8f0ff")
score_number_label.place(x=515, y=205)

# Grade label 
grade_label = Label(frame6, text="", font=("Arial", 38, "bold"), bg="#E6F2E8", fg="#000000")
grade_label.place(x=560, y=90)

button_image6 = Image.open("btnimage/button6.png")    
button_image6 = button_image6.resize((135, 55))   
button_photo6 = ImageTk.PhotoImage(button_image6)

circle_button6 = Button(frame6, image=button_photo6, borderwidth=0, highlightthickness=0,
                    bg=frame6["bg"], activebackground=frame6["bg"],
                    command=lambda: [all_click(), switch_to_frame(frame4)])
circle_button6.place(x=290, y=264)
#second button for pg6
button_image6a = Image.open("btnimage/button6a.png")   
button_image6a = button_image6a.resize((140, 35))   
button_photo6a = ImageTk.PhotoImage(button_image6a)

circle_button6a = Button(frame6, image=button_photo6a, borderwidth=0, highlightthickness=0,
                    bg=frame6["bg"], activebackground=frame6["bg"],
                    command=lambda: [all_click(), switch_to_frame(frame7)])
circle_button6a.place(x=480, y=280)


# ---------------------- FRAME 7 (Play Again Yes/No) ----------------------
frame7 = Frame(root, width=900, height=600)
frame7.place(x=0, y=0)
bg_photo7 = ImageTk.PhotoImage(Image.open("bgimage/page7.jpg").resize((900, 595)))
Label(frame7, image=bg_photo7).place(x=0, y=0)

button_image7 = Image.open("btnimage/button7.png")
button_image7 = button_image7.resize((68, 82))  
button_photo7 = ImageTk.PhotoImage(button_image7)

circle_button7 = Button(frame7, image=button_photo7, borderwidth=0, highlightthickness=0,
                    bg=frame7["bg"], activebackground=frame7["bg"],
                    command= root.destroy)
circle_button7.place(x=182, y=445)
#second button on pag 7
button_image7a = Image.open("btnimage/button7a.png")
button_image7a = button_image7a.resize((72, 80)) 
button_photo7a = ImageTk.PhotoImage(button_image7a)

circle_button7a = Button(frame7, image=button_photo7a, borderwidth=0, highlightthickness=0,
                    bg=frame7["bg"], activebackground=frame7["bg"],
                    command=lambda: [all_click(), switch_to_frame(frame1)])
circle_button7a.place(x=610, y=380)
# to add volume button on all the frames
for f in [frame1, frame2, frame3, frame4, frame5, frame6, frame7]:
    add_volume_buttons(f)

# ---------------------- Start ----------------------
switch_to_frame(frame1)
root.mainloop()