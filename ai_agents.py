import os
import json
import time
from openai import OpenAI

client = OpenAI()

class CorporateAgent:
    def __init__(self, name, role, goal):
        self.name = name
        self.role = role
        self.goal = goal

    def process(self, company_data):
        raise NotImplementedError("Subclasses must implement process method")

class EnrichmentAgent(CorporateAgent):
    def __init__(self):
        super().__init__(
            "EnrichmentAgent", 
            "Especialista em Pesquisa Corporativa", 
            "Descobrir CNPJ, site oficial e LinkedIn de empresas brasileiras"
        )

    def process(self, company_name):
        prompt = f"""
        Você é um agente de inteligência corporativa. Sua tarefa é encontrar informações básicas sobre a empresa brasileira: {company_name}.
        
        Retorne APENAS um JSON com os seguintes campos:
        - cnpj: (formato XX.XXX.XXX/XXXX-XX)
        - website: (URL oficial)
        - linkedin_url: (URL da página da empresa no LinkedIn)
        - description: (breve descrição do que a empresa faz)
        
        Se não encontrar alguma informação, deixe o campo como null.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

class StructureAgent(CorporateAgent):
    def __init__(self):
        super().__init__(
            "StructureAgent", 
            "Analista de Estrutura Societária", 
            "Identificar holdings, subsidiárias e grupos econômicos"
        )

    def process(self, company_name):
        prompt = f"""
        Analise a estrutura societária e o grupo econômico da empresa: {company_name}.
        Identifique se ela pertence a um grupo maior, se possui subsidiárias conhecidas ou marcas famosas associadas.
        
        Retorne APENAS um JSON com:
        - parent_company: (Nome da holding ou empresa controladora, se houver)
        - subsidiaries: [lista de nomes de subsidiárias ou empresas controladas]
        - brands: [lista de marcas principais]
        - economic_group: (Nome do grupo econômico)
        
        Se não houver informações claras, use null ou lista vazia.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

class ProductAgent(CorporateAgent):
    def __init__(self):
        super().__init__(
            "ProductAgent", 
            "Classificador de Produtos e Serviços", 
            "Categorizar ofertas de forma padronizada para análise de similaridade"
        )

    def process(self, company_name, description):
        prompt = f"""
        Com base na empresa {company_name} e sua descrição: {description}, 
        classifique seus principais produtos e serviços em categorias padronizadas.
        
        Retorne APENAS um JSON com:
        - main_products: [lista de produtos/serviços]
        - categories: [lista de categorias de mercado]
        - industry_segment: (segmento específico da indústria)
        
        Seja preciso para permitir análises de similaridade futuras.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
