from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter as tk
import time
import pandas
import random
import csv


# Main Window
class Application(tk.Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.configureApp()
        self.changePage(ConsentPage)
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Raleway", size=12)

    def configureApp(self):
        """Configuration of application"""
        self.attributes("-fullscreen", False)  # Application begins windowed format
        self.resizable(width=False, height=False)  # Restrict resizability
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
        Frame.__init__(self, master)

        label_consent = Label(self,
        text=
        """
        Consent Form
        
        The following research application is being conducted by J Nguyen in the CSET Department with the guidance of Dr. Salivia Guario.
        The application is to evaluate and analyze the results following the Law of Fitts. The law is a predictive model of human movement
        primarily used in human-computer interaction and ergonomics. Participants are expected to click the randomly generated circles
        accurately and precisely within 32 trials. The data recorded will be stored into a database and be included in a report based on
        the demographic responses. The completion time will be between 5 to 10 minutes.""")

        label_consent.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def clickAgree():
            master.changePage(QuestionPage)

        mb_agree = Button(self, text="I Agree", relief=RAISED, command=clickAgree)  # Add command Agree
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

        def generateId():
            global participant_count
            participant_count = 0
            id = f'P{participant_count + 1:04d}'
            participant_count += 1
            return id

        generate_id = generateId()

        id_label = Label(self, text=f"ID: {generate_id}")
        id_label.grid(row=1, column=1, sticky="nsew")

        age_label = Label(self, text="Age")
        age_label.grid(row=2, column=1, sticky="nsew")

        age_entry = Entry(self)
        age_entry.grid(row=3, column=1, sticky="nsew")

        gender = Label(self, text="Gender")
        gender.grid(row=4, column=1, sticky="nsew")

        gender_entry = Entry(self)
        gender_entry.grid(row=5, column=1, sticky="nsew")

        hand_label = Label(self, text="Handedness")
        hand_label.grid(row=6, column=1, sticky="nsew")

        hand_entry = Entry(self)
        hand_entry.grid(row=7, column=1, sticky="nsew")

        self.columnconfigure(0, minsize=450, weight=1)
        self.rowconfigure(0, minsize=400, weight=1)

        def validate():
            # Check if age is valid
            try:
                value1 = int(age_entry.get())
                if value1 < 0 or value1 > 100:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter valid age between 0 and 100.")
                return False

            # Check if gender is filled and valid
            gender = gender_entry.get().strip().casefold()
            if gender not in ["male", "female", "other"]:
                messagebox.showerror("Error", "Please enter valid gender (male, female, or other).")
                return False

            # Check if handedness is selected
            handedness = hand_entry.get().strip().casefold()
            if handedness not in ["left", "right", "l", "r"]:
                messagebox.showerror("Error", "Please enter valid handedness (left or right).")
                return False

            # If all fields have been filled
            return True

        def clickSubmit():
            age = age_entry.get()
            gender = gender_entry.get()
            hand = hand_entry.get()

            # Store the data in CSV file (database)
            with open('Fitts_Data.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id, age, gender, hand])

            if validate():
                # messagebox.showinfo("Submitted.\nThank You!")
                master.changePage(InstructionPage)
            else:
                messagebox.showerror("Error", "Please fill out all required fields before submitting.")

        # Disable the submit button by default
        mb_submit = Button(self, text="Submit", command=clickSubmit)
        mb_submit.menu = Menu(mb_submit, tearoff=0)
        mb_submit.grid(row=8, column=1, sticky="nsew")

    # Pseudocode
    # Display CirclePage 
    # Begin trials and have Timer begin when user clicks on the Circle
    # Once trials are done
    # Navigate to ResultPage with a button or within a condition the trials are complete 


class InstructionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        label_instruction = Message(
            self,
            text=
                "Instructions\n\n\n" +
               "Green circles will randomly generate within the screen." +
               " Each circle must be clicked in order to proceed, and will be done 32 times." +
               " Any misclicks outside of the circles will effect the performance results." +
               " Progress will be visibly displayed on the top of the screen."
        )
        label_instruction.grid(row=0, column=0)

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def begin():
            master.changePage(CirclePage)  # CirclePage - Commented due to Error

        mb_begin = Button(self, text="Begin", relief=RAISED, command=begin)  # Add command Agree
        mb_begin.menu = Menu(mb_begin, tearoff=0)
        mb_begin.grid(row=1, column=0)


# Colored circle for user to click (32 count) - ERROR FIX SOON
class CirclePage(Frame):
    def __init__(self, canvas, master=None):
        Frame.__init__(self, master)
        # Check canvas object is tkinter.Canvas object

        self.canvas = Canvas(master)
        if not isinstance(self.canvas, tk.Canvas):
            raise TypeError("canvas must be a tkinter.Canvas object")
        self.circle_radius = 20
        self.number_of_circles = 32
        self.circles = []

        # Initialize the click counter and the list of click intervals
        click_count = 0
        click_intervals = []

        # Define a function to handle a click on a circle
        def handle_click(event):
            nonlocal click_count, click_intervals
            click_count += 1
            click_intervals.append(time.time() - start_time)
            canvas.delete(event.widget)
            if click_count == self.number_of_circles:
                end_time = time.time()
                print("Total Time: {:.2f} seconds".format(end_time - start_time))
                print("Click Intervals:", click_intervals)
                self.destroy()

        # Generate the circles
        for i in range(self.number_of_circles):
            x = random.randint(self.circle_radius, self.canvas.winfo_width() - self.circle_radius)
            y = random.randint(self.circle_radius, self.canvas.winfo_height() - self.circle_radius)
            circle = tk.Canvas.create_oval(x - self.circle_radius, y - self.circle_radius, x + self.circle_radius, y + self.circle_radius, fill="green")
            canvas.tag_bind(circle, "<Button-1>", handle_click)
            self.circles.append(circle)
        # Start the timer
        start_time = time.time()


# After participants completed trials, populate results and close application
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
        label_thank_you = Label(self,
                                text="Thank You!\n" + "All tasks have been completed and data has been collected.")
        label_thank_you.config(font=18, relief=SOLID)
        label_thank_you.grid(padx=50, pady=25)

        def Close():
            app.quit()

        mb_close = Button(text="Quit", command=Close).grid()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
