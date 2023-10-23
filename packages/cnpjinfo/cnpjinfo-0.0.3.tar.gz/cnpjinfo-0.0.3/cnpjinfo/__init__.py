import json
import logging
from requests import get

__version__ = '0.0.3'

def cnpjinfo(cnpj: str, retry=3):
    """
    Get CNPJ information by scraping data from the cnpj info website.

    Args:
        cnpj (str): The CNPJ (Cadastro Nacional da Pessoa Jurídica) represented as a string.

    Returns:
        dict or None: A dictionary containing information for the given CNPJ if the data is available.
                     Returns None if the data retrieval fails or if the CNPJ is not found.
    """

    logging.debug(f"Starting CNPJ {cnpj} search.")

    response = dict()
    retry = 1

    while not response and retry > 0:
        logging.debug(f"Executing data request attempt, 2 attempts remain out of {retry}.")
        response = get('https://www.receitaws.com.br/v1/cnpj/' + cnpj)
        retry -= 1

    try:
        data = response.json()
    except:
        data = None

    logging.debug(f"Data result: {json.dumps(data, indent=4)}")
    
    return data

def cnpjinfo_list(cnpj_list: list, retry=3):
    """
    Process a list of CNPJs (Cadastro Nacional da Pessoa Jurídica) and retrieve information for each CNPJ.

    Args:
        cnpj_list (list): A list of CNPJs represented as strings.

    Returns:
        list: A list containing information for each CNPJ provided in the input list.
    """
    
    cnpj_list_out = []

    for cnpj in cnpj_list:
        cnpj_data = cnpjinfo(cnpj, retry=retry)
        cnpj_list_out.append(cnpj_data)

    return cnpj_list_out
