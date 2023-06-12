import pandas as pd

df1 = pd.read_excel("q1_data_to_tagg.xlsx")
# df2 = pd.read_excel("q2_data_to_tagg.xlsx")
df3 = pd.read_excel("q3_data_to_tagg.xlsx")

concatenated = pd.concat([df1, df3])
# concatenated.to_csv("all_event_chosen.csv")
size = 500
list_of_dfs = [concatenated.iloc[i:i+size-1,:] for i in range(0, len(concatenated),size)]
for i, df in enumerate(list_of_dfs):
    df.to_csv('dataframe_'+str(i)+'_.csv')

