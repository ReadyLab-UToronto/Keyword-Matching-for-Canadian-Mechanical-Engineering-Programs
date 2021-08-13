import pandas as pd
import os
import csv
import sys

#find folder of a particular university and display all csv files in it
root_folder_name = "C:\\Users\\jerry\\OneDrive - University of Waterloo (1)\\Co-op\\Co-op 3 - S21 - UW UofT USRA\\Webscraping Scripts and Data"
folder_name = input("Folder name: ")
path = root_folder_name + "\\" + folder_name
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.csv')]

print()
for file in files:
	print(file)
print()

if input("Continue? y/n ") != "y":
	sys.exit()
print()

#dictionary to hold all the combined data from all the csvs
dict_of_courses = {"School": [], "Course Number": [], "Course Name": [], "Only Available Within Option/Specialization": [], "Atypical Elective": [], "Course Description": []}

#identify and separate files for general mech eng program and files for courses in options
files_atypical = [file for file in files if "atypical" in file.lower()]
files_options = [file for file in files if ("option" in file.lower() or "specialization" in file.lower() or "minor" in file.lower()) and (file not in files_atypical)]
files_general = [file for file in files if file not in files_options and file not in files_atypical]

#to count the file lengths for some sanity checking
counter = 0

#first load in csvs of the general mech eng program
print("reading these general files: ")
for file in files_general:
	print(file)
print()

for file in files_general:
	counter = 0

	try:
		with open(os.path.join(path, file), encoding = "utf-8") as f:
			
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(" ")
					dict_of_courses["Atypical Elective"].append(" ")
					counter += 1
				else:
					print("Duplicate: ", row[0])	

		print("finished reading {}, {} rows added \n".format(file, counter))

	except UnicodeDecodeError:

		print("Encountered UnicodeDecodeError, switching encoding to mbcs")
		with open(os.path.join(path, file), encoding = "mbcs") as f:
			
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(" ")
					dict_of_courses["Atypical Elective"].append(" ")
					counter += 1
				else:
					print("Duplicate: ", row[0])	

		print("finished reading {}, {} rows added \n".format(file, counter))


#second load in csvs of options/specilizations/"minors"
print("reading these options files: ")
for file in files_options:
	print(file)
print()

for file in files_options:
	counter = 0

	try:
		with open(os.path.join(path, file), encoding = "utf-8") as f:
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			file_tokens = file.lower().split("_")	

			if "option" in file_tokens:
				option_index = file_tokens.index("option") - 1
				option_name = file_tokens[option_index]
				
			elif "specialization" in file_tokens:
				option_index = file_tokens.index("specialization") - 1
				option_name = file_tokens[option_index]			
				
			elif "minor" in file_tokens:
				option_index = file_tokens.index("minor") - 1
				option_name = file_tokens[option_index]			
			else:
				option_name = " "
				print("No options files found") #should not happen since these files would be taken care of in the first loop
						
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(option_name)
					dict_of_courses["Atypical Elective"].append(" ")
					counter += 1
				else:
					print("Duplicate: ", row[0])

	except UnicodeDecodeError:

		print("Encountered UnicodeDecodeError, switching encoding to mbcs")
		with open(os.path.join(path, file), encoding = "mbcs") as f:
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			file_tokens = file.lower().split("_")	

			if "option" in file_tokens:
				option_index = file_tokens.index("option") - 1
				option_name = file_tokens[option_index]
				
			elif "specialization" in file_tokens:
				option_index = file_tokens.index("specialization") - 1
				option_name = file_tokens[option_index]			
				
			elif "minor" in file_tokens:
				option_index = file_tokens.index("minor") - 1
				option_name = file_tokens[option_index]			
			else:
				option_name = " "
				print("No options files found") #should not happen since these files would be taken care of in the first loop
						
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(option_name)
					dict_of_courses["Atypical Elective"].append(" ")
					counter += 1
				else:
					print("Duplicate: ", row[0])

	print("finished reading {}, {} rows added \n".format(file, counter))

#third load in csvs of atypical, non-technical, outside department electives
print("reading these atypical electives files: ")
for file in files_atypical:
	print(file)
print()

for file in files_atypical:
	counter = 0

	try:
		with open(os.path.join(path, file), encoding = "utf-8") as f:
			
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(" ")
					dict_of_courses["Atypical Elective"].append("Yes")
					counter += 1
				else:
					print("Duplicate: ", row[0])

	except UnicodeDecodeError:
		
		print("Encountered UnicodeDecodeError, switching encoding to mbcs")
		with open(os.path.join(path, file), encoding = "mbcs") as f:
		
			reader = csv.reader(f)
			skip_headers = next(reader)
			
			for row in reader:
				if row[0] not in dict_of_courses['Course Number']:
					dict_of_courses['School'].append(folder_name)
					dict_of_courses['Course Number'].append(row[0])
					dict_of_courses['Course Name'].append(row[1])
					dict_of_courses['Course Description'].append(row[2])
					dict_of_courses["Only Available Within Option/Specialization"].append(" ")
					dict_of_courses["Atypical Elective"].append("Yes")
					counter += 1
				else:
					print("Duplicate: ", row[0])

	print("finished reading {}, {} rows added \n".format(file, counter))


df = pd.DataFrame(dict_of_courses)
df.to_csv("Complete_{}_MechanicalEngineering_Courses.csv".format(folder_name), index = False)
