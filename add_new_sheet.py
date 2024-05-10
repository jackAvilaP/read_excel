import pandas as pd

def add_sheet(sheet ,file):
    with pd.ExcelWriter(file, mode="a", engine="openpyxl") as writer:
        sheet.to_excel(writer, sheet_name="MERGE_right", index=False)
