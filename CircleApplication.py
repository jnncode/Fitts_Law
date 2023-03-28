from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import tkinter
import time
import pandas 
import random  
import csv

class DataHandler():  
    with open('Fitts_Data.csv', 'a', newline='') as file:
        write = csv.writer(file)
        data = [] # write data 
        # add condition of when user is done with the questions page, record the answers and proceed to the instructions page 
        write.writerow(data)

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
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Raleway", size=12)
    
    def configureApp(self): 
        """Configuration of application"""
        self.attributes("-fullscreen", False) # Application begins windowed format
        self.resizable(width=False, height=False) # Restrict resizability
        self.geometry("1000x800")
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
        assert isinstance(Canvas, tkinter.Canvas)
        Frame.__init__(self, master)

        labelConsent = Label(self, text = "Consent Form\n\n\nThe following research application is being conducted by J Nguyen in the CSET Department with the guidance of Dr. Salivia Guario.\n"
                    "The application is to evaluate and analyze the results following the Law of Fitts. The law is a predictive model of human movement \n"
                    "primarily used in human-computer interaction and ergonomics. Participants are expected to click the randomly generated circles \n"
                    "accurately and precisely within 32 trials. The data recorded will be stored into a database and be included in a report based on \n"
                    "the demographic responses. The completion time will be between 5 to 10 minutes.")
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
        Frame.__init__(self, master)  # add padding to the frame

        question1 = Label(self, text="Age?").grid(row=1, column=1, sticky="nsew")  
        question1Entry = Entry(self)
        question1Entry.grid(row=2, column=1, sticky="nsew")  

        question2 = Label(self, text="Gender?").grid(row=3, column=1, sticky="nsew")  
        question2Entry = Entry(self)
        question2Entry.grid(row=4, column=1, sticky="nsew") 


        question3 = Label(self, text="Handedness?").grid(row=5, column=1, sticky="nsew")  
        question3Entry = Entry(self)
        question3Entry.grid(row=6, column=1, sticky="nsew")

        self.columnconfigure(0, minsize=450, weight=1)
        self.rowconfigure(0, minsize=400, weight=1)

        def validate():
            # Check if age is valid
            try:
                value = int(question1Entry.get())
                if value < 0 or value > 100:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter valid age between 0 and 100.")
                return False

            # Check if gender is filled and valid
            gender = question2Entry.get().strip().casefold()
            if gender not in ["male", "female", "other"]:
                messagebox.showerror("Error", "Please enter valid gender (male, female, or other).")
                return False

            # Check if handedness is selected
            handedness = question3Entry.get().strip().casefold()
            if handedness not in ["left", "right"]:
                messagebox.showerror("Error", "Please enter valid handedness (left or right).")
                return False

            # If all fields have been filled
            return True


        def clickSubmit():
            if validate():
                master.changePage(InstructionPage)
            else:
                messagebox.showerror("Error", "Please fill out all required fields before submitting.")

        # Disable the submit button by default
        mb_submit = Button(self, text="Submit", command=clickSubmit)
        mb_submit.menu = Menu(mb_submit, tearoff=0)
        mb_submit.grid(row=7, column=1, sticky="nsew")

    # Pseudocode
    # Display CirclePage 
    # Begin trials and have Timer begin when user clicks on the Circle
    # Once trials are done
    # Navigate to ResultPage with a button or within a condition the trials are complete 

class InstructionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        labelInstruction = Message(self, text = "Instructions\n\n\n" + 
                        "Green circles will randomly generate within the screen." +
                        " Each circle must be clicked in order to proceed, and will be done 32 times." + 
                        " Any misclicks outside of the circles will effect the performance results." +
                        " Progress will be visibly displayed on the top of the screen.")
        labelInstruction.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def begin():
            master.changePage(CirclePage)

        mb_begin = Button(self, text="Begin", relief=RAISED, command=begin) # Add command Agree 
        mb_begin.menu = Menu(mb_begin, tearoff=0)
        mb_begin.grid(row=1, column=0)

# Colored circle for user to click (32 count)
class CirclePage(Frame): 
    def __init__(self, canvas, master=None):
        Frame.__init__(self, master)
        self.canvas = canvas
        self.circleRadius = 20  
        self.numberOfCircles = 32  
        self.circles = []

        for i in range(self.numberOfCircles):
            circle_x = random.randint(self.circleRadius, self.canvas.winfo_width() - self.circleRadius)
            circle_y = random.randint(self.circleRadius, self.canvas.winfo_height() - self.circleRadius)
            circle = {
                "x": circle_x,
                "y": circle_y,
                "radius": self.circleRadius,
                "clicks": 0
            }
            self.canvas.create_oval(circle_x-self.circleRadius, circle_y-self.circleRadius,
                                circle_x+self.circleRadius, circle_y+self.circleRadius, fill="blue")
            self.circles.append(circle)

        # Track clicks
        def clickCircle(event):
            for circle in self.circles:
                if ((event.x - circle["x"])**2 + (event.y - circle["y"])**2) <= circle["radius"]**2:
                    circle["clicks"] += 1
                    if circle["clicks"] >= self.numberOfCircles:
                        self.canvas.delete("all")
                        self.circles.remove(circle)
                        for remainingCircle in self.circles:
                            self.canvas.create_oval(remainingCircle["x"]-remainingCircle["radius"],
                                                remainingCircle["y"]-remainingCircle["radius"],
                                                remainingCircle["x"]+remainingCircle["radius"],
                                                remainingCircle["y"]+remainingCircle["radius"],
                                                fill="blue")
                        self.canvas.bind("<Button-1>", clickCircle) 
                        if len(self.circles) == 0:
                            self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, text="Complete")
                            self.unbind("<Button-1>")
                            break
        self.canvas.bind("<Button-1>", clickCircle) 



# After partipants completed trials, populate results and close application 
# Store the data into the database from this current page similarly to when partipants answer the demographic questions to begin trials
class ResultPage(Frame): 
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # Testing - Results will populate for that specific participant and the data collected will be added onto the database (csv file) 
        df = pandas.read_csv('Fitts_Data.csv')
        print(df)

class ThankPage(Frame):
    def __init__(self, master=None): 
        Frame.__init__(self, master)
        labelthankyou = Label(self, text= "Thank You!\n" + "All tasks have been completed and data has been collected.")
        labelthankyou.config(font=18, relief=SOLID)
        labelthankyou.grid(padx=50, pady=25)

        def Close():
            app.quit()

        mb_close = Button(text="Quit", command=Close).grid()



if __name__ == "__main__":
    app = Application()
    app.mainloop()

