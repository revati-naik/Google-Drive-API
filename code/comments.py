from __future__ import print_function

import httplib2
import files_get
import os, io
import csv
import get_file_id
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
		# print("Replies on commment:", replies)

		for reply in val['replies']:

			reply_id = reply['replyId']
			reply_author = reply['author']['displayName']
			print("Replied by: ", reply_author)

			# print_reply(service=service, file_id=file_id, comment_id=comment_id, reply_id=reply_id)

			try:
				resolved_status = reply['verb']
				print("Status: Comment/Reply has been resolved")
			except:
				print("Status: Comment/Reply not resolved")
				reply_content = reply['content']
				print("Reply content: ", reply_content)

			

		# reply_author = val['replies'][1]['author']['displayName']
		# print("Author of the reply: ", reply_author)

		print("-------------------")

	# return None
  except errors.HttpError, error:
	print('An error occurred', error)
  return None


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