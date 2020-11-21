from __future__ import print_function

import sys

sys.dont_write_bytecode = True


class comments_class (object):

	def __init__(self, 
				comment_id, 
				author, 
				text, 
				content, 
				time_stamp):
	# def __init__(self, 
	# 			comment_id, 
	# 			author, 
	# 			text, 
	# 			content, 
	# 			time_stamp, 
	# 			reply_id, 
	# 			reply_author, 
	# 			resolved_status, 
	# 			reply_content):


		self.comment_id=comment_id  
		self.author=author  
		self.text=text  
		self.content=content  
		self.time_stamp=time_stamp  
		# self.reply_id=reply_id  
		# self.reply_author=reply_author  
		# self.resolved_status=resolved_status  
		# self.reply_content=reply_content

	def print_details(self):
		print("Author: ", self.author)
		print("Text: ", self.text)
		print("Comment: ", self.content)
		print("Comment Time: ", self.time_stamp)
		# print("Reply ID: ", self.reply_id)
		# print("Reply Author: ", self.reply_author)
		# print("Resolved Status: ", self.resolved_status)
		# print("Rely Content: ", self.reply_content)
	
	def random_print(self):
		print("testing the class method")

