# Plataforma de Inteligência Corporativa: Universo Empresarial Brasileiro

Este projeto demonstra o poder de **Agentes de IA** trabalhando em conjunto para transformar dados brutos em um **Mapa Vivo de Inteligência Corporativa**.

## Metodologia e Orquestração de Agentes de IA

A construção desta plataforma fundamentou-se na orquestração de múltiplos agentes de inteligência artificial, cada qual com responsabilidades específicas e complementares. A partir da extração inicial dos dados do ranking Valor 1000, o sistema acionou o **EnrichmentAgent**, encarregado de localizar dados cadastrais críticos como CNPJs, domínios oficiais e perfis corporativos no LinkedIn. Simultaneamente, o **StructureAgent** atuou na análise de estruturas societárias, identificando relações de controle entre holdings e subsidiárias que muitas vezes não são evidentes em dados superficiais. Por fim, o **ProductAgent** realizou a categorização semântica de ofertas, permitindo que produtos descritos de formas distintas fossem agrupados em categorias de mercado padronizadas, facilitando análises de similaridade e concorrência.

## Modelagem e Estrutura do Graph Database

A escolha por um banco de dados orientado a grafos justifica-se pela necessidade de representar a complexidade das interconexões corporativas brasileiras. O modelo implementado utiliza uma arquitetura de nós e arestas que permite consultas multidimensionais. Os nós principais representam entidades como **Company**, **EconomicGroup**, **Brand** e **Category**. As relações estabelecidas, como **BELONGS_TO** e **SUBSIDIARY_OF**, permitem o rastreamento imediato de cadeias de comando, enquanto a relação **OPERATES_IN** revela clusters de mercado onde empresas de diferentes grupos competem ou colaboram. Esta estrutura transforma dados tabulares estáticos em um ecossistema dinâmico de informações.

| Tipo de Relação | Descrição | Impacto na Análise |
| --- | --- | --- |
| **BELONGS_TO** | Vincula a empresa operacional à sua holding controladora. | Identificação de concentração de poder econômico. |
| **SUBSIDIARY_OF** | Define a hierarquia direta entre empresas do mesmo grupo. | Mapeamento de estruturas de subsidiárias integrais ou parciais. |
| **OWNS_BRAND** | Associa marcas comerciais às entidades jurídicas responsáveis. | Visibilidade de portfólio de marcas e presença de mercado. |
| **OPERATES_IN** | Conecta a empresa a categorias de produtos e serviços. | Análise de similaridade e descoberta de novos concorrentes. |

## Insights Estratégicos e Conexões Reveladas

A análise do grafo gerado permitiu a descoberta de conexões que transcendem a simples classificação setorial. Observou-se, por exemplo, a vasta rede de influência da **JBS**, cujas operações são centralizadas pela holding **J&F Investimentos**, abrangendo desde o processamento de proteínas até serviços financeiros. Outro insight relevante é a interdependência entre a **Cosan** e a **Raízen**, revelando como grandes grupos utilizam joint ventures para dominar o setor de energia e biocombustíveis. Essas conexões demonstram que o ecossistema corporativo brasileiro é altamente integrado, onde empresas de setores aparentemente distintos, como varejo e logística, frequentemente compartilham a mesma base de controle econômico.

## Documentação e Entregáveis do Projeto

A entrega final deste desafio compreende um conjunto de ativos técnicos que permitem a reprodução e expansão do sistema de inteligência corporativa.

| Arquivo | Descrição | Finalidade |
| --- | --- | --- |
| **graph_database_export.cypher** | Script de exportação para Graph Database. | Popular bancos de dados como Neo4j com nós e relações. |
| **enriched_companies_top50.json** | Base de dados enriquecida das top 50 empresas. | Fornecer dados estruturados para análises externas. |
| **corporate_graph_sample.png** | Visualização gráfica da rede de conexões. | Demonstrar visualmente a complexidade do ecossistema. |
| **ai_agents.py** | Código fonte dos agentes de inteligência. | Permitir a manutenção e evolução da lógica de descoberta. |
| **orchestrator.py** | Sistema de gestão e execução dos agentes. | Orquestrar o fluxo de trabalho entre os diferentes agentes. |
