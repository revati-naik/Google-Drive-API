import matplotlib
import matplotlib.pyplot as plt
import numpy as np


labels = ['Day1', 'Day2', 'Day3', 'Day4', 'Day5']
author_1_comments = np.array([38, 17, 26, 19, 15])/2
author_2_comments = np.array([37, 23, 18, 18, 10])/2
author_3_comments = np.array([46, 27, 26, 19, 17])/2

author_1_edits = np.array([85, 97, 126, 119, 215])/10
author_2_edits = np.array([300, 223, 218, 118, 110])/10
author_3_edits = np.array([346, 127, 326, 219, 317])/10
ind = [y for y, _ in enumerate(labels)]




x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
# rects1 = ax.bar(x - width/2, author_1, width, label='Comments', bottom=author_2+author_1)
# rects2 = ax.bar(x + width/2, author_2, width, label='Edits', bottom=author_1)


plt.bar(x-width/2, author_1_comments, width, label='author_1', edgecolor='black', color='gold', bottom=author_2_comments+author_1_comments)
plt.bar(x-width/2, author_2_comments, width, label='author_2', edgecolor='black', color='silver', bottom=author_1_comments)
plt.bar(x-width/2, author_3_comments, width, label='author_3', edgecolor='black', color='#CD853F')


plt.bar(x+width/2, author_1_edits, width, edgecolor='black', color='gold', bottom=author_2_edits+author_1_edits)
plt.bar(x+width/2, author_2_edits, width, edgecolor='black', color='silver', bottom=author_1_edits)
plt.bar(x+width/2, author_3_edits, width, edgecolor='black', color='#CD853F', tick_label="edits")


# Add some text for labels, title and custom x-axis tick labels, etc.
plt.xticks(ind, labels)
plt.ylabel('No. of Comments/Edits')
plt.xlabel('Days')
plt.title('Comments and Edits')

plt.legend(loc = 'best')
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         plt.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

# fig.tight_layout()
plt.grid()
plt.show()
