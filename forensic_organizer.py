"""
Written by Flynn Acworth
27/11/2015

This code is a mishmash of
forensic goodness, learn to
love it, friend.
"""

import os
import subprocess
import time

# The below code checks for incorrect file extensions and sorts files into the correct folders

def identify_and_move(root_folder):

	"""

	This funciton reads through each
	file in a folder structure, and
	identifies whether the file extension
	has been falsified.

	If the file extension is incorrect
	it is noted down in a log. The file is then
	moved into the correct folder for analysis

	"""
	inc = 0
	copied_file_list = []
	file_list = []
	for root, dirs, files in os.walk(root_folder + "Logical\\"):
		for f in files:
			file_list.append(f)
			print inc
			try:
				file_ary = f.split(".")
				file_ext = file_ary[len(file_ary)-1]
			except:
				pass
			command = 'exiftool "{}"'.format(os.path.join(root,f))
			proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
			exiftool_data = proc.stdout.read().split('\n')
			true_ext = file_ext
			
			for line in exiftool_data:
				
				if "File Type" in line:
					true_ext = line.split(":")[1].strip().lower()
					break
				elif "Error" in line:
					true_ext = "unknown"
					break
				else:
					pass

			if file_ext != true_ext:
				with open("log.txt", "a") as log_file:
					if ( (file_ext == "jpg") and (true_ext == "jpeg") ):
						inc += 1
						file_data = open(os.path.join(root,f), "rb").read()
						copy_file(f, root_folder, file_data, true_ext)
						copied_file_list.append(f)
						continue
					else:
						pass
					log_text = "File '{}'' extension really: {}\n".format(f, true_ext)
					log_file.write(log_text)
					log_file.close()
			else:
				pass

			file_data = open(os.path.join(root,f), "rb").read()
			copy_file(f, root_folder, file_data, true_ext)
			copied_file_list.append(f)
			inc += 1
	for f in file_list:
		if f not in copied_file_list:
			print "NOT COPIED OVER: {}".format(f)

def copy_file(name, root_folder, file_data, extension):

	"""

	This procedure copies all files from the logical or
	physical directory, and puts them into individual
	folders according to their file extension inside the
	analysis folder

	Arguments: file name, file extension

	"""

	analysis_folder = root_folder + "Analysis/" + extension

	if not os.path.exists(analysis_folder):
		os.makedirs(analysis_folder)
	else:
		pass

	new_file = open(analysis_folder + "/" + name, "wb")

	new_file.write(file_data)

	new_file.close()

def generate_folders(root_folder):

	"""

	This procedure is used to create the 
	folder structure for the report.

	It genereates the image, logical, 
	physical, analysis and log folders.

	This takes no arguments, and returns no values.

	This procedure should be called at the very start
	of the forensic script, never again.

	Later I may want to make this simpler, and allow
	the user to input their own folder names.

	"""

	# List of folder to be put inside investigation file
	folders = ["Image\\", "Logical\\", "Logs\\" "Physical\\", "Analysis\\"]

	# Creates the main investigation file
	os.makedirs(root_folder)

	# Creates the folders based on the list contents
	for folder in folders:
		os.makedirs(root_folder+folder)

def main():

	# Creates the root folder
	root_folder = "forensic_analysis_"+time.strftime("%Y-%m-%d")+"/"
	print "[+] Making file structure"

	# Generates the file structure inside of root
	generate_folders(root_folder)

	raw_input("Put files inside logical")

	identify_and_move(root_folder)


main()