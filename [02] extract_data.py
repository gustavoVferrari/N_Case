import pandas as pd
from bs4 import BeautifulSoup
import json

def extract_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')
    
    if not table: 
      

        return None

    rows = []
    for tr in table.find_all('tr')[1:]: # Pular o cabeçalho
        cols = tr.find_all('td')
        if len(cols) >= 6:
            row = {
                'rank_2024': cols[0].get_text(strip=True),
                'rank_2023': cols[1].get_text(strip=True),
                'name': cols[2].get_text(strip=True),
                'headquarters': cols[3].get_text(strip=True),
                'sector': cols[4].get_text(strip=True),
                'revenue_brl_million': cols[5].get_text(strip=True)
            }
            rows.append(row)
    
    return rows


def extract_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    data = []
    start_table = False
    for line in lines:
        if '| --- |' in line:
            start_table = True
            continue
        if start_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            # Formato esperado: | | rank24 | rank23 | name | sede | setor | receita |
            if len(parts) >= 8:
                data.append({
                    'rank_2024': parts[2],
                    'rank_2023': parts[3],
                    'name': parts[-3],
                    'headquarters': parts[5],
                    'sector': parts[6],
                    'revenue_brl_million': parts[7]
                })
    return data

md_path = 'valor1000.md'
companies = extract_from_markdown(md_path)

with open("companies_base.json", 'w', encoding='utf-8') as f:
    json.dump(companies, f, ensure_ascii=False, indent=4)

print(f'Extraídas {len(companies)} empresas.')