import os
from fnmatch import fnmatch


# May need year for movies that have been remade
# And wouldnt get the movie 2012
# Check movies with spaces instead of .

# not every movie has a year, like looper 
#    The hunger games

# doesnt work good with mkv or avi


def Title(name):
	length = len(name)
	title = ""
	for x in range(0, length):
		# print (title)
		# print (name)

		# year xxxx
		if name[x].isdigit() and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3].isdigit():
			return title[:-1]

		# 720p
		if name[x].isdigit() and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3] == 'p':
			return title[:-1]

		# mp4
		if name[x] == 'm' and name[x+1] == 'p' and name[x+2] == '4':
			return title[:-1]

		# for years like (xxxx)
		if name[x] == "(" and name[x+1].isdigit() and name[x+2].isdigit() and name[x+3].isdigit() and name[x+4].isdigit() and name[x+5] == ")":
			return title[:-1]

		# Change . to a space
		if name[x] != '.':
			title = title + name[x]
		else:
			title = title + " "

	return title



if __name__ == '__main__':
	# root = 'E:Movies'
	root = 'E:'
	# pattern = "*.mp4"
	pattern = "*"
	list_movies = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			if fnmatch(name, pattern):
				# print (os.path.join(path, name))
				# print (Title(name))
				# print (name)
				title_and_location = Title(name), os.path.join(path, name)
				list_movies.append(title_and_location)

	# name = "2020.2017.720p.BluRay.x264-[YTS.AG].mp4"
	# print(Title(name), name)
	
	# print ("Title:", list_movies[597][0])
	# print ("Location:", list_movies[597][1])

	
	# w if it exist
	f = open("index.txt", "w")
	for movie in list_movies:
		f.write("Title: "+ str(movie[0]) + str("\n"))
		f.write("Location: "+ str(movie[1]) + str("\n\n"))
	f.close()

	# print (list_movies)
	print ("\nMovie count: ", len(list_movies))
	


