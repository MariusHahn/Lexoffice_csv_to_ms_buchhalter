import pandas
import datetime
import csv
import typing

A = pandas.read_csv("konten.csv", sep=";")

def to_ms_buchhalter_csv(df: pandas.DataFrame): 
    def soll_konto_func(s: pandas.Series) -> int:
        return s["Konto"] if s["Betrag"] >= 0 else s["Gegenkonto"]

    def haben_konto_func(series: pandas.Series) -> int:
        return series["Gegenkonto"] if series["Betrag"] >= 0 else series["Konto"]

    def betrag_func(series: pandas.Series) -> float:
        return series["Soll"] - series["Haben"]
    A = df.copy()
    
    A["Belegdatum"] = A["Datum"]
    A["Buchungsdatum"] = A["Datum"]
    A["Belegnummernkreis"] = A.apply(lambda x: "", axis=1)
    A = A.assign(Betrag=betrag_func)
    A["Sollkonto"] = A.apply(soll_konto_func, axis=1)
    A["Habenkonto"] = A.apply(haben_konto_func, axis=1)
    A["Steuerschlüssel"] = A["Steuer"]
    A["Kostenstelle 1"] = A.apply(lambda x: "", axis=1)
    A["Kostenstelle 2"] = A.apply(lambda x: "", axis=1)
    A["Währung"] = A.apply(lambda x: "", axis=1)
    A["Buchungstext"] = A["Belegnummer"] + " | " + A["Text"]
    A["Belegnummer"] = A.apply(lambda x: "", axis=1)

    A.drop(["Konto", "Kontobezeichnung", "Datum", "Text", "Gegenkonto", "Soll", "Haben", "Steuer", "Steuerkonto"], axis=1, inplace=True)
    
    A = A[[ "Belegdatum" , "Buchungsdatum" , "Belegnummernkreis" , "Belegnummer" , "Buchungstext", "Betrag" , "Sollkonto" , "Habenkonto" , "Steuerschlüssel", "Kostenstelle 1" , "Kostenstelle 2" , "Währung" ]]

    A.to_csv("konten_ms_buchhalter.csv", index=False, quoting=csv.QUOTE_ALL,sep=';')
    
to_ms_buchhalter_csv(A)

# "Konto";"Kontobezeichnung";"Datum";"Belegnummer";"Text";"Gegenkonto";"Soll";"Haben";"Steuer";"Steuerkonto"


# Belegdatum | Buchungsdatum | Belegnummernkreis | Belegnummer | Buchungstext | Betrag | Sollkonto | Habenkonto | Steuerschlüssel, Kostenstelle 1 | Kostenstelle 2 | Währung 

#print(A.groupby(["Konto", "Gegenkonto"])["Soll"].sum().head(20))
#print("----------------------------------------------------------")
#print(A.groupby(["Konto", "Gegenkonto"])["Haben"].sum().head(20))