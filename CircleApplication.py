from tkinter import *
from tkinter import ttk
import random 
from time import time
import tkinter
import pandas as pd

#class DataHandler():  
    # Create CSV File and add data and then once it is full, navigate to Excel and add file path to open and access 'database'
    # When user completes the demographic questions, add results to excel spread
    # Similarly when they have completed their trials of clicking, add those results to the excel spread 


# Included under Questions Page 
class Participants(): 
    def __init__(self):
        self.id = None
        self.age = None # Add condition for partipants to be at least 18 or older 
        self.gender = None
        self.dominance = None # handedness

# Main Window 
class Application(Tk): 
    def __init__(self): 
        Tk.__init__(self)
        self._frame = None
        self.configureApp()
        self.changePage(ConsentPage)
    
    def configureApp(self): 
        """Configuration of Application"""
        self.attributes("-fullscreen", False) # Application begins windowed format
        self.resizable(width=False, height=False) # Restrict resizability
        self.maxsize(1000, 1000)
        self.title("Fitts' Law")

    def changePage(self, frame_class, id=None):
        """Switch to new page by destroying the previous frame and replacing it to a new one"""
        if id is not None:
            new_frame = frame_class(self, id=id)
        else:
            new_frame = frame_class(self)
        if self._frame is not None: 
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

    
# Main Page of Application
class ConsentPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        labelConsent = Label(self, text = "The following research application is being conducted by J Nguyen in the CSET Department with the guidance of Dr. Salivia Guario.\n"
                    "The application is to evaluate and analyze the results following the Law of Fitts. The law is a predictive model of human movement \n"
                    "primarily used in human-computer interaction and ergonomics. Participants are expected to click the randomly generated circles \n"
                    "accurately and precisely within 32 trials. The data recorded will be stored into a database and be included in a report based on \n"
                    "the demographic responses. The completion time will be between 5 to 10 minutes.")
        
        labelConsent.config(font=('Raleway', 12))
        labelConsent.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def clickAgree():
            master.changePage(QuestionPage)

        mb_agree = Button(self, text="I Agree", relief=RAISED, command=clickAgree) # Add command Agree 
        mb_agree.menu = Menu(mb_agree, tearoff=0)
        mb_agree.grid(row=1, column=0)
            
        def clickDisagree(): 
            self.quit()

        mb_disagree = Button(self, text="I Decline", relief=RAISED, command=clickDisagree)
        mb_disagree.menu = Menu(mb_disagree, tearoff=0)
        mb_disagree.grid()
        self.rowconfigure(2, minsize=100, weight=6)



# List of questions in one page and must be required fields before proceeding 
class QuestionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        question1 = Label(self, text="Age?")
        question1Entry = Entry(self)
        question2 = Label(self, text="Gender?")
        question2Entry = Entry(self)
        question3 = Label(self, text="Handedness?")
        question3Radio = Radiobutton(self)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def Submit():
            master.changePage(InstructionPage)

        mb_submit = Button(self, text="Submit", relief=RAISED, command=Submit)
        mb_submit.menu = Menu(mb_submit, tearoff=0)
        mb_submit.grid()
        self.rowconfigure(2, minsize=100, weight=6)


    #def requirement():
        


    # Pseudocode
    # if (agreeButtonClicked): 
    # Display CirclePage 
    # Begin trials and have Timer begin when user clicks on the Circle
    # Once trials are done
    # Navigate to ResultPage with a button or within a condition the trials are complete 

    # Proceed with Instructions Page 

class InstructionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        labelInstruction = Message(self, text = "Instructions\n\n\n" + 
                        "Green circles will randomly generate within the screen." +
                        " Each circle must be clicked in order to proceed, and will be done 32 times." + 
                        " Any misclicks outside of the circles will effect the performance results." +
                        " Progress will be visibly displayed on the top of the screen.")
        labelInstruction.config(font=18, relief=SOLID)
        labelInstruction.grid(padx=50, pady=25)

class Circle: 
    def __init__(self, parent, canvas, id): 
        self.parent = parent
        self.canvas = canvas
        self.id = id 

# Colored circle for user to click (32 count)
class CirclePage: 
    def __init__(self, root, canvas, color, width, height, id):
        pass
    def generateCircle(canvas): 
        canvas.circle(110, 10, 210, 110, outline = "BLACK", fill = "GREEN", width = 2)
        canvas.grid()
        
        # canvas.bind('<B1-Motion>', handler)
        coordinates = []
    # Generate random coordinates for the circles to be placed 

# After partipants completed trials, populate results and close application 
# Store the data into the database from this current page similarly to when partipants answer the demographic questions to begin trials
class ResultPage(Frame): 
    def __init__(self, master=None)
        Frame.__init__(self, master)

    # May delete later if not utilized (optional page)

class ThankPage(Frame):
    def __init__(self, master=None): 
        Frame.__init__(self, master)
        labelthankyou = Label(self, text= "Thank You!\n" + "All tasks have been completed and data has been collected.")
        labelthankyou.config(font=18, relief=SOLID)
        labelthankyou.grid(padx=50, pady=25)

        # Testing - Results will populate for that specific participant and the data collected will be added onto the database (csv file) < loop
        df = pd.read_csv('Fitts_Data.csv')
        print(df)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

