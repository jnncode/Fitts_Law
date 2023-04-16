# Figures depicting the populated data
import pandas
import matplotlib.pyplot as plt

columns = ["ID", "Age", "Gender", "Hand", "Completion Time(s)", "Inaccurate Clicks"]
data = pandas.read_csv("Fitts_Data.csv", usecols=columns) # Specify index

# Scatter Plot - Age and Time > 15 Circle Radius
x = data["Age"][:10]
y = data["Completion Time(s)"][:10]
plt.scatter(x, y, color="b")
plt.xlabel("Age")
plt.ylabel("Time(s)")
plt.title("Completion Time vs. Age for Radius 15")
plt.show()

# Scatter Plot - Age and Time > 30 Circle Radius
x = data["Age"][10:]
y = data["Completion Time(s)"][10:]
plt.scatter(x, y, color="b")
plt.xlabel("Age")
plt.ylabel("Time(s)")
plt.title("Completion Time vs. Age for Radius 30")
plt.show()

# Scatter Plot - Gender and Time > 15 Circle Radius
data["Gender"] = data["Gender"].str.lower()
gender_labels = {"female": "Female", "male": "Male", "other": "Other"}
data["Gender"] = data["Gender"].replace(gender_labels)
x = data["Gender"][:10]
y = data["Completion Time(s)"][:10]
plt.scatter(x, y, color="b")
plt.xlabel("Gender")
plt.ylabel("Time(s)")
plt.title("Completion Time vs. Gender for Radius 15")
plt.show()

# Scatter Plot - Gender and Time > 30 Circle Radius

# Bar Graph - Average Inaccurate Clicks of 15 and 30 Circle Radius
x_ticks = [15, 30]
y1 = data["Inaccurate Clicks"][:10].mean() # Radius 15 
y2 = data["Inaccurate Clicks"][10:].mean() # Radius 30
width = 5
plt.bar(x_ticks[0], y1, width=width, color="b")
plt.bar(x_ticks[1], y2, width=width, color="r")
plt.xticks(x_ticks)
plt.xlabel("Radius")
plt.ylabel("Misclicks")
plt.title("Average Misclicks vs. Radius")
plt.show()

# Bar Graph - Average Time of 15 and 30 Circle Radius
x_ticks = [15, 30]
y1 = data["Completion Time(s)"][:10].mean() # Radius 15 
y2 = data["Completion Time(s)"][10:].mean() # Radius 30
width = 5
plt.bar(x_ticks[0], y1, width=width, color="b")
plt.bar(x_ticks[1], y2, width=width, color="r")
plt.xticks(x_ticks)
plt.xlabel("Radius")
plt.ylabel("Time(s)")
plt.title("Average Completion Time vs. Radius")
plt.show()