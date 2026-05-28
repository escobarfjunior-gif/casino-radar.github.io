#!/usr/bin/env python3
"""
CasinoRadar - Robô de Geração Automática de Artigos BULLETPROOF (v6)
Focado em estabilidade absoluta, recuperação de erros e performance.
"""

import os
import re
import json
import hashlib
import unicodedata
import logging
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI

# ─── Configuração de Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("robot_debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Desabilitar avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Configurações ────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
DOCS_DIR    = BASE_DIR / "docs"
BLOG_DIR    = DOCS_DIR / "blog"
BLOG_HTML   = DOCS_DIR / "blog.html"
SITEMAP_XML = DOCS_DIR / "sitemap.xml"
BASE_URL    = "https://casino-radar.github.io"
ADSENSE_ID  = "ca-pub-4896859041377751"

# ─── Sessão de Requests Resiliente ───────────────────────────────────────────
def get_resilient_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

http = get_resilient_session()

# ─── Fontes RSS de notícias confiáveis ────────────────────────────────────────
RSS_SOURCES = [
    "https://igamingbusiness.com/feed/",
    "https://calvinayre.com/feed/",
    "https://agenciabrasil.ebc.com.br/rss/geral/feed.xml",
    "https://g1.globo.com/rss/g1/economia/",
    "https://www.gamesmagazinebrasil.com/rss/",
]

KEYWORDS_TITLE = [
    "cassino", "casino", "aposta", "bet", "slot", "igaming", "jogo online",
    "fortune tiger", "aviator", "spaceman", "blaze", "betano", "sportingbet",
    "kto", "stake", "novibet", "betnacional", "estrelabet", "pixbet",
    "roleta", "poker", "bingo", "crash game", "jogo responsável", "gambling",
    "brasil", "regulação", "licença", "pix", "fazenda", "spa"
]

TODAY = date.today()
TODAY_STR = TODAY.strftime("%Y-%m-%d")
TODAY_PT  = TODAY.strftime("%-d de %B de %Y").replace(
    "January","janeiro").replace("February","fevereiro").replace(
    "March","março").replace("April","abril").replace(
    "May","maio").replace("June","junho").replace(
    "July","julho").replace("August","agosto").replace(
    "September","setembro").replace("October","outubro").replace(
    "November","novembro").replace("December","dezembro")

# ─── Funções Core ─────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    try:
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = re.sub(r"[^\w\s-]", "", text.lower())
        text = re.sub(r"[\s_]+", "-", text)
        text = re.sub(r"-+", "-", text).strip("-")
        return text[:80]
    except Exception:
        return hashlib.md5(text.encode()).hexdigest()[:10]

def fetch_rss(url: str) -> list[dict]:
    try:
        resp = http.get(url, timeout=20, headers={"User-Agent": "CasinoRadar-Bot/2.0"}, verify=False)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link")  or "").strip()
            desc  = (item.findtext("description") or "").strip()
            if title and link:
                items.append({"title": title, "link": link, "description": desc})
        return items
    except Exception as e:
        logger.warning(f"Falha ao buscar RSS {url}: {e}")
        return []

def is_relevant(item: dict) -> bool:
    title = item["title"].lower()
    if not any(kw in title for kw in KEYWORDS_TITLE):
        return False
    exclusions = ["futebol", "crime", "acidente", "covid", "saúde", "morte"]
    if any(ex in title for ex in exclusions):
        return False
    return True

def generate_article_safe(news_item: dict, client: OpenAI) -> dict | None:
    prompt = f"""Especialista em iGaming Brasil. Escreva artigo SEO (900+ palavras) sobre:
Título: {news_item['title']}
Fonte: {news_item['link']}

Requisitos:
1. Tom profissional (EEAT).
2. Estrutura HTML (H2, H3, P, UL).
3. JSON estrito: {{"title":"", "slug":"", "description":"", "tags":[], "icon":"", "html_body":""}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500,
            temperature=0.7,
            timeout=120
        )
        raw = response.choices[0].message.content.strip()
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match: return None
        return json.loads(json_match.group())
    except Exception as e:
        logger.error(f"Erro na IA: {e}")
        return None

def update_files_safe(article: dict):
    try:
        # 1. Salvar Artigo
        slug = article['slug']
        html_path = BLOG_DIR / f"{slug}.html"
        
        # Template simplificado e robusto
        html_content = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>{article['title']}</title>
        <meta name="description" content="{article['description']}"><link rel="stylesheet" href="../style.css"></head>
        <body><main class="container"><h1>{article['icon']} {article['title']}</h1>{article['html_body']}</main></body></html>"""
        
        html_path.write_text(html_content, encoding="utf-8")
        
        # 2. Atualizar Blog Index (Prevenir corrupção de arquivo)
        if BLOG_HTML.exists():
            content = BLOG_HTML.read_text(encoding="utf-8")
            if '<div class="blog-grid">' in content:
                new_card = f'<!-- {slug} --><div class="blog-card"><h3>{article["title"]}</h3><p>{article["description"]}</p><a href="blog/{slug}.html">Ler mais</a></div>'
                content = content.replace('<div class="blog-grid">', f'<div class="blog-grid">{new_card}')
                BLOG_HTML.write_text(content, encoding="utf-8")
        
        logger.info(f"Arquivos atualizados para: {slug}")
        return True
    except Exception as e:
        logger.error(f"Erro ao atualizar arquivos: {e}")
        return False

# ─── Execução Principal com Proteção Global ──────────────────────────────────
def main():
    logger.info("Iniciando Robô Bulletproof...")
    try:
        # Garantir diretórios
        BLOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # API Client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY não configurada!")
            return
        client = OpenAI(api_key=api_key)

        # Coleta
        news = []
        for src in RSS_SOURCES:
            items = fetch_rss(src)
            news.extend([i for i in items if is_relevant(i)])
            if len(news) >= 10: break
            
        if not news:
            logger.info("Sem notícias novas relevantes.")
            return

        # Processamento
        created = 0
        existing = {f.stem for f in BLOG_DIR.glob("*.html")}
        
        for item in news:
            slug = slugify(item['title'])
            if slug in existing: continue
            
            logger.info(f"Gerando: {item['title']}")
            article = generate_article_safe(item, client)
            
            if article:
                article['slug'] = slug
                if update_files_safe(article):
                    created += 1
                    existing.add(slug)
            
            if created >= 2: break
            time.sleep(5) # Delay anti-bloqueio

        logger.info(f"Sucesso! {created} artigos criados.")
        
    except Exception as e:
        logger.critical(f"FALHA CRÍTICA NO ROBÔ: {e}", exc_info=True)
        # Opcional: Enviar alerta via Webhook aqui

if __name__ == "__main__":
    main()
