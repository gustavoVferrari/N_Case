import json
import time
from ai_agents_market import URLEnrichmentAgent, ICPAgent

def process_company(company_basic_info):
    website = company_basic_info['website']
    name = company_basic_info['name']
    print(f"Processando: {name}...")
    
    urlenricher = URLEnrichmentAgent()
    icp = ICPAgent()
    
    try:
        # Passo 1: Enriquecimento básico
        website_info = urlenricher.process(website)        
        
        # Passo 3: Produtos e Categorias
        icp_info = icp.process(name, website)
        
        # Consolidar
        full_data = {
            'website': website,
            'name': name,
            **website_info,
            **icp_info
        }
        
        return full_data
    except Exception as e:
        print(f"Erro ao processar {name}: {e}")
        return None

if __name__ == "__main__":
    with open("enriched_companies_sample.json", 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    # Para demonstração e teste, vamos processar as top 30 primeiro
    results = []
    for i in range(10):
        res = process_company(companies[i])
        if res:
            results.append(res)
        time.sleep(1) # Evitar rate limiting se necessário
        
    with open('enriched_business_sample.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Processamento concluído para {len(results)} empresas.")
