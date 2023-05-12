import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def flottype(df,cols):
    for col in cols:
        df[col]=df[col].fillna(0)
        df[col]=df[col].replace(",",".",regex=True)
        df[col]=df[col].astype(float)
    return df

def strtype(df,cols):
    for col in cols:
        df[col]=df[col].astype(str)
    return df
def adress(df):
    df["adresse_Postal"]=df["adresse_numero"]+" "+df["adresse_nom_voie"]+" "+df["nom_commune"]+" "+df["code_postal"]
    df["coldep"]=df['code_departement']
    return df

def drop(df,cols):
    df=df.drop(columns=cols)
    return df
def typecoldep(df,coldep):
    df[coldep]=df[coldep].replace('2A',96,regex=True)
    df[coldep]=df[coldep].replace('2B',97,regex=True)
    df[coldep]=df[coldep].astype(float)
    return df
def natureCulture(df,nature,col="nature_culture"):
    df[col]=df[col].map(lambda x :nature[x]if x in nature else x)
    return df

@st.cache(allow_output_mutation=True)
def prepro(df):
    flotcol=[ 'lot1_surface_carrez',
       'lot2_surface_carrez',
       'lot3_surface_carrez',
        'lot4_surface_carrez',
        'lot5_surface_carrez',
        'nombre_lots',
        'surface_reelle_bati',
        'nombre_pieces_principales',
        'surface_terrain',
        'valeur_fonciere']
    localisation=['adresse_numero', 'adresse_suffixe',
       'adresse_nom_voie', 'adresse_code_voie', 'code_postal', 'code_commune',
       'nom_commune', 'code_departement', 'ancien_code_commune',
       'ancien_nom_commune','longitude', 'latitude']
    delete=["adresse_numero","adresse_nom_voie","nom_commune","code_postal",'adresse_suffixe', 'adresse_code_voie',
       'code_commune', 'code_departement', 'ancien_code_commune',
       'ancien_nom_commune','ancien_id_parcelle', 'numero_volume','id_parcelle','code_type_local','code_nature_culture','code_nature_culture_speciale','lot1_numero', 'lot2_numero', 'lot3_numero','lot4_numero','lot5_numero']
    nature={
        "AB":" terrains à bâtir",
        "AG":" terrains d’agrément",
        "B": "bois",
        "BF":" futaiesfeuillues",
        "BM":" futaies mixtes",
        "BO": "oseraies",
        "BP": "peupleraies",
        "BR":" futaies résineuses",
        "BS":" taillis sous futaie",
        "BT":" taillis simples",
        "CA": "carrières",
        "CH":" chemin de fer",
        "E": "eaux",
        "J": "jardins",
        "L": "landes",
        "LB":" landes boisées",
        "P": "prés",
        "PA": "pâtures",
        "PC": "pacages",
        "PE":" prés d’embouche",
        "PH": "herbages",
        "PP":" prés plantes",
        "S": "sols",
        "T": "terres",
        "TP":" terres plantées",
        "VE": "vergers",
        "VI": "vignes"
    }
    df=flottype(df,flotcol)
    df=strtype(df,localisation)
    df=adress(df)
    df=drop(df,delete)
    df=typecoldep(df,"coldep")
    df=natureCulture(df,nature)
    df["date_mutation"]=pd.to_datetime(df["date_mutation"])
    df=df.sort_values('date_mutation').reset_index(drop=True)
    return df