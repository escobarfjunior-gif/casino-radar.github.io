
import json
from pathlib import Path
from datetime import datetime
from logger import setup_logger
import xml.etree.ElementTree as ET

logger = setup_logger("build_sitemap", "build_sitemap.log")

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
SITEMAP_XML = DOCS_DIR / "sitemap.xml"
BASE_URL = "https://casino-radar.github.io"

def generate_sitemap():
    """Gera e atualiza o sitemap.xml com as páginas HTML existentes."""
    logger.info("Iniciando a geração do sitemap.xml...")

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Adicionar a homepage
    home_url = ET.SubElement(urlset, "url")
    ET.SubElement(home_url, "loc").text = BASE_URL
    ET.SubElement(home_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(home_url, "priority").text = "1.0"

    # Adicionar páginas estáticas (ex: contato, privacidade, termos)
    static_pages = ["contato.html", "privacidade.html", "termos.html", "metodologia.html", "analise.html", "calculadora.html", "comparador.html"]
    for page in static_pages:
        if (DOCS_DIR / page).exists():
            static_url = ET.SubElement(urlset, "url")
            ET.SubElement(static_url, "loc").text = f"{BASE_URL}/{page}"
            ET.SubElement(static_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
            ET.SubElement(static_url, "priority").text = "0.8"

    # Adicionar páginas de cassinos
    for casino_page in (DOCS_DIR / "cassinos").glob("*.html"):
        casino_url = ET.SubElement(urlset, "url")
        ET.SubElement(casino_url, "loc").text = f"{BASE_URL}/cassinos/{casino_page.name}"
        ET.SubElement(casino_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(casino_url, "priority").text = "0.9"

    # Adicionar páginas de blog (se existirem)
    for blog_page in (DOCS_DIR / "blog").glob("*.html"):
        blog_url = ET.SubElement(urlset, "url")
        ET.SubElement(blog_url, "loc").text = f"{BASE_URL}/blog/{blog_page.name}"
        ET.SubElement(blog_url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(blog_url, "priority").text = "0.7"

    # Criar a árvore XML e salvar
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0) # Formata o XML com indentação
    tree.write(SITEMAP_XML, encoding="utf-8", xml_declaration=True)

    logger.info(f"Sitemap.xml gerado com sucesso em {SITEMAP_XML}")

def main():
    generate_sitemap()

if __name__ == "__main__":
    main()
