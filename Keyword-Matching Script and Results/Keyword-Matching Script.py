import nltk
from nltk.util import ngrams
import re
import string
import pandas as pd

#1. read in dataset
course_data_df = pd.read_csv("..\\Web-Scraping Scripts and Data\\Accredited Canadian English Undergrad MechEng Programs\\All_Web-Scraped_Courses_Master_List.csv")

################################################################################################################

#2. clean up descrptions
def process_text(text):
	
	#2.1 replace hyphens and slashes and other word separators with white space
	text = str(text)
	text = text.replace("-", " ")
	text = text.replace("/", " ")
	text = text.replace(",", " ")
	text = text.replace(".", " ")
	text = text.replace("\n", " ")
	text = text.replace("\xa0", " ")
	text = text.replace("\x9d", " ")
	text = text.replace("’", "'")

	#2.2 remove punctuations
	text = "".join([char for char in text if char not in string.punctuation])

	#2.3 decapitalize
	text = text.lower()

	#2.4 tokenize into a list of words
	tokenized_text = re.split('\s+', text)
	tokenized_text = [text for text in tokenized_text if len(text) > 0]

	#2.5 lemmatize
	wn = nltk.WordNetLemmatizer()
	tokenized_text = [wn.lemmatize(word) for word in tokenized_text]

	return tokenized_text #returns a list

#unigrams list
course_data_df["unigrams_list"] = course_data_df["Course Name"].apply(lambda x: process_text(x)) + course_data_df["Course Description"].apply(lambda x: process_text(x))
print("\nFinished tokenizing course descriptions\n")

################################################################################################################

#3. read in keyword lists
ED_keywords = pd.read_csv("..\\Lists of Keywords\\Final ED Keywords.csv")
AI_keywords = pd.read_csv("..\\Lists of Keywords\\Final AI Keywords.csv")
AI_ED_keywords = pd.read_csv("..\\Lists of Keywords\\Final EDxAI Keywords.csv")

################################################################################################################

#4. process each keyword into tokenized words
ED_keywords["processed"] = ED_keywords["ED Keywords"].apply(lambda x: process_text(x)) #convert each row to a list of separate, processed words

AI_keywords["processed"] = AI_keywords["AI Keywords"].apply(lambda x: process_text(x))

AI_ED_keywords["processed"] = AI_ED_keywords["EDxAI Keywords"].apply(lambda x: process_text(x))

print("Finished reading in and processing keywords\n")

################################################################################################################

#5. match keywords to course descriptions

#to determine whether listA exists in listB in the exact same order
def A_is_in_B(listA, listB):

	for i in range(len(listB) - len(listA) + 1):

		if listA == listB[i:i+len(listA)]:
			return True

	return False

results_dict = {
	"School": [],
	"Course Number": [],
	"Course Name": [],
	"Only Available Within Option/Specialization": [],
	"Atypical Elective": [],
	"Course Description": [],
	"ED Match Count": [],
	"ED Keywords Matched": [],
	"AI Match Count": [],
	"AI Keywords Matched": [],
	"EDxAI Match Count": [],
	"EDxAI Keywords Matched": []
}

for ind in course_data_df.index:

	ED_matched_counter = 0
	ED_matched_keywords = []

	AI_matched_counter = 0
	AI_matched_keywords = []

	AI_ED_matched_counter = 0
	AI_ED_matched_keywords = []

	keywords_matched = False

	for keyword in ED_keywords['processed']:
		if A_is_in_B(keyword, course_data_df["unigrams_list"][ind]):
			ED_matched_counter += 1
			ED_matched_keywords.append(" ".join(keyword))
			keywords_matched = True

	for keyword in AI_keywords['processed']:
		if A_is_in_B(keyword, course_data_df["unigrams_list"][ind]):
			AI_matched_counter += 1
			AI_matched_keywords.append(" ".join(keyword))
			keywords_matched = True

	for keyword in AI_ED_keywords['processed']:
		if A_is_in_B(keyword, course_data_df["unigrams_list"][ind]):
			AI_ED_matched_counter += 1
			AI_ED_matched_keywords.append(" ".join(keyword))
			keywords_matched = True

	if keywords_matched:
		results_dict["School"].append(course_data_df["School"][ind])
		results_dict["Course Number"].append(course_data_df["Course Number"][ind])
		results_dict["Course Name"].append(course_data_df["Course Name"][ind])
		results_dict["Only Available Within Option/Specialization"].append(course_data_df["Only Available Within Option/Specialization"][ind])
		results_dict["Atypical Elective"].append(course_data_df["Atypical Elective"][ind])
		results_dict["Course Description"].append(course_data_df["Course Description"][ind])

		results_dict["ED Match Count"].append(ED_matched_counter)
		results_dict["ED Keywords Matched"].append(", ".join(ED_matched_keywords))
		results_dict["AI Match Count"].append(AI_matched_counter)
		results_dict["AI Keywords Matched"].append(", ".join(AI_matched_keywords))
		results_dict["EDxAI Match Count"].append(AI_ED_matched_counter)
		results_dict["EDxAI Keywords Matched"].append(", ".join(AI_ED_matched_keywords))

print("Finished matching keywords\n")

################################################################################################################

#6. output results to file

df = pd.DataFrame(results_dict)
df.to_csv("Keyword_Matching_Results.csv", index = False)
print("Generated keyword-matching results\n")