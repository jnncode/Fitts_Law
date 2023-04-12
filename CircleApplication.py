from tkinter import *
from tkinter import font
from tkinter import messagebox
import tkinter as tk
import time
import random
import csv
import math


# import pandas
# import os

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

        mb_agree = Button(self, text="I Agree", relief=RAISED, width=7, height=1, command=clickAgree)
        mb_agree.menu = Menu(mb_agree, tearoff=0)
        mb_agree.grid(row=1, column=0, sticky="ns", pady=8)

        def clickDisagree():
            self.quit()

        mb_disagree = Button(self, text="I Decline", relief=RAISED, width=7, height=1, command=clickDisagree)
        mb_disagree.menu = Menu(mb_disagree, tearoff=0)
        mb_disagree.grid(row=2, column=0, sticky="ns", pady=8)


# Lists ID, Age, Gender, and Handedness then transfers the information into the CSV file
# Clear all data before beginning trials to keep CSV accurate and consistent
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
            participant_count += 1  # Begin with P0001
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

            age = age_entry.get().strip(" ")
            gender = gender_entry.get().strip(" ")
            hand = hand_entry.get().strip(" ")

            new_id = generateId()  # generate a new ID each time the user submits for next user

            # Store the data in CSV file (database)
            with open("Fitts_Data.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Check if the file is empty
                    writer.writerow(["ID", "Age", "Gender", "Hand", "Completion Time(s)", "Click Intervals(ms)", "Inaccurate Clicks"])  # Write headers
                data_str = "{},{},{},{},".format(new_id, age, gender, hand)
                file.write(data_str)
                # writer.writerow([new_id, age, gender, hand])
            # removeSpaces("Fitts_Data.csv")
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


# Colored circle for user to click (32 count)
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
        """Handles the clicks of the circles"""
        self.click_count += 1
        self.click_intervals.append(round(((time.time() - self.start_time) * 1000), 4))  # convert to milliseconds
        clicked_x = event.x
        clicked_y = event.y
        for circle, x, y in self.circles:
            center_x = x
            center_y = y
            distance = math.sqrt((clicked_x - center_x) ** 2 + (clicked_y - center_y) ** 2)
            if distance <= self.circle_radius:
                self.canvas.delete(circle)
                if distance >= (self.circle_radius / 2):
                    self.inaccurate_clicks += 1
                if self.click_count == self.number_of_circles:
                    self.completion_time = round((time.time() - self.start_time), 4)  # convert to seconds
                    self.destroy()
                    self.handleData(1)
                    self.complete() # transition to last page of application
                    self.progress.grid_forget() # remove progress tracker label
                else:
                    self.generateCircle()
                    self.progress.config(text=f"{self.click_count}/{self.number_of_circles}")  # progress tracker X/32

    def handleData(self, row_index):
        """Handles the existing data in addition to new data in CSV"""
        # Write new data to CSV file
        with open("Fitts_Data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.completion_time, (sum(self.click_intervals) / 32), self.inaccurate_clicks])

        # Read existing data from CSV file
        with open("Fitts_Data.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = list(reader)

        # # Update headers to include new columns (if not added previously)
        # new_headers = ["Completion Time(s)", "Click Intervals(ms)", "Inaccurate Clicks"]
        # if set(new_headers) - set(headers):
        #     headers += new_headers
        #
        # if row_index > 7:
        #     raise TypeError("Maximum of headers reached.")

        # # Write headers to file (if necessary) and update data
        # with open("Fitts_Data.csv", mode="w", newline="") as file:
        #     writer = csv.writer(file)
        #     if set(new_headers) - set(headers):
        #         writer.writerow(headers + new_headers)
        #     writer.writerows([headers] + data[:row_index] + [[self.completion_time, (sum(self.click_intervals) / 32), self.inaccurate_clicks]] + data[row_index+1:])

class ThankPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        label_complete = Label(self,
                               text=
                               """
                               Task Completed.

                               Thank you for participating in the study!""", justify=CENTER)

        label_complete.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, minsize=1000, weight=6)
        self.rowconfigure(0, minsize=600, weight=6)

        def close():
            app.quit()

        mb_close = Button(self, text="Quit", relief=RAISED, width=7, height=1, command=close)
        mb_close.menu = Menu(mb_close, tearoff=0)
        mb_close.grid(row=1, column=0, sticky="ns", pady=8)


if __name__ == "__main__":
    app = Application()
    app.mainloop()