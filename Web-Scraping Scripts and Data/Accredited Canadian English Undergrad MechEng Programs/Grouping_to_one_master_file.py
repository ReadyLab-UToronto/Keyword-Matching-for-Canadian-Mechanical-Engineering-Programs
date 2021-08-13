import pandas as pd
import os

path = "C:\\Users\\jerry\\OneDrive - University of Waterloo (1)\\Co-op\\Co-op 3 - S21 - UW UofT USRA\\Webscraping Scripts and Data"
files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.startswith("Complete_") and file.endswith(".csv")]

counter = 0
dfs = []
for file in files:
	dfs.append(pd.read_csv(os.path.join(path, file)))
	print("added ", file, " to list")
	counter += 1

print("{} csv files added to list".format(counter))
print()

counter = 0
mega_df = pd.DataFrame()
for df in dfs:
	mega_df = mega_df.append(df, ignore_index=True)
	counter += 1

print("{} dataframes combined".format(counter))

print(mega_df)

mega_df.to_csv("Copy_of_All_Canadian_Accredited_MechanicalEngineering_Program_Relevant_Courses.csv", index = False)



