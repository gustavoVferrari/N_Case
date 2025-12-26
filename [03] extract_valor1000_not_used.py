import json
import re

def extract_from_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()    

    lines = content.split('\n')
    data = []
    
    for line in lines:
        # Limpar espaços extras no início e fim
        clean_line = line.strip()
        if not clean_line:
            continue
            
        # Dividir por tabulação ou múltiplos espaços
        parts = re.split(r'\t+', clean_line)
        
        # Se não houver tabs, tentar por espaços múltiplos (o markdown pode ter convertido tabs em espaços)
        if len(parts) < 6:
            parts = re.split(r'\s{2,}', clean_line)
            
        if len(parts) >= 6:
            # Validar se os primeiros elementos são números (ranks)
            if parts[0].isdigit():
                data.append({
                    'rank_2024': parts[0],
                    'rank_2023': parts[1],
                    'name': parts[2],
                    'headquarters': parts[3],
                    'sector': parts[4],
                    'revenue_brl_million': parts[5]
                })
    
    return data

md_path = r'valor1000.md'
companies = extract_from_text(md_path)

# Se ainda estiver vazio, vamos tentar uma abordagem baseada em regex
if not companies:
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Regex para capturar o padrão: rank rank nome sede setor receita
    matches = re.findall(r'(\d+)\s+(\d+|-)\s+(.*?)\s+([A-Z]{2})\s+(.*?)\s+([\d.,]+)', content)
    for m in matches:
        companies.append({
            'rank_2024': m[0],
            'rank_2023': m[1],
            'name': m[2],
            'headquarters': m[3],
            'sector': m[4],
            'revenue_brl_million': m[5]
        })

with open('companies_base.json', 'w', encoding='utf-8') as f:
    json.dump(companies, f, ensure_ascii=False, indent=4)

print(f'Extraídas {len(companies)} empresas.')
