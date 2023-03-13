from tkinter import *
from tkinter import ttk
import random 
from time import time 


#class DataHandler():  
    # Create CSV File and add data and then once it is full, navigate to Excel and add file path to open and access 'database'
    # When user completes the demographic questions, add results to excel spread
    # Similarly when they have completed their trials of clicking, add those results to the excel spread 


# Included under Questions Page 
class Participants(): 
    def __init__(self):
        self.id = None
        self.age = None
        self.gender = None
        self.dominance = None # handedness

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
        self.maxsize(800, 800)
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
        self._frame.pack()

    
# Main Page of Application
class ConsentPage(Frame):
    def __init__(self, master=None):
        frame = Frame.__init__(self, master)
       
        title = StringVar() 
        labelTitle = Message(self, textvariable=title)

        title.set("Consent Form")
        labelTitle.config(font=25, justify=CENTER)
        labelTitle.pack(pady=50)

        consent = StringVar() 
        labelConsent = Message(self, textvariable=consent)
        consent.set("The following research application is being conducted by J Nguyen in the CSET Department with the guidance of Dr. Salivia Guario.\n" +
                    "The application is to evaluate and analyze the results following the Law of Fitts. The law is a predictive model of human movement" +
                    " primarily used in human-computer interaction and ergonomics. Participants are expected to click the randomly generated circles" +
                    " accurately and precisely within 32 trials. The data recorded will be stored into a database and be included in a report based on" +
                    " the demographic responses. The completion time will be between 5 to 10 minutes.")
        labelConsent.config(font=18, relief=SOLID)
        labelConsent.pack(padx=50, pady=25)

        def clickAgree():
            master.changePage(QuestionPage)

        mb_agree = Button(self, text="I Agree", relief=RAISED, command=clickAgree) # Add command Agree 
        mb_agree.menu = Menu(mb_agree, tearoff=0)
        mb_agree.pack()
            
        def clickDisagree(): 
            self.quit()

        mb_disagree = Button(self, text="I Decline", relief=RAISED, command=clickDisagree)
        mb_disagree.menu = Menu(mb_disagree, tearoff=0)
        mb_disagree.pack()


# List of questions in one page and must be required fields before proceeding 
class QuestionPage(Frame):
    def __init__(self, master=None):
        frame = Frame.__init__(self, master)

        question1 = Label(self, text="Age?")
        question1Entry = Entry(self)
        question2 = Label(self, text="Gender?")
        question2Entry = Entry(self)
        question3 = Label(self, text="Handedness?")
        question3Radio = Radiobutton(self)

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
        frame = Frame.__init__(self, master)
        instruction = StringVar() 
        labelInstruction = Message(self, textvariable=instruction)
        instruction.set("Instructions\n\n\n" + 
                        "Green circles will randomly generate within the screen." +
                        " Each circle must be clicked in order to proceed, and will be done 32 times." + 
                        " Any misclicks outside of the circles will effect the performance results." +
                        " Progress will be visibly displayed on the top of the screen.")
        labelInstruction.config(font=18, relief=SOLID)
        labelInstruction.pack(padx=50, pady=25)

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
        canvas.pack()
        
        # canvas.bind('<B1-Motion>', handler)
        coordinates = []
    # Generate random coordinates for the circles to be placed 

# After partipants completed trials, populate results and close application 
# Store the data into the database from this current page similarly to when partipants answer the demographic questions to begin trials
class ResultPage(Frame): 
    pass
    # May delete later if not utilized (optional page)

class ThankPage(Frame):
    def __init__(self, master=None): 
        frame = Frame.__init__(self, master)
        thankyou = StringVar()
        labelthankyou = Message(self, textvariable=thankyou)
        thankyou.set("Thank You!\n" + "All tasks have been completed and data has been collected.")
        labelthankyou.config(font=18, relief=SOLID)
        labelthankyou.pack(padx=50, pady=25)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

