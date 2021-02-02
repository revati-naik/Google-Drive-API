from __future__ import print_function

import httplib2
# import files_get
import os
import io
import csv
# import get_file_id
import pandas as pd
from matplotlib import pyplot as plt
from apiclient import http
from apiclient import errors


import commentsClass
import numpy as np

from oauth2client import tools
from oauth2client import client
from apiclient import discovery
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


import sys
# import networkx as nx

sys.dont_write_bytecode = True

# """Retrieve a list of comments.
# 	Args:
# 	service: Drive API service instance.
# 	file_id: ID of the file to retrieve comments for.
# 	Returns:
# 	List of comments.
# """
def retrieve_comments(service, file_id, file_title):
	try:
		print("==========COMMENTS==========")
		comments = service.comments().list(fileId=file_id).execute()
		comments_list = comments.get('items', [])
		with open(file_title + "_comments.csv",'w') as file:
				writer = csv.writer(file)
				writer.writerow(["SN", "Author", "Text", "Comment", "Time Stamp", "Replies", "Reply Author", "Reply Type", "Reply Content", "Status"])
		i = 1
		# comment_time_list = []
		# comment_day_list = []
		dict_to_print = {}
		minor_dict = {"days":[], "time": [], "replies": []}
		for val in comments_list:
			# print(val)
			# break
			
			author = val['author']['displayName'].encode('ascii', 'ignore')
			# print("Author: ", author)
			text = val['context']['value'].encode('ascii', 'ignore')
			# print("Text: ", text)
			content1 = val['content'].encode('ascii', 'ignore')
			# print("Comment: ", content1)
			comment_id = val['commentId'].encode('ascii', 'ignore')
			time_stamp = val['modifiedDate'].encode('ascii', 'ignore')
		
			comments_details = commentsClass.comments_class(comment_id=comment_id, 
					author=author, 
					text=text, 
					content=content1, 
					time_stamp=time_stamp)

			comments_details.print_details()

			replies = val['replies']
			print("Replies on commment:", len(replies))

			with open(file_title + "_comments.csv",'a') as file:
				writer = csv.writer(file)
				# writer.writerow(["SN", "Author", "Text", "Content"])
				writer.writerow([i, author.decode('utf-8'), text.decode('utf-8'), content1.decode('utf-8'), time_stamp.decode('utf-8'), len(replies)])
			i = i+1
			if len(replies) != 0:
				for reply in val['replies']:
				
					try:
						resolved_status = reply['verb']

						reply_id = reply['replyId']
						reply_author = reply['author']['displayName']
						print("Reolved by: ", reply_author)
						reply_date = reply['modifiedDate']
						print("Resolved time Date: ", reply_date)
						
						# day, time = get_date_time(timestamp=reply_date)
						reply_content = reply['content']

						if resolved_status == "resolve":

							print("Resolved Status: ", resolved_status)
							print("Status: Comment/Reply has been resolved by ", reply_author)


						with open(file_title + "_comments.csv",'a') as file:
							writer = csv.writer(file)
							writer.writerow([i, author.decode('utf-8'), text.decode('utf-8'), content1.decode('utf-8'), reply_date.decode('utf-8'), "-",  reply_author.decode('utf-8'), "Resolving the comment", "-",resolved_status])

					except:
						reply_id = reply['replyId']
						reply_author = reply['author']['displayName']
						print("Replied by: ", reply_author)
						reply_date = reply['modifiedDate']
						print("Reply Date: ", reply_date)
						
						# day, time = get_date_time(timestamp=reply_date)
						# print("This is not a reply")
						reply_content = reply['content']
						print("Reply Content: ", reply_content)
						resolved_status = "not resolved"
						print("Status: Comment/Reply not resolved")
						with open(file_title + "_comments.csv",'a') as file:
							writer = csv.writer(file)
							writer.writerow([i, reply_author, text.decode('utf-8'), content1.decode('utf-8'), reply_date, "-",  reply_author, "Reply on comment", reply_content, resolved_status])

						i += 1
				# day, time = get_date_time(timestamp=time_stamp)
				print("-------------------")
		return dict_to_print
	except errors.HttpError as error:
  		print('An error occurred', error)




# def print_reply(service, file_id, comment_id, reply_id):
#   """Print information about the specified reply.

#   Args:
# 	service: Drive API service instance.
# 	file_id: ID of the file to print reply for.
# 	comment_id: ID of the comment to print reply for.
# 	reply_id: ID of the reply to print.
#   """
#   try:
# 	reply = service.replies().get(
# 		fileId=file_id, commentId=comment_id, replyId=reply_id).execute()
# 	# print(reply)
# 	# print ('Modified Date: ', reply['modifiedDate'])
# 	# print ('Author: ', reply['author']['displayName'])
# 	# print ('Content: ', reply['content'])
#   except errors.HttpError, error:
# 	print ('An error occurred: ', error)


# def viz_graph(dict_to_print):
# 	# print("dict_to_print: ", dict_to_print)
# 	i = 0
# 	plt.title('Comments Frequency')
# 	plt.ylim(1440)
# 	plt.gca().invert_yaxis()
# 	plt.xlabel('Days')
# 	plt.ylabel('Time (Minutes)')
# 	# dict_to_print = {"Philip":{"days":['2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-12'], "time": [853, 289, 650, 780, 277], "color": "cyan"}, "Revati":{"days":['2020-08-17', '2020-08-15', '2020-08-13', '2020-08-12', '2020-08-12'], "time": [800, 123, 555, 999, 765], "color": "orange"}}
# 	color_list = ["cyan","orange", "lightgreen", "teal", "orchid" ]
# 	marker_list = ["o", "v", "s", "p", "D"]
# 	for keys, values in dict_to_print.items():
# 		user_label = keys
# 		print("USERS: ", user_label)
# 		# print(values.items())
# 		# break
# 		for key_small, values_small in values.items():
# 			# print(values)
# 			comment_day_list = values["days"]
# 			comment_time_list = values["time"]
# 			user_color = color_list[i]
# 			user_marker = marker_list[i]
# 			# print("comment_day_list: ", comment_day_list)
# 			# print("comment_time_list: ", comment_time_list)
# 		# print
# 		plt.scatter(comment_day_list, comment_time_list, color=user_color, alpha=0.7, label=user_label, marker=user_marker)
# 		plt.legend(loc = 'best')
# 		i += 1
# 	plt.show()
# 			# break



# 	# comment_day_list_1 = ['2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-12']
# 	# comment_day_list_2 = ['2020-08-17', '2020-08-15', '2020-08-13', '2020-08-12', '2020-08-12']
# 	# comment_time_list_1 = [853, 289, 650, 780, 277]
# 	# comment_time_list_2 = [800, 123, 555, 999, 765]
# 	# plt.ylim(1440)
# 	# plt.gca().invert_yaxis()
# 	# plt.xlabel('Days')
# 	# plt.ylabel('Time (Minutes)')
# 	# plt.scatter(comment_day_list_1, comment_time_list_1, color="cyan", alpha=0.7, label="Revati")
# 	# plt.scatter(comment_day_list_2, comment_time_list_2, color="orange", alpha=0.7, label="Philip")
# 	# plt.title('Comments Frequency')
# 	# plt.legend(loc = 'best')
# 	# plt.show()
# 	# 
# 	# 
# def get_date_time(timestamp):
# 	comment_day = timestamp.split("T")[0]
# 	# print("comment_day: ", comment_day)
# 	comment_time = timestamp.split("T")[1][:5].split(":")
# 	# comment_time = comment_time_list
# 	total_time_minutes = int(comment_time[0])*60 + int(comment_time[1])
# 	# print("total_time_minutes", total_time_minutes)
# 	# print("Author to add: ", author)
# 	# comment
# 	comment_time = (total_time_minutes)

# 	return comment_day, comment_time


# def graph_plot():

# 	fig, ax = plt.subplots()
# 	# print("In func")
# 	G = nx.Graph()
# 	# G.add_node(1)
# 	# G.add_node(2)
# 	# G.add_edge(1,2)

# 	authors = {1:"Anisha", 2:"Revati", 3:"Chenxi", 4:"Lauren"}

# 	# G.add_nodes_from(["1", "2", "3", "4"])

# 	########Group Writing#############
# 	# G.add_edge(4,1,weight=5)
# 	# G.add_edge(2,1,weight=2)
# 	# G.add_edge(1,3,weight=1)
# 	# G.add_edge(2,4,weight=1)


# 	########Parallel Writing##########
# 	# G.add_edge(1,4,weight=2)
# 	# G.add_edge(3,4,weight=4)
# 	# G.add_edge(3,1,weight=4)
# 	# G.add_edge(3,2,weight=1)
# 	# G.add_edge(1,2,weight=1)

# 	########Cooperative Revision######
# 	G.add_edge(2,1,weight=2)
# 	G.add_edge(2,3,weight=1)
# 	G.add_edge(1,3,weight=1)
# 	G.add_edge(1,4,weight=1)



# 	# G.add_edges_from([("4", "1", weight=5), ("2", "1", weight=2), ("1", "3"), ("2", "4")])
# 	# pos = nx.circular_layout(G)

# 	# G.add_edges_from([("a","c"),("c","d"), ("a",1), (1,"d"), ("a",2)])
# 	edges = G.edges()
# 	# colors = [G[u][v]['color'] for u,v in edges]
# 	weights = [G[u][v]['weight'] for u,v in edges]
# 	# G = nx.relabel_nodes(G, authors)
# 	pos=nx.spring_layout(G)
# 	# nx.draw(H, pos, node_color="black", edge_color="lightblue", edges=edges, width=weights, with_labels=True)
# 	# nx.draw(H, pos, edges=edges, width=weights, with_labels=True)
# 	nx.draw(G, pos, edges=edges, width=weights, with_labels=True)

# 	# nx.draw(H, node_color="cyan", with_labels = True)
# 	ax.set_title("Comments Relation")
# 	# plt
# 	plt.show()


# def comments_num_bar():
# 	N = 4
# 	ind = np.arange(N)

# 	########Cooperative Revision######
# 	# Anisha = np.array([0, 0, 1, 1, 1])
# 	# Revati = np.array([1, 0, 1, 0, 0])
# 	# Chenxi = np.array([0, 1, 1, 0, 0])
# 	# Lauren = np.array([0, 0, 0, 0, 1])
# 	# plt.xticks(ind, ('11/16', '11/17', '11/18', '11/20', '11/24'))

# 	#######Parallel Writing##########
# 	# Anisha = np.array([1, 0, 1, 7, 1, 0, 1])
# 	# Revati = np.array([0, 2, 0, 0, 1, 0, 0])
# 	# Chenxi = np.array([1, 0, 0, 1, 0, 1, 2])
# 	# Lauren = np.array([0, 0, 0, 1, 3, 1, 1])
# 	# plt.xticks(ind, ('11/13', '11/16', '11/17', '11/20', '11/21', '11/22', '11/24'))

# 	########Group Writing#############
# 	Anisha = np.array([1, 1, 3, 6])
# 	Revati = np.array([1, 0, 1, 4])
# 	Chenxi = np.array([1, 3, 0, 0])
# 	Lauren = np.array([0, 0, 3, 4])
# 	plt.xticks(ind, ('11/17', '11/18', '11/20', '11/24'))

# 		# the x locations for the groups
# 	width = 0.35       # the width of the bars: can also be len(x) sequence

# 	p1 = plt.bar(ind, Anisha, width, bottom=Revati+Chenxi+Lauren)
# 	p2 = plt.bar(ind, Revati, width, bottom=Chenxi+Lauren)
# 	p3 = plt.bar(ind, Chenxi, width, bottom=Lauren)
# 	p4 = plt.bar(ind, Lauren, width)

# 	plt.ylabel('No. of Comments')
# 	plt.xlabel('Date')
# 	plt.title('Number of Comments in a Day')
	
# 	# plt.yticks(np.arange(0, 81, 10))
# 	plt.legend((p1[0], p2[0], p3[0], p4[0]), ('Anisha', 'Revati', 'Chenxi', 'Lauren'))

# 	plt.show()


	

# if __name__ == '__main__':
# 	# graph_plot()
# 	comments_num_bar()