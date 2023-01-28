import json
import pandas as pd
df = pd.read_csv("extract/extrat_Franciline.csv", sep=';')
df_ban = pd.read_csv("extract/extrat_Franciline_to_BAN.geocoded.csv")
df_full = pd.merge(df, df_ban, on="id")
df_full.to_csv('extract/extrat_Franciline_with_BAN.csv',encoding='utf-8-sig', index=False, header=True, sep=';')