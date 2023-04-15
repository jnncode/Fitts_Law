# Figures depicting the populated data
import numpy
import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv("Fitts_Data.csv")
print(data)

plt.xlabel("Completion Time")
x = (data.columns[4])
plt.ylabel("Age")
y = (data.columns[1])
plt.title("Completion Time Based on Age")
plt.show()