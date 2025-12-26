import json
import time
from orchestrator_market import process_company

sample_size = 30 # empresas processadas

if __name__ == "__main__":
    with open("enriched_companies_top_30.json", 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    # Processar as top - qtd = sample_size
    results = []
    for i in range(sample_size):
        res = process_company(companies[i])
        if res:
            results.append(res)
  
        time.sleep(1)
        
    with open(f'enriched_business_top_{sample_size}.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Processamento concluído para {len(results)} empresas.")
