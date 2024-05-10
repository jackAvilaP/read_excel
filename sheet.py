import pandas as pd
from os import remove
from cdb import generate_barcode
from add_new_sheet import add_sheet


def data_sheet(name):

    if name == "MaestroRotulos.xlsx":
        file = f"../read_excel/documents/{name}"

        with pd.ExcelFile(file) as xls:
            sheet_names = xls.sheet_names

        df_datos = pd.read_excel(file, sheet_name="DATOS", header=5)
        df_siesa = pd.read_excel(file, sheet_name="SIESA")

        df_datos = df_datos.rename(columns={"LOTE PROVEEDOR. ": "LOTE"})

        values_datos = df_datos[
            [
                "REFERENCIA.",
                "LOTE",
                "CRITERIO DE ORIGEN.",
                "CANTIDAD TOTAL.",
                "UNIDAD DE MEDIDA.",
                "ITEM.",
                "NÚMERO DE FACTURA.",
                "Resultado de análisis (Aprobado / Rechazados / Aprobado bajo Conseción).",
                "CÓDIGO (NC) MATERIA PRIMA.",
            ]
        ]

        result_right = pd.merge(df_siesa, values_datos, how="right", on="LOTE")

        barcode_cols = (
            list(result_right["ROLLO "].unique())
            + list(result_right["CÓDIGO (NC) MATERIA PRIMA."].unique())
            + list(result_right["CANTIDAD"].unique())
        )

        # for data in barcode_cols:
        #     generate_barcode(str(data))

        merge_right_dict = result_right.to_dict(orient="records")
        labels = list(merge_right_dict[0].keys())
        remove(file)

        return [sheet_names, merge_right_dict, labels]

    if name == "MaestroRotulosInsumos.xlsx":

        file = f"../read_excel/documents/{name}"

        with pd.ExcelFile(file) as xls:
            sheet_names = xls.sheet_names

        df_datos = pd.read_excel(file, sheet_name="DATOS", header=5)

        df_datos = df_datos.rename(columns={"LOTE PROVEEDOR. ": "LOTE"})

        values_datos = df_datos[
            [
                "REFERENCIA.",
                "LOTE",
                "CRITERIO DE ORIGEN.",
                "CANTIDAD TOTAL.",
                "UNIDAD DE MEDIDA.",
                "ITEM.",
                "NÚMERO DE FACTURA.",
                "Resultado de análisis (Aprobado / Rechazados / Aprobado bajo Concesión).",
                "CÓDIGO (NC) MATERIA PRIMA.",
            ]
        ]

        merge_right_dict = values_datos.to_dict(orient="records")

        merge_right_dict = [
            {key: str(value) for key, value in record.items()}
            for record in merge_right_dict
        ]

        labels = list(merge_right_dict[0].keys())
        remove(file)
        return [sheet_names, merge_right_dict, labels]


# add_sheet(result_right, file)
