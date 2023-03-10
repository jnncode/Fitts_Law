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

root.geometry("800x800")
root.title("Fitts' Law")

class ConsentPage():
    title = StringVar() 
    labelTitle = Message(root, textvariable=title)

    title.set("Consent Form")
    labelTitle.config(font=25, justify=CENTER)
    labelTitle.pack(pady=50)

    consent = StringVar() 
    labelConsent = Message(root, textvariable=consent)
    consent.set("The following research application is being conducted by J Nguyen in the CSET Department with the guidance of Dr. Salivia Guario." + 
     "\nThe application is to evaluate and analyze the results following the Law of Fitts. The law is a predictive model of human movement primarily used in human-computer interaction and ergonomics." 
     + "\nParticipants are expected to click the randomly generated circles accurately and precisely with 32 trials. The data recorded will be stored into a database and be included in a report based "
     + "on the dempgraphic responses.")
    labelConsent.config(font=18, relief=SOLID)
    labelConsent.pack(padx=50, pady=25)

    mb_agree = Button(root, text="I Agree", relief=RAISED) # add command Agree 
    mb_agree.menu = Menu(mb_agree, tearoff=0)
    mb_agree.pack()


    # def clickAgree():
    #     root.destroy()
    #     import QuestionPage
        
    def clickDisagree(): 
        root.quit()

    mb_disagree = Button(root, text="I Decline", relief=RAISED, command=clickDisagree)
    mb_disagree.menu = Menu(mb_disagree, tearoff=0)
    mb_disagree.pack()

root.mainloop()


