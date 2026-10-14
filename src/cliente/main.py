import os
import pandas as pd

file = os.environ["FILE"]

def sendParquet() -> None:
    dataset =  pd.read_parquet(file)
    print(dataset.head())


def main():
    sendParquet()


if __name__ == "__main__":
    main()