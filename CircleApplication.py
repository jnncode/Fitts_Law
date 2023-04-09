from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter as tk
import time
import pandas
import random
import csv
import pandas 
import math

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

        label_consent.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def clickAgree():
            master.changePage(QuestionPage)

        mb_agree = Button(self, text="I Agree", relief=RAISED,  width=7, height=1, command=clickAgree)
        mb_agree.menu = Menu(mb_agree, tearoff=0)
        mb_agree.grid(row=1, column=0, sticky="ns", pady=8)

        def clickDisagree():
            self.quit()

        mb_disagree = Button(self, text="I Decline", relief=RAISED, width=7, height=1, command=clickDisagree)
        mb_disagree.menu = Menu(mb_disagree, tearoff=0)
        mb_disagree.grid(row=2, column=0, sticky="ns", pady=8)

# Lists ID, Age, Gender, and Handedness then transfers the information into the CSV file
# Clear all data before beginning trials to keep CSV accurate and consistent12
class QuestionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)  # add padding to the frame
        
        # define participant_count and call countIntervals to initialize
        global participant_count
        participant_count = 0

        def countIntervals():
            try:
                with open("Fitts_Data.csv", "r", newline="") as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                    global participant_count, generated_ids
                    if len(rows) > 0:
                        last_id = rows[-1]
                        if last_id and len(last_id) == 6 and last_id.startswith("P") and last_id[1:].isdigit():
                            participant_count = int(last_id[1:])
                        else:
                            participant_count = 0
                        generated_ids = list(set([row[0] for row in rows if row and len(row) >= 1]))
                    else:
                        participant_count = 0
                        generated_ids = []
            except FileNotFoundError:
                participant_count = 0
                generated_ids = []
        
        def generateId():
            """Generates Participant ID"""
            countIntervals()
            global participant_count, generated_ids
            participant_count += 1 # Begin with P0001 
            new_id = f"P{participant_count:04d}"
            while new_id in generated_ids: 
                participant_count += 1
                new_id = f"P{participant_count:04d}"
            return new_id 
        
        countIntervals()  # call the function to set the participant_count initially
        
        def removeSpaces(data_file):
            with open(data_file, "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
            # remove spaces from each cell in each row
            for row in rows: 
                for i in range(len(row)):
                    row[i] = row[i].strip()
            # write cleaned rows back to CSV file 
            with open(data_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

        def clickSubmit():
            """Transfers information into CSV"""
            if not validate():
                return

            age = age_entry.get()
            gender = gender_entry.get()
            hand = hand_entry.get()

            new_id = generateId() # generate a new ID each time the user submits for next user

            # Store the data in CSV file (database)
            with open("Fitts_Data.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Check if the file is empty
                    old_row = writer.writerow(["ID", "Age", "Gender", "Hand"])  # Write headers
                writer.writerow([new_id, age, gender, hand])
            removeSpaces("Fitts_Data.csv")
            if validate():
                master.changePage(InstructionPage)
            else:
                messagebox.showerror("Error", "Please fill out all required fields before submitting.")
        
        new_id = generateId()
        id_label = Label(self, text=f"ID: {new_id}")
        id_label.grid(row=1, column=1, sticky="nsew")

        age_label = Label(self, text="Age")
        age_label.grid(row=2, column=1, sticky="nsew")

        age_entry = Entry(self)
        age_entry.grid(row=3, column=1, sticky="nsew")

        gender_label = Label(self, text="Gender")
        gender_label.grid(row=4, column=1, sticky="nsew")

        gender_entry = Entry(self)
        gender_entry.grid(row=5, column=1, sticky="nsew")

        hand_label = Label(self, text="Handedness")
        hand_label.grid(row=6, column=1, sticky="nsew")

        hand_entry = Entry(self)
        hand_entry.grid(row=7, column=1, sticky="nsew")

        self.columnconfigure(0, minsize=450, weight=1)
        self.rowconfigure(0, minsize=400, weight=1)

        def validate():
            """Validates the answers of questions"""
            # Check if age is filled and valid
            try:
                value = int(age_entry.get())
                if value < 18 or value > 100 or not age_entry.get():
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter valid age between 18 and 100 (must be 18 or older).")
                return False

            # Check if gender is filled and valid
            gender = gender_entry.get().strip().casefold()
            if gender not in ["male", "female", "other"] or not gender_entry.get():
                messagebox.showerror("Error", "Please enter valid gender (male, female, or other).")
                return False

            # Check if handedness is filled and valid
            handedness = hand_entry.get().strip().casefold()
            if handedness not in ["left", "right"] or not hand_entry.get():
                messagebox.showerror("Error", "Please enter valid handedness (left or right).")
                return False

            # If all fields have been filled
            return True

        # Disable the submit button by default
        mb_submit = Button(self, text="Submit", width=7, height=1, command=clickSubmit)
        mb_submit.menu = Menu(mb_submit, tearoff=0)
        mb_submit.grid(row=8, column=1, sticky="nsew", pady=20)

    # Pseudocode
    # Display CirclePage 
    # Begin trials and have Timer begin when user clicks on the Circle
    # Once trials are done
    # Navigate to ResultPage with a button or within a condition the trials are complete 

class InstructionPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        label_instruction = Label(self,
        text=
        """
        Instructions
            
        Green circles will randomly generate within the screen. 
        Each circle must be clicked in order to proceed, and will be done 32 times.
        Any misclicks outside of the circles will effect the performance results.
        Progress will be visibly displayed on the top of the screen.""")

        label_instruction.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def begin():
            master.changePage(CirclePage)  

        mb_begin = Button(self, text="Begin", relief=RAISED, command=begin)  # Add command Agree
        mb_begin.menu = Menu(mb_begin, tearoff=0)
        mb_begin.grid(row=1, column=0, sticky="ns")


# Colored circle for user to click (32 count) - ERROR FIX SOON
class CirclePage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.canvas = Canvas(master, width=1000, height=680)
        self.circle_radius = 15
        self.number_of_circles = 32
        self.circles = []
        self.click_count = 0
        self.click_intervals = []
        self.inaccurate_clicks = 0

        # Start the timer
        self.start_time = time.time()

        # Generate the first cicrle
        self.generateCircle()

        # Progress label
        self.progress = Label(text=f"{self.click_count}/{self.number_of_circles}")
        self.progress.grid(sticky="n")

        # Add canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")

    # Transition 
    def complete(self):
        self.master.changePage(ThankPage)

    def generateCircle(self):
        """Generates circle one at a time"""
        self.canvas.delete("circle")
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        x = random.randint(self.circle_radius, canvas_width - self.circle_radius)
        y = random.randint(self.circle_radius, canvas_height - self.circle_radius)

        circle = self.canvas.create_oval(
            x - self.circle_radius, y - self.circle_radius,
            x + self.circle_radius, y + self.circle_radius,
            fill="green", tags="circle")
        self.canvas.tag_bind(circle, "<Button-1>", self.handleClick)
        self.circles.append((circle, x, y))

    # Define a function to handle a click on a circle
    def handleClick(self, event):
        # Incremement click count by number of circles clicked thus far
        self.click_count += 1
        self.click_intervals.append(time.time() - self.start_time)
        clicked_x = event.x
        clicked_y = event.y
        for circle, x, y in self.circles:
            center_x = x
            center_y = y
            distance = math.sqrt((clicked_x - center_x)**2 + (clicked_y - center_y)**2)
            if distance <= self.circle_radius:
                self.canvas.delete(circle)
                if distance >= (self.circle_radius / 2):
                    self.inaccurate_clicks += 1
                if self.click_count == self.number_of_circles:
                    completion_time = time.time()
                    self.destroy()
                    with open("Fitts_Data.csv", "r", newline="") as file:
                        reader = csv.reader(file)
                        # Read header row
                        header = next(reader)
                        # Find index position of last header
                        last_header_index = header.index("Hand") if "Hand" in header else 2
                        # Add new headers for new columns 
                        header = header[:last_header_index + 1] + ["Completion Time", "Click Intervals", "Total Clicks", "Inaccurate Clicks"] + header[last_header_index + 1:]
                        # Create list to hold rows with added columns
                        rows = []
                        for row in reader:
                            if len(row) < 4: # check if row has at least 4 elements 
                                continue # skip this row if insufficient amount of elements 
                            # Extract the previous columns 
                            id, age, gender, hand = row[:4]
                            # Extract list of click times and/or skip value cannot be converted to float and continue 
                            click_times = []
                            for x in row[4:]:
                                try:
                                    click_times.append(float(x))
                                except ValueError:
                                    pass
                            # Calculate total clicks
                            total_clicks = len(click_times)
                            # Check rows list is empty
                            if not rows: 
                                rows.append(header)
                            # Replace old and create new row with added columns
                            self.old_row = rows.pop(0)
                            new_row = [id, age, gender, hand, completion_time, self.click_intervals, total_clicks, self.inaccurate_clicks]
                            # Append new row to list of rows at end of list
                            rows.append(new_row)
                    with open("Fitts_Data.csv", "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(header)
                        writer.writerows(rows) # write all rows at once 
                        self.complete() # transition to last page of application
                        self.progress.grid_forget() # remove progress tracker label 
                        break
                else:
                    self.generateCircle()
                    self.progress.config(text=f"{self.click_count}/{self.number_of_circles}") # progress tracker X/32

class ThankPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        label_thank_you = Label(self,
                                text="Thank You!\n" + "Task is completed and data was collected.")
        label_thank_you.config(relief=SOLID)
        label_thank_you.grid(row=0, column=0, sticky="nsew", columnspan=2)

        def Close():
            app.quit()

        mb_close = Button(text="Quit", command=Close)
        mb_close.menu = Menu(mb_close, tearoff=0)
        mb_close.grid(row=1, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()