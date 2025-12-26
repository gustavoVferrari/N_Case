import asyncio
from playwright.async_api import async_playwright
from markdownify import markdownify as md

async def simulate_browser_navigate(url, output_file):
    async with async_playwright() as p:
        # Inicia o navegador
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"Navegando para: {url}...")
        # Navega e espera até que a rede esteja ociosa (garante carregamento do JS)
        await page.goto(url, wait_until="networkidle")
        
        # Opcional: Esperar por um seletor específico da tabela para garantir que os dados estão lá
        await page.wait_for_selector("table")
        
        # Obtém o conteúdo HTML completo após a renderização do JavaScript
        html_content = await page.content()
        
        # Converte o HTML para Markdown
        print("Convertendo conteúdo para Markdown...")
        markdown_content = md(html_content, heading_style="ATX")
        
        # Salva o arquivo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        print(f"Sucesso! Arquivo salvo em: {output_file}")
        await browser.close()

# Execução
url_valor = "https://infograficos.valor.globo.com/valor1000/rankings/ranking-das-1000-maiores/2025"
asyncio.run(simulate_browser_navigate(url_valor, "valor1000.md" ))
