import requests
import os
import json
import time

from bs4 import BeautifulSoup
import pandas as pd

def can_be_float(value: str) -> bool:
    """"
    Check if a string can be converted to a float.

    Args:
        value (str): The string to check.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def scrape_page(element_id):
    """
    Scrape the NIST X-ray mass attenuation page and find the relevant values from the HTML table.

    Args:
        element_id (str): The atomic element (starting from 1) to scrape data for.
    """
    print("- Scraping atomic element ID:", element_id)
    url = f'https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z{element_id}.html'

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    tables = soup.find_all('table')
    html_table = tables[1]
    data_rows = html_table.find_all('tr')[5:]

    data = []
    for row in data_rows:
        curr_data = row.find_all('td')
        curr_data = [ele.text.strip() for ele in curr_data]

        data.append([ele for ele in curr_data if ele and can_be_float(ele)])

    return {
        "energy_MeV": [float(x[0]) for x in data],
        "mu_rho_cm2_g": [float(x[1]) for x in data],
        "mu_en_rho_cm2_g": [float(x[2]) for x in data],
    }

if __name__ == '__main__':
    print("Welcome to the Mato!")
    print("Scraping NIST X-ray mass attenuation coefficients...")
    tables_by_element_idx = {}
    for element in range(1,93):
        element_id = str(element).zfill(2)
        result = scrape_page(element_id)
        tables_by_element_idx[element_id] = result

    file_name = "nist_attenuation_coeffs"
    file_name += f"_{time.strftime('%Y%m%d_%H%M%S')}" + ".json"

    if os.path.exists(file_name):
        print(f"The file `{file_name}` already exists! Exiting...")
        exit(1)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(tables_by_element_idx, f, indent=4)

    print("Done! You can drink your coffee now.")