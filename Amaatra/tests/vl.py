from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
import pandas as pd
import os
import sys



#global for vinelad
yes =0
no=0
might=0
basal_age=0
vli=0
index_arr = [0] * 90
agetoadd = 0
age_range = {6:[45,65],7:[51,70],8:[57,74],9:[62,77]}
cage = 6
vlf = age_range[cage][1]


class Question:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers
        global vli
        vli = 0

    def check(self, letter, view):
        global yes
        global no
        global might
        global basal_age
        global index_arr
        global vli
        global vlf
        global agetoadd
        agemap = {0:0.7, 34:1.2, 44:2, 56:2.4, 61:3, 65:2.4, 70:3, 74:4, 77:3}
        for (k, v) in agemap.items():
            if vli == k:
                agetoadd = v

        if(letter == "A"):
            label = Label(view, text="Yes")
            yes += 1
            basal_age+=agetoadd
            vli += 1
            index_arr[vli] = 1
        elif(letter == "B"):
            label = Label(view, text="No")
            no +=1
            vli += 1
            index_arr[vli] = 0
        else:
            label = Label(view, text="Could have passed")
            might +=1
            basal_age += agetoadd/2.0
            vli += 1
            index_arr[vli] = 2

        if (index_arr[vli]==1 and index_arr[(vli)-2]==1 and index_arr[(vli)-1]==2):
            current=self.mapmaybeage(vli)
            previous=self.mapmaybeage(vli-1)
            if current == previous:
                basal_age += agetoadd/2.0
            else:
                basal_age+= agemap[previous]/2.0
        print("current basal age is ")
        print(basal_age, " months")

        label.pack()
        view.after(1, lambda *args: self.unpackView(view))

    def mapmaybeage(self,vli):
        if vli < 34:
            return 0
        elif vli<44:
            return 34
        elif vli<56:
            return 44
        elif vli<61:
            return 56
        elif vli<65:
            return 61
        elif vli<70:
            return 65
        elif vli<74:
            return 70
        elif vli<77:
            return 74
        elif vli<81:
            return 77



    def getView(self, window):
        view = Frame(window)
        Label(view, text=self.question).pack()
        Button(view, text=self.answers[0], command=lambda *args: self.check("A", view),width=50).pack()
        Button(view, text=self.answers[1], command=lambda *args: self.check("B", view),width=50).pack()
        Button(view, text=self.answers[2], command=lambda *args: self.check("C", view),width=50).pack()

        return view

    def unpackView(self, view):
        view.pack_forget()
        askQuestion()

def askQuestion():
    global questions, window, button, yes, no,might, number_of_questions,social_quotient,index_arr,vlf,vli
    if(vli == vlf):
        Label(window,text="Thank you for answering the questions.\n basal_age = " + str(basal_age)).pack()
        global cage
        social_quotient=(basal_age/(cage*12))*100#chrono age taken as 10 as all question included are till 9-10 yearsold
        Label(window, text="social quotient = " + str(social_quotient)).pack()
        if(social_quotient<20):
            ID = True
            Label(window, text="Profound Intelletual disability").pack()
        elif((social_quotient>=20) and(social_quotient<35)):
            ID = True
            Label(window, text="Severe Intelletual disability").pack()
        elif((social_quotient>=35) and (social_quotient<50)):
            ID = True
            Label(window, text="Moderate Intelletual disability").pack()
        elif((social_quotient>=50) and (social_quotient<70)):
            ID = True
            Label(window, text="Mild Intelletual disability").pack()
        else:
            ID = False
            Label(window, text="Normal IQ").pack()
            window.configure(background='spring green')
        if ID==True:
            window.configure(background='firebrick2')
        buttonn = Button(window,text="Next",command=quitf)
        buttonn.pack(side=BOTTOM)
        returnval = float(social_quotient) #TODO: create func to return the val
        return
    button.pack_forget()
    label_des.pack_forget()
    questions[vli].getView(window).pack()

def quitf():
    pass
    #TODO: Call result display.

questions = []
filepath=os.path.dirname(os.path.abspath(__file__))
file = open(filepath+"/VL/vineland2questions.txt", "r",encoding='windows-1252')
line = file.readline()
while(line != ""):
    questionString = line
    answers = []
    for vli in range (3):
        answers.append(file.readline())

    questions.append(Question(questionString, answers))
    line = file.readline()
file.close()

number_of_questions = len(questions)


window = Tk()
w = 600
h = 300
# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))
label_heading = Label(window, text="VINELAND SOCIAL MATURITY TEST",bg="black",fg="white",font=('Helvetica', '20'))
label_heading.pack()
label_des = Label(window, text="\n\nThe Vineland Social Maturity Scale (VSMS) measures the differential social\ncapacities of an individual. It provides an estimate of Social Age (SA) and Social\nQuotient (SQ), and shows high correlation (0.80) with intelligence. It is designed to\nmeasure social maturation in eight social areas: Self-help General (SHG), Self-help\nEating (SHE), Self-help Dressing (SHD), Self direction (SD), Occupation (OCC),\nCommunication (COM), Locomotion (LOM), and Socialization (SOC).",fg="blue",font=('15'))
label_des.pack()
button = Button(window, text="Start", command=askQuestion)
button.pack()
window.mainloop()