"""
fichier regroupant les fonctions pour le fichier de sortie xlsx
"""

# library
import io
from pathlib import Path

import pandas as pd
from pandas.io.formats import excel as pd_excel


def xlsx_define_format(wkbk):
    """fonction pour definir les différents formats utilisés"""

    euro_format = wkbk.add_format(
        {"num_format": "### ### ###.00 €", "align": "center", "valign": "vcenter"}
    )
    prct_format = wkbk.add_format({"num_format": "0.00%", "align": "center", "valign": "vcenter"})
    cntr_format = wkbk.add_format({"align": "center", "valign": "vcenter"})
    # date_format = wkbk.add_format({"align": "center", "valign": "vcenter",
    ref_format = wkbk.add_format(
        {"num_format": "0000000000000", "align": "center", "valign": "vcenter"}
    )

    header_bleu = wkbk.add_format(
        {
            "bold": True,
            "font_color": "#F6F1F1",
            "fg_color": "#19A7CE",
            "border": 1,
            "border_color": "#F6F1F1",
            "align": "center",
            "valign": "vcenter",
        }
    )

    header_orange = wkbk.add_format(
        {
            "bold": True,
            "font_color": "#FAFAFA",
            "fg_color": "#FF8080",
            "border": 1,
            "border_color": "#F6F1F1",
            "align": "center",
            "valign": "vcenter",
        }
    )

    bold_format = wkbk.add_format({"bold": True, "align": "center", "valign": "vcenter"})

    return (
        euro_format,
        prct_format,
        cntr_format,
        header_bleu,
        ref_format,
        bold_format,
        header_orange,
    )


def xlsx_header_format(df_0, h_fmt, wkst):
    """fonction pour appliquer facilement le format sur le header du tableau
    (adaptation de row et de index_title dans le projet emprunt)
    """
    list_col = df_0.columns

    for col_num, data in enumerate(list_col):
        wkst.write(0, col_num, data, h_fmt)


def xlsx_generate_file(df_data: pd.DataFrame, df_groupby: pd.DataFrame, output_file: Path) -> None:
    """function to compose the xlsx_generation functions"""
    # on enregistre dans un buffer_io pour simplifier la modification xlsxwrite/pandas
    xlsx_buffer = io.BytesIO()

    # génération d'un xlsx à partir d'un df classique
    with pd.ExcelWriter(xlsx_buffer, engine="xlsxwriter") as writer:
        # to remove index and header formatting from pandas
        pd_excel.ExcelFormatter.header_style = None

        # to write df_x in worksheet
        df_data.to_excel(writer, sheet_name="données", index=False)
        df_groupby.to_excel(writer, sheet_name="bilan_par_pays", index=False)

        # format excel
        workbook = writer.book

        # format parameters
        size_col_toto = 18
        (
            money_fmt,
            prct_fmt,
            cntr_fmt,
            entete_bleu,
            ref_fmt,
            bold_fmt,
            entete_orange,
        ) = xlsx_define_format(workbook)

        # modifiying formats
        worksheet_data = writer.sheets["données"]
        worksheet_data.set_column("A:J", size_col_toto, cntr_fmt)
        worksheet_data.set_column("F:F", size_col_toto, ref_fmt)
        worksheet_data.set_column("G:G", 31, cntr_fmt)
        worksheet_data.set_column("H:I", size_col_toto, money_fmt)
        worksheet_data.set_row(0, 21)
        # xlsx_header_format(df_data, bold_fmt, worksheet_data)
        xlsx_header_format(df_data, entete_orange, worksheet_data)

        worksheet_bilan = writer.sheets["bilan_par_pays"]
        worksheet_bilan.set_column("A:A", size_col_toto, cntr_fmt)
        worksheet_bilan.set_column("B:B", size_col_toto, money_fmt)
        worksheet_bilan.set_column("C:C", size_col_toto, prct_fmt)
        worksheet_bilan.set_row(0, 21)
        xlsx_header_format(df_groupby, entete_bleu, worksheet_bilan)

    # on sauve en xlsx
    with open(output_file, "wb") as f:
        f.write(xlsx_buffer.getbuffer())

    return None


# end
