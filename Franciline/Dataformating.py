import json
import pandas as pd
df = pd.read_csv("extract/extrat_Franciline.csv", sep=';')
df_ban = pd.read_csv("extract/extrat_Franciline_to_BAN.geocoded.csv")
df_full = pd.merge(df, df_ban, on="id")
#df_full = df_full.assign(Phone = lambda x: x.replace('tel:', ''))
df_full["numero"] = df_full["numero"].apply(lambda x: str(x).replace('tel:', ''))
df_full["code_postal"] = df_full["code_postal"].apply(lambda x: str(x).replace('.0', ''))

df_full.to_csv('extract/extrat_Franciline_full.csv',encoding='utf-8-sig', index=False, header=True, sep=';')