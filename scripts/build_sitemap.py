from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

from logger import setup_logger

logger = setup_logger("build_sitemap", "build_sitemap.log")
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
SITEMAP_XML = DOCS_DIR / "sitemap.xml"
BASE_URL = "https://casino-radar.github.io"

STATIC_PAGES = [
    "contato.html",
    "privacidade.html",
    "termos.html",
    "metodologia.html",
    "analise.html",
    "calculadora.html",
    "comparador.html",
    "blog.html",
]

SECTIONS = [
    ("cassinos", "0.90"),
    ("comparativos", "0.82"),
    ("reviews", "0.75"),
    ("guias", "0.75"),
    ("blog", "0.70"),
]


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def add_url(urlset: ET.Element, seen: set[str], loc: str, priority: str, changefreq: str = "weekly") -> None:
    loc = loc.strip()
    if not loc or loc in seen:
        return
    seen.add(loc)
    node = ET.SubElement(urlset, "url")
    ET.SubElement(node, "loc").text = loc
    ET.SubElement(node, "lastmod").text = today()
    ET.SubElement(node, "changefreq").text = changefreq
    ET.SubElement(node, "priority").text = priority


def generate_sitemap() -> None:
    logger.info("Iniciando geração defensiva do sitemap.xml...")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    seen: set[str] = set()

    add_url(urlset, seen, BASE_URL, "1.00", "daily")

    for page in STATIC_PAGES:
        if (DOCS_DIR / page).exists():
            add_url(urlset, seen, f"{BASE_URL}/{page}", "0.80", "weekly")

    for section, priority in SECTIONS:
        section_dir = DOCS_DIR / section
        if not section_dir.exists():
            continue
        for html_file in sorted(section_dir.glob("*.html")):
            add_url(urlset, seen, f"{BASE_URL}/{section}/{html_file.name}", priority, "weekly")

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_XML, encoding="utf-8", xml_declaration=True)
    logger.info(f"Sitemap gerado com {len(seen)} URL(s) única(s) em {SITEMAP_XML}.")


def main() -> None:
    try:
        from generate_intelligence import main as generate_intelligence_main

        generate_intelligence_main()
    except Exception as exc:
        logger.warning(f"Não foi possível gerar JSONs de inteligência antes do sitemap: {exc}")
    generate_sitemap()


if __name__ == "__main__":
    main()
