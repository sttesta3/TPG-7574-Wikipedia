import re
import ast
import nltk
import pandas as pd
from nltk.corpus import stopwords
from collections import namedtuple

DATASETPATHEN = "datasets/enwiki_namespace_0_"
DATASETPATHFR = "datasets/frwiki_namespace_0_"
TOTALDATASETS = 1

WORD_REGEX = r'\b\w+\b'
NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'

def _seccionATexto(documento: str) -> tuple[str, bool]:
    bio = False
    textoSeccion = ""
    try:
        for seccion in ast.literal_eval(documento):
            for parrafo in seccion["has_parts"]:
                if parrafo["type"] == "paragraph":
                    textoSeccion += parrafo["value"] 
            if seccion["name"].lower() == "biography" or seccion["name"].lower() == "biographie": 
                bio = True
    except Exception:
        pass

    return (textoSeccion, bio)

def _resumenAPalabras(resumen: str) -> dict[str]:
    palabrasSinStop = {}
    palabras = re.findall(WORD_REGEX, resumen.lower())
    for palabra in palabras:
        if palabra not in set(stopwords.words('english')) | set(stopwords.words('french')) and not re.fullmatch(NUMBER_REGEX, palabra):
            palabrasSinStop[palabra] = 1
    return palabrasSinStop


def query2(fila: namedtuple) -> int:
    if fila.date_modified.year <= 2020:
        texto, bio = _seccionATexto(fila.sections)
        if bio:
            print(fila.name)
            return 1
    return 0


top = {}
def query4(fila: namedtuple) -> None:
    global top
    texto, bio = _seccionATexto(fila.sections)
    palabras = _resumenAPalabras(texto)
    print(palabras)

    for clave, valor in palabras.items():
        top[clave] = top.get(clave, 0) + valor



def main() -> None:
    for i in range(TOTALDATASETS):
        datasetEn = pd.read_parquet(DATASETPATHEN + str(i).zfill(5) + ".parquet")
        datasetFr = pd.read_parquet(DATASETPATHFR + str(i).zfill(5) + ".parquet")

        dataset = pd.concat([datasetEn, datasetFr])

        i = 0
        for fila in dataset.itertuples():
            i += query2(fila)
            #query4(fila)

        print(i)
            
        #global top
        #print(sorted(top.items(), key=lambda item: item[1], reverse=True)[:20])


if __name__ == "__main__":
    main()