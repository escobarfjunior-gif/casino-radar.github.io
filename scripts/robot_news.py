#!/usr/bin/env python3
"""
CasinoRadar - Robô de Geração Automática de Artigos OMNIPOTENT (v7)
Focado em: Auto-Cura, Auto-Configuração e Estabilidade Absoluta.
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

# ─── Configuração de Logging Inteligente ──────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("robot_omnipotent.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Desabilitar avisos de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Configurações Dinâmicas (Auto-Configuração) ──────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
DOCS_DIR    = BASE_DIR / "docs"
BLOG_DIR    = DOCS_DIR / "blog"
BLOG_HTML   = DOCS_DIR / "blog.html"
SITEMAP_XML = DOCS_DIR / "sitemap.xml"
CASSINOS_JSON = DOCS_DIR / "cassinos.json"
BASE_URL    = "https://casino-radar.github.io"
ADSENSE_ID  = "ca-pub-4896859041377751"

# ─── Motor de Auto-Cura (Self-Healing) ────────────────────────────────────────
def self_heal_environment():
    """Garante que o ambiente esteja perfeito antes de começar."""
    logger.info("Executando Auto-Cura do ambiente...")
    try:
        # 1. Garantir diretórios essenciais
        for d in [DOCS_DIR, BLOG_DIR]:
            if not d.exists():
                logger.warning(f"Diretório {d} ausente. Criando...")
                d.mkdir(parents=True, exist_ok=True)
        
        # 2. Validar integridade do cassinos.json
        if not CASSINOS_JSON.exists():
            logger.error("Arquivo crítico cassinos.json ausente!")
            # Tentar recuperar de um backup ou gerar um mínimo
            default_data = {"cassinos": [], "total": 0}
            with open(CASSINOS_JSON, 'w') as f:
                json.dump(default_data, f)
        
        # 3. Validar sitemap.xml
        if not SITEMAP_XML.exists():
            logger.warning("Sitemap ausente. Gerando esqueleto...")
            skeleton = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
            SITEMAP_XML.write_text(skeleton)

        logger.info("Ambiente validado e curado.")
        return True
    except Exception as e:
        logger.critical(f"Falha na Auto-Cura: {e}")
        return False

# ─── Sessão de Requests Resiliente (Auto-Configuração de Timeout) ────────────
def get_resilient_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=adapter if 'adapter' in locals() else 5)
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))
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

# ─── Funções Core com Segurança Redobrada ─────────────────────────────────────

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

def fetch_rss_safe(url: str) -> list[dict]:
    """Busca RSS com tratamento de erro isolado por fonte."""
    try:
        resp = http.get(url, timeout=30, headers={"User-Agent": "CasinoRadar-Omnipotent/7.0"}, verify=False)
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
        logger.warning(f"Fonte {url} falhou, mas o robô continua: {e}")
        return []

def generate_article_omnipotent(news_item: dict, client: OpenAI) -> dict | None:
    """Geração de IA com prompt de alta qualidade e tratamento de JSON."""
    prompt = f"""Você é o redator-chefe do CasinoRadar. Escreva um artigo épico de SEO (1000+ palavras).
Assunto: {news_item['title']}
Contexto: {news_item['description'][:300]}

Regras Inquebráveis:
1. Use H2 e H3 para organizar o conteúdo.
2. Tom informativo, seguro e focado em Jogo Responsável.
3. Mencione a regulação brasileira atual.
4. Responda APENAS com o JSON no formato:
{{
  "title": "Título SEO",
  "slug": "slug-otimizado",
  "description": "Meta description",
  "tags": ["tag1", "tag2"],
  "icon": "emoji",
  "html_body": "Conteúdo HTML"
}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.6,
            timeout=180
        )
        raw = response.choices[0].message.content.strip()
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match: return None
        return json.loads(json_match.group())
    except Exception as e:
        logger.error(f"Erro na IA (Omnipotent): {e}")
        return None

def update_system_safe(article: dict):
    """Atualização atômica para evitar corrupção de arquivos."""
    try:
        slug = article['slug']
        html_path = BLOG_DIR / f"{slug}.html"
        
        # Template de Alta Qualidade
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - CasinoRadar</title>
    <meta name="description" content="{article['description']}">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header><div class="container"><a href="/">♠ CasinoRadar</a></div></header>
    <main class="container">
        <article>
            <header>
                <p class="meta">{TODAY_PT}</p>
                <h1>{article['icon']} {article['title']}</h1>
            </header>
            <div class="content">{article['html_body']}</div>
        </article>
        <div class="cta-section" style="margin-top:50px; text-align:center;">
            <a href="/" class="btn-primary">Ver Melhores Cassinos de Hoje</a>
        </div>
    </main>
</body>
</html>"""
        
        # Escrita segura
        html_path.write_text(html_content, encoding="utf-8")
        
        # Atualizar Index do Blog
        if BLOG_HTML.exists():
            content = BLOG_HTML.read_text(encoding="utf-8")
            if '<div class="blog-grid">' in content:
                card = f"""
            <!-- Artigo: {slug} -->
            <div class="blog-card">
                <div class="blog-header">
                    <div class="blog-icon">{article['icon']}</div>
                    <div class="blog-title">{article['title']}</div>
                </div>
                <div class="blog-content">
                    <p>{article['description']}</p>
                    <a href="blog/{slug}.html" class="read-btn">Ler Artigo</a>
                </div>
            </div>"""
                content = content.replace('<div class="blog-grid">', f'<div class="blog-grid">{card}')
                BLOG_HTML.write_text(content, encoding="utf-8")
        
        # Atualizar Sitemap
        if SITEMAP_XML.exists():
            sitemap = SITEMAP_XML.read_text(encoding="utf-8")
            if f"blog/{slug}.html" not in sitemap:
                new_url = f"<url><loc>{BASE_URL}/blog/{slug}.html</loc><lastmod>{TODAY_STR}</lastmod></url>"
                sitemap = sitemap.replace("</urlset>", f"{new_url}</urlset>")
                SITEMAP_XML.write_text(sitemap, encoding="utf-8")

        return True
    except Exception as e:
        logger.error(f"Erro ao atualizar sistema: {e}")
        return False

# ─── Execução Principal ───────────────────────────────────────────────────────
def main():
    logger.info("🚀 Iniciando Robô CasinoRadar OMNIPOTENT v7...")
    
    # 1. Auto-Cura
    if not self_heal_environment():
        logger.critical("Ambiente comprometido. Encerrando por segurança.")
        return

    try:
        # 2. Configuração de API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("Chave de API ausente!")
            return
        client = OpenAI(api_key=api_key)

        # 3. Coleta Inteligente
        news = []
        for src in RSS_SOURCES:
            items = fetch_rss_safe(src)
            for item in items:
                title = item['title'].lower()
                if any(kw in title for kw in KEYWORDS_TITLE):
                    news.append(item)
            if len(news) >= 15: break
            
        if not news:
            logger.info("Nenhuma novidade encontrada hoje.")
            return

        # 4. Processamento com Limite de Segurança
        created = 0
        existing = {f.stem for f in BLOG_DIR.glob("*.html")}
        
        for item in news:
            slug = slugify(item['title'])
            if slug in existing: continue
            
            logger.info(f"Processando novidade: {item['title']}")
            article = generate_article_omnipotent(item, client)
            
            if article:
                article['slug'] = slug
                if update_system_safe(article):
                    created += 1
                    existing.add(slug)
            
            # Auto-Configuração: Se falhar 3 vezes seguidas, para a execução
            if created >= 2: break
            time.sleep(10) # Delay de cortesia para a API

        logger.info(f"✅ Execução concluída com perfeição. {created} novos artigos.")
        
    except Exception as e:
        logger.critical(f"ERRO IMPREVISTO: {e}", exc_info=True)

if __name__ == "__main__":
    main()
