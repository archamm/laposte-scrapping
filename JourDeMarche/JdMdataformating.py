import pandas as pd
from tqdm import tqdm


df = pd.read_csv("JourDeMarche/extract/extrat_JdM_012023.csv")
df = df.drop_duplicates(subset=['name', 'horaires'], keep='first')
df = df[df["adress"].str.contains("produits en|environ") == False]
df = df[df["name"].str.contains("produits en") == False]
df = df[df["horaires"].str.contains("Ce marché a lieu") == True]
df['adress'] = df['adress'].replace('None', 'centre-ville')



df.to_csv('JourDeMarche/extract/extrat_JdM_022023_v1.2.csv',encoding='utf-8-sig', index=False, header=True)