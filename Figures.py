# Figures depicting the populated data
import numpy
import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv("Fitts_Data")

plt.xlabel("Completion Time")
plt.ylabel("Age")
plt.title("Completion Time Based on Age")