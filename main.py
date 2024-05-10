from os import getcwd
from sheet import data_sheet
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

# uvicorn main:app --reload --port 5174 --host 127.0.0.1
# Servidor de archivos con FastAPI | Python
# template html https://codesandbox.io/p/sandbox/template-rotulo-gsz2lz?file=%2Findex.html%3A11%2C22
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.title = "API Generacion de Rotulos MyD"

app.version = "1.0.0"


@app.get("/", tags=["Home"])
async def home():
    return {"message": "Hello World"}


@app.post("/single", tags=["Excel data"])
async def upload_file(file: UploadFile = File(...)):

    if (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        with open("../read_excel/documents/" + file.filename, "wb") as my_file:  # type: ignore
            content = await file.read()
            my_file.write(content)
            my_file.close()

        return {"message": "save file Ok!"}

    return {"message": "it is not type xlsx"}


@app.get("/data/{name}", tags=["Excel data"])
async def get_data(name):

    if name == "MaestroRotulos.xlsx":

        content = data_sheet(name)
        message = "save file Ok!"
        type = "rollo"
        groups = []
        group = []
        lote = content[1][0]["LOTE"] # type: ignore

        for item in content[1]: # type: ignore
            if lote == item["LOTE"]:
                group.append(item)
            else:
                groups.append(group)
                lote = item["LOTE"]
                group = []

        return JSONResponse(
            content={
                "message": message,
                "type": type,
                "sheetName": content[0], # type: ignore
                "labels": content[2], # type: ignore
                "groups": groups,
            }
        )

    if name == "MaestroRotulosInsumos.xlsx":

        content = data_sheet(name)
        message = "save file Ok!"
        type = "insumo"
        groups = []
        group = []

        for item in content[1]: # type: ignore
            for i in range(1, 9):
                group.append(item)
            groups.append(group)
            group = []

        return JSONResponse(
            content={
                "message": message,
                "type": type,
                "sheetName": content[0], # type: ignore
                "labels": content[2], # type: ignore
                "groups": groups,
            }
        )


@app.get("/download/{name_file}")
async def download_file(name_file: str):
    root = f"../read_excel/documents/{name_file}.zip"
    return FileResponse(root)
