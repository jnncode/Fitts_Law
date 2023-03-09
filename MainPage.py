# Execute any and all components (elements) by calling the methods 

# Main Page will include the Window Panel and have an automatic separate window pop-up to occur of the conset form

# Another panel similarly to the conset form of the demographic questions
# Age 
# Sex - Female, Male
# Gender - Social Construct 

import tkinter 
from tkinter import *
from tkinter import ttk
root = tkinter.Tk() 

root.geometry("750x750")
root.title("Fitts' Law")

class ConsentPage():
    var = StringVar() 
    label = Message(root, textvariable=var, relief=RAISED)

    var.set("Consent Form")

    mb_agree = Menubutton (root, text="I Agree", relief=RAISED)
    mb_agree.menu = Menu(mb_agree, tearoff=0)
    # mb_agree.pack(side=LEFT)
    mb_agree.pack()

    mb_disagree = Menubutton(root, text="I Decline", relief=RAISED)
    mb_disagree.menu = Menu(mb_disagree, tearoff=0)
    # mb_disagree.pack(side=RIGHT)
    mb_disagree.pack()

class QuestionsPage():
    var = StringVar()
    label = Message(root, textvariable=var, relief=RAISED)
    var.set("Questions")

    # List of questions in one page and must be required fields before proceeding 



root.mainloop()


