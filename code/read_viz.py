

def read_csv(filename):
	file_read = open(filename)
	file_data = file_read.read().split("\n")
	# print(file_data)
	file_data = file_data[2:]

	day_list = []
	time_list = []

	for entry in file_data:
		pass



read_csv("comments_list.csv")