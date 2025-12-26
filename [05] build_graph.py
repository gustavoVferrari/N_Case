import json
import networkx as nx

def build_graph(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    G = nx.MultiDiGraph()
    cypher_commands = []
    
    # Criar nós de empresas e suas propriedades
    for comp in companies:
        name = comp['name']
        # Limpar nome para evitar erros em Cypher
        safe_name = name.replace("'", "\\'")
        
        # Comando Cypher para criar Empresa
        props = {
            'name': safe_name,
            'rank_2024': comp.get('rank_2024'),
            'sector': comp.get('sector'),
            'revenue': comp.get('revenue_brl_million'),
            'cnpj': comp.get('cnpj'),
            'website': comp.get('website'),
            'description': comp.get('description', '').replace("'", "\\'")
        }
        
        prop_str = ", ".join([f"{k}: '{v}'" for k, v in props.items() if v])
        cypher_commands.append(f"MERGE (e:Company {{name: '{safe_name}'}}) SET e += {{{prop_str}}};")
        
        # Relação com Holding/Parent
        parent = comp.get('parent_company')
        if parent:
            safe_parent = parent.replace("'", "\\'")
            cypher_commands.append(f"MERGE (p:Company {{name: '{safe_parent}'}});")
            cypher_commands.append(f"MATCH (e:Company {{name: '{safe_name}'}}), (p:Company {{name: '{safe_parent}'}}) MERGE (e)-[:BELONGS_TO]->(p);")
            
        # Relação com Grupo Econômico
        group = comp.get('economic_group')
        if group:
            safe_group = group.replace("'", "\\'")
            cypher_commands.append(f"MERGE (g:EconomicGroup {{name: '{safe_group}'}});")
            cypher_commands.append(f"MATCH (e:Company {{name: '{safe_name}'}}), (g:EconomicGroup {{name: '{safe_group}'}}) MERGE (e)-[:PART_OF_GROUP]->(g);")
            
        # Subsidiárias
        for sub in comp.get('subsidiaries', []):
            safe_sub = sub.replace("'", "\\'")
            cypher_commands.append(f"MERGE (s:Company {{name: '{safe_sub}'}});")
            cypher_commands.append(f"MATCH (e:Company {{name: '{safe_name}'}}), (s:Company {{name: '{safe_sub}'}}) MERGE (s)-[:SUBSIDIARY_OF]->(e);")
            
        # Marcas
        for brand in comp.get('brands', []):
            safe_brand = brand.replace("'", "\\'")
            cypher_commands.append(f"MERGE (b:Brand {{name: '{safe_brand}'}});")
            cypher_commands.append(f"MATCH (e:Company {{name: '{safe_name}'}}), (b:Brand {{name: '{safe_brand}'}}) MERGE (e)-[:OWNS_BRAND]->(b);")
            
        # Categorias e Produtos
        for cat in comp.get('categories', []):
            safe_cat = cat.replace("'", "\\'")
            cypher_commands.append(f"MERGE (c:Category {{name: '{safe_cat}'}});")
            cypher_commands.append(f"MATCH (e:Company {{name: '{safe_name}'}}), (c:Category {{name: '{safe_cat}'}}) MERGE (e)-[:OPERATES_IN]->(c);")

    return cypher_commands

if __name__ == "__main__":
    commands = build_graph('enriched_companies_top_30.json')
    with open('graph_database_export.cypher', 'w', encoding='utf-8') as f:
        f.write("\n".join(commands))
    print(f"Grafo gerado com {len(commands)} comandos Cypher.")
