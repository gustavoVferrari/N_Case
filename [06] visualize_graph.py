import json
import networkx as nx
import matplotlib.pyplot as plt

def visualize_sample(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    G = nx.Graph()
    
    # Vamos pegar apenas as top 30 para a visualização não ficar poluída
    for comp in companies[:30]:
        name = comp['name']
        G.add_node(name, type='Company')
        
        # Grupo Econômico
        group = comp.get('economic_group')
        if group:
            G.add_node(group, type='Group')
            G.add_edge(name, group, relation='PART_OF')
            
        # Parent
        parent = comp.get('parent_company')
        if parent:
            G.add_node(parent, type='Company')
            G.add_edge(name, parent, relation='BELONGS_TO')
            
        # Algumas categorias para mostrar conexões de mercado
        for cat in comp.get('categories', [])[:2]:
            G.add_node(cat, type='Category')
            G.add_edge(name, cat, relation='OPERATES_IN')

    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=0.5)
    
    # Cores por tipo de nó
    node_colors = []
    for node, data in G.nodes(data=True):
        ntype = data.get('type', 'Company')
        if ntype == 'Group': node_colors.append('red')
        elif ntype == 'Category': node_colors.append('green')
        else: node_colors.append('skyblue')
        
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=8, font_weight='bold')
    plt.title("Mapa de Inteligência Corporativa - Top 30 Empresas (Amostra)")
    plt.savefig('corporate_graph_sample.png')

if __name__ == "__main__":
    visualize_sample('enriched_companies_top_30.json')
