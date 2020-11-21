from __future__ import print_function

import httplib2
import files_get
import os, io
import csv
import get_file_id
import pandas as pd
from matplotlib import pyplot as plt
from apiclient import http
from apiclient import errors


import commentsClass

from oauth2client import tools
from oauth2client import client
from apiclient import discovery
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


import sys

sys.dont_write_bytecode = True


def retrieve_comments(service, file_id):
  """Retrieve a list of comments.

  Args:
	service: Drive API service instance.
	file_id: ID of the file to retrieve comments for.
  Returns:
	List of comments.
  """
  try:

	print("==========COMMENTS==========")
	comments = service.comments().list(fileId=file_id).execute()
	# print(comments)
	# return comments.get('items', [])
	comments_list = comments.get('items', [])
	# print(comments_list[0])

	with open('comments_list.csv','w') as file:
			writer = csv.writer(file)
			writer.writerow(["SN", "Author", "Text", "Content", "Time Stamp"])
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
		# print("Modified Time: ", time_stamp)

		# print(time_stamp.split("T"))
		# comment_day_list.append(time_stamp.split("T")[0])
		# comment_day = time_stamp.split("T")[0]
		# print("comment_day: ", comment_day)
		# comment_time = time_stamp.split("T")[1][:5].split(":")
		# # comment_time = comment_time_list
		# total_time_minutes = int(comment_time[0])*60 + int(comment_time[1])
		# print("total_time_minutes", total_time_minutes)
		# print("Author to add: ", author)
		# # comment
		# comment_time = (total_time_minutes)
		# break
		
		# if author not in dict_to_print.keys():
		# 	dict_to_print[author] = minor_dict
		# 	dict_to_print[author]["days"].append(comment_day)
		# 	dict_to_print[author]["time"].append(comment_time)
		# else:
		# 	dict_to_print[author]["days"].append(comment_day)
		# 	dict_to_print[author]["time"].append(comment_time)
		# else:
			# print("Already present")
		# dict_to_print[author]["days"] = comment_day_list
		# minor_dict["time"] = comment_time_list
		# dict_to_print[author] = minor_dict
		# print("Adding author: ", author)
		# dict_to_print[author]["days"].append(comment_day)
		# dict_to_print[author]["time"].append(comment_time)
		# print(dict_to_print)
		# comment_time_list = []
		# comment_day_list = []


		comments_details = commentsClass.comments_class(comment_id=comment_id, 
				author=author, 
				text=text, 
				content=content1, 
				time_stamp=time_stamp)

		comments_details.print_details()

		with open('comments_list.csv','a') as file:
			writer = csv.writer(file)
			# writer.writerow(["SN", "Author", "Text", "Content"])
			writer.writerow([i, author, text, content1, time_stamp])
		i = i+1

		replies = val['replies']
		print("Replies on commment:", len(replies))
		# print(replies)
		if len(replies) != 0:
			for reply in val['replies']:
				# print(reply)

				reply_id = reply['replyId']
				reply_author = reply['author']['displayName']
				print("Replied by: ", reply_author)
				reply_date = reply['modifiedDate']
				print("Reply Date: ", reply_date)

				day, time = get_date_time(timestamp=reply_date)

				if author not in dict_to_print.keys():
					dict_to_print[author] = {"days":[], "time": []}
				# print("dict_to_print_new: ", dict_to_print)
				
				dict_to_print[author]["days"].append(day)
				dict_to_print[author]["time"].append(time)

				# print_reply(service=service, file_id=file_id, comment_id=comment_id, reply_id=reply_id)

				try:
					resolved_status = reply['verb']
					print("Status: Comment/Reply has been resolved")
				except:
					print("Status: Comment/Reply not resolved")
					reply_content = reply['content']
					print("Reply content: ", reply_content)
			# comments_details = commentsClass.comments_class( 
			# 		comment_id=comment_id, 
			# 		author=author, 
			# 		text=text, 
			# 		content=content1, 
			# 		time_stamp=time_stamp, 
			# 		reply_id=reply_id, 
			# 		reply_author=reply_author, 
			# 		resolved_status=resolved_status, 
			# 		reply_content=reply_content)	

			# comments_details.print_details()

		# else:
		# 	comments_details = commentsClass.comments_class(comment_id=comment_id, 
		# 		author=author, 
		# 		text=text, 
		# 		content=content1, 
		# 		time_stamp=time_stamp)

		# 	comments_details.print_details()

		# reply_author = val['replies'][1]['author']['displayName']
		# print("Author of the reply: ", reply_author)
		day, time = get_date_time(timestamp=time_stamp)

		if author not in dict_to_print.keys():
			dict_to_print[author] = {"days":[], "time": []}
			# print("dict_to_print_new: ", dict_to_print)
			
		dict_to_print[author]["days"].append(day)
		dict_to_print[author]["time"].append(time)
		# print(dict_to_print)
		# minor_dict = {"days":[], "time": []}
		print("-------------------")

	# print("comment_time_list: ", comment_time_list)
	# print("comment_day_list: ", comment_day_list)

	# return None
  except errors.HttpError, error:
	print('An error occurred', error)
  return dict_to_print


def print_reply(service, file_id, comment_id, reply_id):
  """Print information about the specified reply.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print reply for.
    comment_id: ID of the comment to print reply for.
    reply_id: ID of the reply to print.
  """
  try:
    reply = service.replies().get(
        fileId=file_id, commentId=comment_id, replyId=reply_id).execute()
    # print(reply)
    # print ('Modified Date: ', reply['modifiedDate'])
    # print ('Author: ', reply['author']['displayName'])
    # print ('Content: ', reply['content'])
  except errors.HttpError, error:
    print ('An error occurred: ', error)


def viz_graph(dict_to_print):
	# print("dict_to_print: ", dict_to_print)
	i = 0
	plt.title('Comments Frequency')
	plt.ylim(1440)
	plt.gca().invert_yaxis()
	plt.xlabel('Days')
	plt.ylabel('Time (Minutes)')
	# dict_to_print = {"Philip":{"days":['2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-12'], "time": [853, 289, 650, 780, 277], "color": "cyan"}, "Revati":{"days":['2020-08-17', '2020-08-15', '2020-08-13', '2020-08-12', '2020-08-12'], "time": [800, 123, 555, 999, 765], "color": "orange"}}
	color_list = ["cyan","orange", "lightgreen", "teal", "orchid" ]
	marker_list = ["o", "v", "s", "p", "D"]
	for keys, values in dict_to_print.items():
		user_label = keys
		print("USERS: ", user_label)
		# print(values.items())
		# break
		for key_small, values_small in values.items():
			# print(values)
			comment_day_list = values["days"]
			comment_time_list = values["time"]
			user_color = color_list[i]
			user_marker = marker_list[i]
			# print("comment_day_list: ", comment_day_list)
			# print("comment_time_list: ", comment_time_list)
		# print
		plt.scatter(comment_day_list, comment_time_list, color=user_color, alpha=0.7, label=user_label, marker=user_marker)
		plt.legend(loc = 'best')
		i += 1
	plt.show()
			# break





	# comment_day_list_1 = ['2020-08-17', '2020-08-16', '2020-08-15', '2020-08-14', '2020-08-12']
	# comment_day_list_2 = ['2020-08-17', '2020-08-15', '2020-08-13', '2020-08-12', '2020-08-12']
	# comment_time_list_1 = [853, 289, 650, 780, 277]
	# comment_time_list_2 = [800, 123, 555, 999, 765]
	# plt.ylim(1440)
	# plt.gca().invert_yaxis()
	# plt.xlabel('Days')
	# plt.ylabel('Time (Minutes)')
	# plt.scatter(comment_day_list_1, comment_time_list_1, color="cyan", alpha=0.7, label="Revati")
	# plt.scatter(comment_day_list_2, comment_time_list_2, color="orange", alpha=0.7, label="Philip")
	# plt.title('Comments Frequency')
	# plt.legend(loc = 'best')
	# plt.show()
	# 
	# 
def get_date_time(timestamp):
	comment_day = timestamp.split("T")[0]
	# print("comment_day: ", comment_day)
	comment_time = timestamp.split("T")[1][:5].split(":")
	# comment_time = comment_time_list
	total_time_minutes = int(comment_time[0])*60 + int(comment_time[1])
	# print("total_time_minutes", total_time_minutes)
	# print("Author to add: ", author)
	# comment
	comment_time = (total_time_minutes)

	return comment_day, comment_time