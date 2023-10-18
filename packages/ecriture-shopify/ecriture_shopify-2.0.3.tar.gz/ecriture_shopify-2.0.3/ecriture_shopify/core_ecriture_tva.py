"""
fichier regroupant les fonctions "coeur" pour les calculs de tva de shopify
"""

# library
from typing import Tuple

import numpy as np
import pandas as pd


# constantes
# liste des colonnes du fichier de sortie 'écriture comptable'
LIST_COLS_EC = [
    "JOURNAL",
    "TYPE DE VENTE",
    "DATE",
    "GENERAL",
    "AUXILIAIRE",
    "REFERENCE",
    "LIBELLE",
    "DEBIT",
    "CREDIT",
    "PAYS",
]


def add_tva_colonne(df_0, dict_pays_tva):
    """fonction pour ajouter la colonne TVA en fonction du dict pays_tva
    A noter que l'intelligence de savoir quelle tva appliquer est en dehors de ce code.
    """
    df_1 = df_0.copy()

    # on crée la colonne tva et on applique la tva FR par défaut
    # car si pays < seuil alors tva fr (et on traite le cas principale: france uniquement)
    tva_fr = dict_pays_tva["France"]
    df_1.loc[:, "tva"] = tva_fr

    # pour chaque pays qui a un seuil défini, on lui associe.
    for country, tva_country in dict_pays_tva.items():
        if country != "France":
            df_1.loc[df_1["pays"] == country, "tva"] = tva_country
        else:
            # Si France, on ne fait rien car traité au dessus.
            pass

    return df_1


def create_summary_df(df, dict_pays_tva):
    """pour avoir un bilan par pays (et par mois car fichier mensuel)"""
    df_summary = df.groupby(["pays"], as_index=False)["ventes_ttc"].sum()
    df_summary["ventes_ttc"] = df_summary["ventes_ttc"].div(1000)

    df_summary = add_tva_colonne(df_summary, dict_pays_tva)
    df_summary = df_summary.rename(columns={"tva": "tva_appliquée"})

    return df_summary


def create_df_ecriture_comptable(df):
    """fonction principale pour créer le fichier d'écriture comptable

    rêgle de compta:
        si ventes totales >= 0: HT CREDIT, taxes CREDIT & TTC DEBIT
        si ventes totales < 0: HT DEBIT, taxes DEBIT & TTC CREDIT
    """

    # on pré-calcule ce dont on aura besoin
    df_0 = df.copy()
    df_0.loc[:, "ttc"] = df_0["ventes_ttc"]
    df_0.loc[:, "ht"] = df_0["ventes_ttc"] / (1 + df_0["tva"])
    df_0.loc[:, "taxes"] = df_0["ht"] * df_0["tva"]

    # on crée le df vide avec les colonnes d'écriture comptable
    df_1 = pd.DataFrame(columns=LIST_COLS_EC)
    df_1_ttc = pd.DataFrame(columns=LIST_COLS_EC, index=range(len(df_0)))

    # pour TTC
    df_1_ttc.loc[:, "JOURNAL"] = "VEN"
    df_1_ttc.loc[:, "TYPE DE VENTE"] = df_0["type_transaction"]
    df_1_ttc.loc[:, "DATE"] = df_0["date"]
    df_1_ttc.loc[:, "GENERAL"] = 411000
    df_1_ttc.loc[:, "AUXILIAIRE"] = ""
    df_1_ttc.loc[:, "REFERENCE"] = df_0["id_vente"].astype("int64")
    df_1_ttc.loc[:, "LIBELLE"] = (
        "ref_com" + ": " + df_0["ref_command"].astype("int64").astype(str) + " " + df_0["pays"]
    )
    df_1_ttc.loc[:, "DEBIT"] = np.where(df_0["ventes_ttc"] >= 0, df_0["ttc"], np.nan)
    df_1_ttc.loc[:, "CREDIT"] = np.where(df_0["ventes_ttc"] < 0, -df_0["ttc"], np.nan)
    df_1_ttc.loc[:, "PAYS"] = df_0["pays"]

    # pour HT
    df_1_ht = df_1_ttc.copy()
    df_1_ht.loc[:, "GENERAL"] = 70100100
    df_1_ht.loc[:, "AUXILIAIRE"] = ""
    df_1_ht.loc[:, "CREDIT"] = np.where(df_0["ventes_ttc"] >= 0, df_0["ht"], np.nan)
    df_1_ht.loc[:, "DEBIT"] = np.where(df_0["ventes_ttc"] < 0, -df_0["ht"], np.nan)

    # pour TVA
    df_1_tva = df_1_ttc.copy()
    df_1_tva.loc[:, "GENERAL"] = 44571400
    df_1_tva.loc[:, "AUXILIAIRE"] = ""
    df_1_tva.loc[:, "CREDIT"] = np.where(df_0["ventes_ttc"] >= 0, df_0["taxes"], np.nan)
    df_1_tva.loc[:, "DEBIT"] = np.where(df_0["ventes_ttc"] < 0, -df_0["taxes"], np.nan)

    # on regroupe et on trie
    df_1 = pd.concat([df_1_ttc, df_1_ht, df_1_tva], axis=0)
    df_1 = df_1.sort_values(["DATE", "REFERENCE", "LIBELLE"], ascending=[True, True, True])
    df_1 = df_1.reset_index(drop=True)

    # on clean
    df_1["DEBIT"] = df_1["DEBIT"].astype(float).div(1000)
    df_1["CREDIT"] = df_1["CREDIT"].astype(float).div(1000)

    return df_1


def create_dfs_ec_shopify(
    df_0: pd.DataFrame, dict_pays_tva: dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """function to compose the core functions to compute the TVA and écritures comptables"""

    # on calcule la TVA pour chaque pays
    df_0 = add_tva_colonne(df_0, dict_pays_tva)
    # on crée le df de sortie et on calcule la tva sur 3 lignes (TTC, HT, TVA)
    df_ec = create_df_ecriture_comptable(df_0)

    # on construit le bilan par pays (et mensuel)
    df_bilan = create_summary_df(df_0, dict_pays_tva)

    return df_ec, df_bilan


# end
