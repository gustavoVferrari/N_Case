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

class URLEnrichmentAgent(CorporateAgent):
    def __init__(self):
        super().__init__(
            "URLEnrichmentAgent", 
            "Especialista em Pesquisa Corporativa", 
            "Faça uma analise SWOT (Strenghts, Weaknesses, Opportunities  e Threats)"
        )

    def process(self, website):
        prompt = f"""
        Você é um agente de inteligência corporativa. Sua tarefa é encontrar informações básicas sobre a empresa na pagina: {website}.
        Caso falte informação para fazer analise SWOT, no item que nao tem informacao, complete o item com informações que sejam mais comuns nesse tipo de mercado.
        
        Retorne APENAS um JSON com os seguintes campos:
        - Strenghts: descricao dos pontos fortes da empresa
        - Weaknesses: descricao dos pontos fracos da empresa
        - Opportunities : descricao das oportunidades da empresa
        - Threats: descricao das ameaças da empresa
        
        Se não encontrar alguma informação, deixe o campo como null.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)


class ICPAgent(CorporateAgent):
    def __init__(self):
        super().__init__(
            "ICPAgent", 
            "Classificador de Publico Alvo", 
            "Com base nas informções encontradas, estime um ICP para a atividade enconomica da empresa"
        )

    def process(self, company_name, website):
        prompt = f"""
        Com base na empresa {company_name} e sua descrição: {website}, 
        classifique seus principais produtos e serviços em categorias padronizadas.
        
        Retorne APENAS um JSON com:
        - ICP: [lista do publico alvo]
        
        Seja preciso para permitir análises de similaridade futuras.
        """
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
