# Figures depicting the populated data
import numpy
import pandas
import matplotlib.pyplot as plt

columns = ["ID", "Age", "Gender", "Hand", "Completion Time(s)", "Inaccurate Clicks"]
data = pandas.read_csv("Fitts_Data.csv", usecols=columns) # Specify index
print(data)

# Scatter Plot - Age
x = data["Age"][:10]
y = data["Completion Time(s)"][:10]
plt.scatter(x, y,c="b")
plt.xlabel("Age")
plt.ylabel("Completion Time(s)")
plt.title("Completion Time Based on Age")
plt.show()

# Scatter Plot - Gender
data["Gender"] = data["Gender"].str.lower()
gender_labels = {"female": "Female", "male": "Male", "other": "Other"}
data["Gender"] = data["Gender"].replace(gender_labels)
x = data["Gender"][:10]
y = data["Completion Time(s)"][:10]
plt.scatter(x, y, c="b")
plt.xlabel("Gender")
plt.ylabel("Completion Time(s)")
plt.title("Completion Time Based on Gender")
plt.show()

