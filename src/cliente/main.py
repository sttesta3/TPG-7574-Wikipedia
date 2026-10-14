import os
import pandas as pd
from mensajes import DataMensaje

FILE = os.environ["FILE"]
GATEWAYHOST = os.environ["GATEWAYHOST"]
GATEWAYPORT = os.environ["GATEWAYPORT"]

def _sendParquet() -> None:
    dataset =  pd.read_parquet(FILE)
    
    for fila in dataset.itertuples():
        DataMensaje(fila).send(socket="")
        break

def main():
    _sendParquet()

if __name__ == "__main__":
    main()