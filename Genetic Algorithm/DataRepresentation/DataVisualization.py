import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 36)
score = []
lines_cleared = []
time_trained = []

with open("GeneticAlgorithm/Logs/logs.txt", "r") as f:
    lines = f.readlines()
    for line_num, line in enumerate(lines):
        if line_num % 112 == 56:
            if line.startswith("[["):
                indiv = eval(line)
                score.append(indiv[0][0])
                lines_cleared.append(indiv[0][1])
        if line.startswith("time"):
            txt1, txt2, time = line.split()
            time_trained.append(eval(time))

fig, ax1 = plt.subplots()
line1 = ax1.plot(x, score, label="Point", color="red")
ax1.set_ylabel("Point")
ax1.set_ylim(0, 24000)

ax2 = ax1.twinx()
line2 = ax2.plot(x, lines_cleared, label="Lines Cleared", color="blue")
ax2.set_ylabel("Lines Cleared")
ax2.set_ylim(0, 450)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="lower right") 

ax1.set_xlabel("Generation")  

plt.figure(1)
fig, ax1 = plt.subplots()

line1 = ax1.plot(x, score, label="Point", color="red")
ax1.set_ylabel("Point")  
ax1.set_ylim(0, 24000)
ax1.tick_params(axis='y') 

ax2 = ax1.twinx()
line2 = ax2.plot(x, time_trained, label="Time Trained", color="blue")
ax2.set_ylabel("Time Trained")  
ax2.set_ylim(0, 5000)
ax2.tick_params(axis='y')  

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="lower right")  


ax1.set_xlabel("Generation") 
ax1.tick_params(axis='x')

plt.show()