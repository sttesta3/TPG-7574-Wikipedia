import csv
import sys
import yaml
import logging
import subprocess

DOCKER_FILE_PATH = "./docker-compose.yaml"

TOP_SIZE=20 

class ClientValidationError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def await_client_containers(client_services_name):
    result = subprocess.run(
        ["docker", "container", "wait"] + client_services_name, capture_output=True
    )

    zero_exit_code_count = 0
    for char in result.stdout.decode("utf-8"):
        if char == "0":
            zero_exit_code_count += 1

    if zero_exit_code_count != len(client_services_name):
        raise ClientValidationError("One or more clients exited with an error code")


def find_environment_variable(environment_variables, target_environment_variable):
    for environment_variable in environment_variables:
        [name, value] = environment_variable.split("=")
        if name == target_environment_variable:
            return value
    return None


def build_input_top(input_file):
    try:
        amount_by_word = {}
        with open(input_file, newline="\n") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in csv_reader:
                [fruit, amount] = row
                amount_by_word[fruit] = amount_by_word.get(fruit, 0) + int(amount)

        word_top = sorted(amount_by_word.values())
        word_top.reverse()
        return word_top
    except Exception as e:
        logging.error(e)
        raise ClientValidationError("Couldn't build input file fruit top")


def read_output_fruit_top(output_file):
    try:
        fruit_top = []
        with open(output_file, newline="\n") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            for row in csv_reader:
                [fruit, amount] = row
                fruit_top.append(FruitItem(fruit, int(amount)))
        return fruit_top
    except Exception as e:
        logging.error(e)
        raise ClientValidationError("Couldn't read output file fruit top")


def get_input_files(environment) -> list[list[str],list[str]]:
    input_fileEN = find_environment_variable(environment, "DATASETPATHEN")
    input_fileFR = find_environment_variable(environment, "DATASETPATHFR")
    total_datasetsEN = int(find_environment_variable(environment, "TOTALDATASETSEN"))
    total_datasetsFR = int(find_environment_variable(environment, "TOTALDATASETSFR"))
    dataset_inicio = int(find_environment_variable(environment, "DATASETINICIO"))

    datasetsEN = [ f".{input_fileEN}{str(dataset_inicio + i).zfill(5)}.parquet" for i in range(total_datasetsEN)]
    datasetsFR = [ f".{input_fileFR}{str(dataset_inicio + i).zfill(5)}.parquet" for i in range(total_datasetsFR)]

    return datasetsEN + datasetsFR

def run_notebook_output_to_files(input_files, id_cliente):
    # Referencia: https://www.kaggle.com/code/francobar/wikipedia-article-analysis
    import re
    import os
    import json
    import numpy
    import collections

    import nltk
    import pandas as pd
    from nltk.corpus import stopwords

    nltk.download('stopwords')

    COLUMNS_TO_DROP = ['additional_entities', 'date_created',
       'description', 'event', 'identifier',
       'infoboxes', 'is_part_of', 'license', 'main_entity',
       'references', 'tables', 'version']
    
    wiki_entry_df = None
    for file in input_files:
        df = pd.read_parquet(file)
        df = df.drop(columns=COLUMNS_TO_DROP)
        if wiki_entry_df is None:
            wiki_entry_df = df
            continue
        wiki_entry_df = pd.concat([wiki_entry_df, df])        

    def in_language_parse(in_language_column):
        if not isinstance(in_language_column, dict):
            return None
        return in_language_column.get('identifier', None)
    wiki_entry_df["in_language"] = wiki_entry_df["in_language"].apply(in_language_parse)

    def image_object_to_url(image):
        if not isinstance(image, dict):
            return None
        return image.get('content_url', None)
    wiki_entry_df["image"] = wiki_entry_df["image"].apply(image_object_to_url)

    # Query1 
    wiki_entry_df['date_modified_year'] = wiki_entry_df['date_modified'].dt.year
    wiki_entry_before_2020_df = wiki_entry_df[wiki_entry_df['date_modified_year'] <= 2020].copy()
    resultado_1 = wiki_entry_before_2020_df[wiki_entry_before_2020_df["in_language"] == "en"][["url","date_modified_year"]]
    resultado_1.to_csv(f"output/test_{id_cliente}_1.csv", index=False, header=False)

    # Query2 
    BIOGRAPHY_SECTION_NAMES = ['biographie', 'biography']
    def has_biography_section(sections):
        if not isinstance(sections, str):
            return False
        section_names =  [section.get("name", "").lower() for section in json.loads(sections)]
        for biography_section_name in BIOGRAPHY_SECTION_NAMES:
            if biography_section_name in section_names:
                return True
        return False
    wiki_entry_before_2020_df['has_biography_section'] = wiki_entry_before_2020_df['sections'].apply(has_biography_section)
    
    #Note: Actual implementation should download the image from the url
    resultado_2 = wiki_entry_before_2020_df[(wiki_entry_before_2020_df['has_biography_section'] == True)][["url", "name"]]     
    resultado_2["ubicacion_imagen"] = "/output/0/2/" + resultado_2["name"] + ".jpg"
    resultado_2.to_csv(f"output/test_{id_cliente}_2.csv", index=False, header=False)

    # Query 4 
    # Word and count of the 20 most common words in the abstract
    TOP_SIZE = 20
    WORD_REGEX = r'\b\w+\b'
    NUMBER_REGEX = r'[+-]?((\d+\.?\d*)|(\.\d+))'
    
    def extract_non_stopwords_from_abstract(abstract):
        if not isinstance(abstract, str):
            return []
        words = re.findall(WORD_REGEX, abstract.lower())
        return [word for word in words if word not in stop_words and not re.fullmatch(NUMBER_REGEX, word)]
    
    def extract_word_count(abstract):
        if not isinstance(abstract, str):
            return []
        words = re.findall(WORD_REGEX, abstract.lower())
        return len(words)
    
    stop_words = set(stopwords.words('english')) | set(stopwords.words('french'))
    words_counter = collections.Counter()
    total_words = 0 
    for abstract in wiki_entry_df['abstract'].dropna():
        non_stop_words = extract_non_stopwords_from_abstract(abstract)
        words_counter.update(set(non_stop_words))
    resultado_4 = pd.DataFrame(words_counter.most_common(TOP_SIZE), columns=["word", "count"])
    resultado_4.to_csv(f"output/test_{id_cliente}_4.csv", index=False, header=False)

    # Query 3
    # Shared words between all french and english articles in the abstract
    def fill_language_word_set(df, language):
        language_words = set()
        for abstract in df[df["in_language"] == language]['abstract'].dropna():
            language_words |= set(extract_non_stopwords_from_abstract(abstract))
        return language_words
    
    english_words = fill_language_word_set(wiki_entry_df, "en")
    french_words = fill_language_word_set(wiki_entry_df, "fr")
    shared_words = english_words & french_words
    resultado_3 = pd.Series(data=list(english_words & french_words))
    resultado_3.to_csv(f"output/test_{id_cliente}_3.csv", index=False, header=False)

def diff_files(id_query, id_cliente, sort=True) -> bool:
    archivo1 = f"output/{id_cliente}/{id_query}.csv"
    archivo2 = f"output/test_{id_cliente}_{id_query}.csv"

    if sort: 
        cmd = f"diff <(sort {archivo1}) <(sort {archivo2})"
    else:
        cmd = f"diff {archivo1} {archivo2}" 
    
    logging.info(cmd)
    result = subprocess.run(cmd, shell=True, executable='/bin/bash', capture_output=True, text=True)
    
    # Man diff(1): Devuelve 1 si los archivos son diferentes 0 si son iguales 
    if result.returncode == 2:
        logging.warning(f"diff error: {result.stderr.strip()}")
        return False
    elif result.returncode == 1:
        logging.info(f"Los archivos son diferentes:\n{result.stdout.strip()}")
        return False
    else:
        return True

def verify_client_output(client_service):
    client_name = client_service["container_name"]
    logging.info(client_name)
    environment = client_service["environment"]
    input_files = get_input_files(environment)
    client_id = find_environment_variable(environment, "ID")
    if not input_files:
        raise ClientValidationError("Bad file environment variable config")

    run_notebook_output_to_files(input_files,client_id)
    for id_query in range(1,5):
        sort = id_query != 4   # Se ordena la salida de todas las queries excepto la 4, dado que es un top
        if not diff_files(id_query, client_id, sort):
            raise ClientValidationError(f"Query {id_query} no coincidió")

    logging.info("OK")


def find_top_size(services):
    for service in services.values():
        top_size = find_environment_variable(service["environment"], "TOP_SIZE")
        if top_size:
            return int(top_size)


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        with open(DOCKER_FILE_PATH, "r") as docker_compose_file:
            parsed_docker_compose_file = yaml.safe_load(docker_compose_file)
            services = parsed_docker_compose_file["services"]
            client_services_name = list(
                filter(
                    lambda service_key: "client"
                    in services[service_key]["build"]["dockerfile"],
                    services.keys(),
                )
            )
#            top_size = find_top_size(services)
            logging.info("Awaiting client containers to exit...")
            await_client_containers(client_services_name)
            logging.info("Validating clients...")
            for client_service_name in client_services_name:
                client_service = services[client_service_name]
                verify_client_output(client_service)
            logging.info("Test was successful")
    except ClientValidationError as e:
        logging.error(e.message)
        return 1
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
