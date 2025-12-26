import json
import time
from ai_agents import EnrichmentAgent, StructureAgent, ProductAgent

def process_company(company_basic_info):
    name = company_basic_info['name']
    print(f"Processando: {name}...")
    
    enricher = EnrichmentAgent()
    structurer = StructureAgent()
    productizer = ProductAgent()
    
    try:
        # Passo 1: Enriquecimento básico
        basic_info = enricher.process(name)
        
        # Passo 2: Estrutura societária
        structure_info = structurer.process(name)
        
        # Passo 3: Produtos e Categorias
        product_info = productizer.process(name, basic_info.get('description', ''))
        
        # Consolidar
        full_data = {
            **company_basic_info,
            **basic_info,
            **structure_info,
            **product_info
        }
        
        return full_data
    except Exception as e:
        print(f"Erro ao processar {name}: {e}")
        return None

if __name__ == "__main__":
    with open("companies_base.json", 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    # Para demonstração e teste, vamos processar as top 30 primeiro
    results = []
    for i in range(10):
        res = process_company(companies[i])
        if res:
            results.append(res)
        time.sleep(1) # Evitar rate limiting se necessário
        
    with open('enriched_companies_sample.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Processamento concluído para {len(results)} empresas.")
