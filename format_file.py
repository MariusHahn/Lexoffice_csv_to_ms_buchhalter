import re
import os
import pandas
import csv

with open("/home/marius/Downloads/Export_Konten_von_2020-01-01_bis_2020-12-31.csv", encoding="UTF-16 LE", newline='\r\n' ) as f:
    text = f.read()
    #text = re.sub(r'[^"]\n', "", text)
    with open("tmp.csv", mode='w', encoding="UTF-8") as output:
        output.write(text)

with open("tmp.csv", mode="r", encoding="UTF-8") as in_file:
    text = in_file.read()
    text = re.sub(r'[^"]\n', "", text)
    with open("konten.csv", mode="w", encoding="UTF-8") as out_file:
        out_file.write(text)

os.remove("tmp.csv")

def clean_steuerkonto(text):
    return "" if pandas.isna(text) else int(text)

def text_to_int(text):
    return str(text)

def text_to_float(text):
    return float(str(text).replace(".", "").replace(",", "."))

A = pandas.read_csv("konten.csv", sep=";")

A["Kontobezeichnung"] = A["Kontobezeichnung"].apply(str)
A["Belegnummer"] = A["Belegnummer"].apply(str)
A["Text"] = A["Text"].apply(str)
A["Gegenkonto"] = A["Gegenkonto"].apply(int)
A["Soll"] = A["Soll"].apply(text_to_float)
A["Haben"] = A["Haben"].apply(text_to_float)
A["Steuer"] = A["Steuer"].apply(text_to_float)
A["Gegenkonto"] = A["Gegenkonto"].apply(text_to_int)
A["Steuerkonto"] = A["Steuerkonto"].apply(clean_steuerkonto)

A.to_csv("konten.csv", index=False, quoting=csv.QUOTE_ALL,sep=';')
