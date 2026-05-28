#!/usr/bin/env python3
"""
CasinoRadar - Robô de Geração Automática de Artigos
Busca notícias de fontes confiáveis sobre cassinos/apostas no Brasil
e gera novos artigos de blog com conteúdo EEAT + SEO.
Roda via GitHub Actions a cada 3 horas.
"""

import os
import re
import json
import hashlib
import unicodedata
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openai import OpenAI

# ─── Configurações ────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent
DOCS_DIR    = BASE_DIR / "docs"
BLOG_DIR    = DOCS_DIR / "blog"
BLOG_HTML   = DOCS_DIR / "blog.html"
SITEMAP_XML = DOCS_DIR / "sitemap.xml"
BASE_URL    = "https://casino-radar.github.io"
ADSENSE_ID  = "ca-pub-4896859041377751"

# OpenAI (chave via env var OPENAI_API_KEY)
client = OpenAI()

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = get_session()


# ─── Fontes RSS de notícias confiáveis ────────────────────────────────────────
RSS_SOURCES = [
    # iGaming Brasil (principal fonte do setor no Brasil)
    "https://igamingbrasil.com/feed/",
    # Jogos de Azar Brasil
    "https://www.jogosdeazar.com.br/feed/",
    # iGaming Business (global)
    "https://igamingbusiness.com/feed/",
    # CalvinAyre (notícias globais de apostas)
    "https://calvinayre.com/feed/",
    # Agência Brasil (regulação)
    "https://agenciabrasil.ebc.com.br/rss/geral/feed.xml",
    # G1 - Economia
    "https://g1.globo.com/rss/g1/economia/",
]

# Palavras-chave OBRIGATÓRIAS no título da notícia
KEYWORDS_TITLE = [
    "cassino", "casino", "aposta", "bet", "slot", "igaming", "jogo online",
    "fortune tiger", "aviator", "spaceman", "blaze", "betano", "sportingbet",
    "kto", "stake", "novibet", "betnacional", "estrelabet", "pixbet",
    "roleta", "poker", "bingo", "crash game", "jogo responsável", "gambling"
]

# Palavras-chave secundárias (corpo da notícia)
KEYWORDS = [
    "cassino", "casino", "apostas", "bet", "jogo online", "slots", "pix aposta",
    "regulação apostas", "licença bet", "bônus cassino", "jogo responsável",
    "fortune tiger", "aviator", "spaceman", "blaze", "betano", "sportingbet",
    "kto", "stake", "novibet", "betnacional", "estrelabet", "igaming"
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

# ─── Utilitários ──────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80]


def load_existing_slugs() -> set:
    return {f.stem for f in BLOG_DIR.glob("*.html")}


def fetch_rss(url: str) -> list[dict]:
    """Busca e parseia um feed RSS, retorna lista de {title, link, description, pubDate}."""
    try:
        resp = session.get(url, timeout=15, headers={"User-Agent": "CasinoRadar-Bot/1.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link")  or "").strip()
            desc  = (item.findtext("description") or "").strip()
            pub   = (item.findtext("pubDate") or "").strip()
            if title and link:
                items.append({"title": title, "link": link, "description": desc, "pubDate": pub})
        return items
    except requests.exceptions.RequestException as e:
        print(f"  [AVISO] Falha ao buscar {url}: {e}")
        return []


def is_relevant(item: dict) -> bool:
    """Verifica se a notícia é relevante para o nicho de cassinos.
    Exige que o TÍTULO contenha ao menos uma palavra-chave primária.
    """
    title = item["title"].lower()
    # Filtro estrito: palavra-chave deve estar no título
    if not any(kw in title for kw in KEYWORDS_TITLE):
        return False
    # Excluir notícias claramente fora do nicho
    exclusions = ["futebol", "eleição", "política", "crime", "tráfico",
                  "acidente", "covid", "saúde", "educação", "cultura"]
    if any(ex in title for ex in exclusions):
        return False
    return True


def collect_news(max_items: int = 5) -> list[dict]:
    """Coleta notícias relevantes de todas as fontes RSS."""
    all_items = []
    for url in RSS_SOURCES:
        print(f"  Buscando: {url}")
        items = fetch_rss(url)
        relevant = [i for i in items if is_relevant(i)]
        all_items.extend(relevant)
        if len(all_items) >= max_items * 2:
            break

    # Deduplicar por título
    seen = set()
    unique = []
    for item in all_items:
        key = hashlib.md5(item["title"].encode()).hexdigest()
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]


def generate_article(news_item: dict) -> dict | None:
    """Usa GPT para gerar um artigo completo baseado na notícia."""
    title_hint = news_item["title"]
    desc_hint  = news_item["description"][:500] if news_item["description"] else ""
    source_url = news_item["link"]

    prompt = f"""Você é um especialista em cassinos online no Brasil com 10 anos de experiência.
Baseado na notícia abaixo, escreva um artigo de blog em português brasileiro com:
- Mínimo de 900 palavras
- Tom jornalístico, informativo e confiável (EEAT: Expertise, Authoritativeness, Trustworthiness)
- SEO otimizado: use as palavras-chave naturalmente
- Estrutura: Introdução, 3-4 seções com H2, Conclusão
- Inclua dicas práticas para o leitor
- Mencione regulação brasileira (SPA/MF) quando relevante
- NÃO copie a notícia original; use-a como inspiração para criar conteúdo único
- Retorne APENAS um JSON válido com os campos:
  {{
    "title": "Título do artigo (máx 70 chars, atrativo e com keyword)",
    "slug": "slug-do-artigo-sem-acentos",
    "description": "Meta description SEO (máx 155 chars)",
    "tags": ["tag1", "tag2", "tag3"],
    "icon": "emoji único representativo",
    "html_body": "conteúdo HTML completo do artigo (apenas o interior do <main>, sem head/body)"
  }}

NOTÍCIA DE REFERÊNCIA:
Título: {title_hint}
Descrição: {desc_hint}
Fonte: {source_url}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2200,
            temperature=0.7,
            timeout=60,
        )
        raw = response.choices[0].message.content.strip()

        # Extrair JSON do response
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            print("  [ERRO] JSON não encontrado na resposta da IA")
            return None

        data = json.loads(json_match.group())
        return data

    except requests.exceptions.RequestException as e:
        print(f"  [ERRO] Falha na geração com IA: {e}")
        return None


def build_article_html(article: dict) -> str:
    """Monta o HTML completo do artigo com AdSense e template do site."""
    adsense_unit = f"""
    <!-- Bloco de Anúncio AdSense -->
    <div style="margin: 30px auto; text-align: center; max-width: 728px; background: rgba(26, 31, 58, 0.4); padding: 10px; border-radius: 8px;">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{ADSENSE_ID}"
             data-ad-slot="default"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({{}});
        </script>
    </div>"""

    tags_html = "".join(f'<span class="blog-tag">{t}</span>' for t in article.get("tags", []))
    body = article.get("html_body", "<p>Conteúdo em breve.</p>")

    # Inserir segundo bloco de AdSense antes da conclusão
    body = re.sub(
        r'(<h2[^>]*>[^<]*[Cc]onclusão[^<]*</h2>)',
        f'{adsense_unit}\n\\1',
        body
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} - CasinoRadar</title>
    <meta name="description" content="{article['description']}">
    <meta name="keywords" content="{', '.join(article.get('tags', []))}">
    <meta property="og:title" content="{article['title']}">
    <meta property="og:description" content="{article['description']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{BASE_URL}/blog/{article['slug']}.html">
    <link rel="canonical" href="{BASE_URL}/blog/{article['slug']}.html">
    <link rel="manifest" href="/manifest.json">
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_ID}"
         crossorigin="anonymous"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --primary: #d4af37;
            --primary-light: #e5c158;
            --text-primary: #e5e7eb;
            --text-secondary: #9ca3af;
            --bg-darker: #0a0e18;
            --card-bg: rgba(26, 31, 58, 0.85);
        }}
        body {{
            background: linear-gradient(135deg, var(--bg-darker) 0%, #1a1f3a 100%);
            color: var(--text-primary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 30px 20px; }}
        h1 {{ font-size: 2.4em; color: var(--primary); margin-bottom: 20px; text-align: center; line-height: 1.2; }}
        h2 {{ font-size: 1.8em; color: var(--primary-light); margin-top: 40px; margin-bottom: 15px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 10px; }}
        h3 {{ font-size: 1.4em; color: var(--text-primary); margin-top: 30px; margin-bottom: 10px; }}
        p {{ margin-bottom: 1em; font-size: 1.05em; }}
        a {{ color: #00d4ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul, ol {{ margin-left: 24px; margin-bottom: 1em; }}
        li {{ margin-bottom: 6px; font-size: 1.05em; }}
        .author-info {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(212, 175, 55, 0.1); font-size: 0.9em; color: var(--text-secondary); }}
        .date {{ display: block; margin-bottom: 20px; text-align: center; color: var(--text-secondary); font-size: 0.95em; }}
        .highlight {{ background-color: rgba(212, 175, 55, 0.1); padding: 15px; border-left: 5px solid var(--primary); margin: 25px 0; border-radius: 4px; }}
        .cta-button {{ display: block; width: fit-content; margin: 30px auto; padding: 15px 30px; background: linear-gradient(135deg, #34d399 0%, #10b981 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; transition: transform 0.3s ease, box-shadow 0.3s ease; }}
        .cta-button:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(52, 211, 153, 0.4); }}
        .source-ref {{ font-size: 0.85em; color: var(--text-secondary); margin-top: 20px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 4px; }}
    </style>
</head>
<body>
    <header style="background: rgba(26, 31, 58, 0.8); backdrop-filter: blur(10px); padding: 20px 0; border-bottom: 1px solid rgba(212, 175, 55, 0.1); margin-bottom: 40px;">
        <div class="container">
            <a href="/" style="font-size: 24px; font-weight: 800; color: var(--primary); text-decoration: none;">&#9824; CasinoRadar</a>
        </div>
    </header>
    <main class="container">
        <span class="date">{TODAY_PT}</span>
        <h1>{article['icon']} {article['title']}</h1>
        {adsense_unit}
        {body}
        <div class="source-ref">
            <strong>Fonte de referência:</strong> <a href="{article.get('source_url','#')}" target="_blank" rel="noopener noreferrer">Notícia original</a> — Conteúdo editorial independente produzido pela equipe CasinoRadar.
        </div>
        <a href="/blog.html" class="cta-button">&#8592; Voltar para o Blog</a>
        <div class="author-info">
            <p>Por equipe CasinoRadar. Publicado em {TODAY_PT}. Conteúdo informativo e independente.</p>
        </div>
    </main>
    <script>
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js').catch(() => {{}});
        }}
    </script>
</body>
</html>
"""


def add_to_blog_index(article: dict) -> None:
    """Insere o novo card do artigo no topo do blog.html."""
    tags_html = "".join(f'\n                        <span class="blog-tag">{t}</span>' for t in article.get("tags", []))
    new_card = f"""
            <!-- Artigo: {article['title']} -->
            <div class="blog-card">
                <div class="blog-header">
                    <div class="blog-icon">{article['icon']}</div>
                    <div class="blog-title">{article['title']}</div>
                    <div class="blog-date">{TODAY_PT}</div>
                </div>
                <div class="blog-content">
                    <p class="blog-excerpt">{article['description']}</p>
                    <div class="blog-meta">{tags_html}
                    </div>
                    <a href="blog/{article['slug']}.html" class="read-btn">Ler Artigo Completo</a>
                </div>
            </div>"""

    content = BLOG_HTML.read_text(encoding="utf-8")
    # Inserir após a abertura do blog-grid
    content = content.replace(
        '<div class="blog-grid">',
        f'<div class="blog-grid">{new_card}'
    )
    BLOG_HTML.write_text(content, encoding="utf-8")


def update_sitemap(slug: str) -> None:
    """Adiciona a nova URL ao sitemap.xml."""
    content = SITEMAP_XML.read_text(encoding="utf-8")
    new_url = f"""    <url>
        <loc>{BASE_URL}/blog/{slug}.html</loc>
        <lastmod>{TODAY_STR}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>"""
    content = content.replace("</urlset>", f"{new_url}\n</urlset>")
    SITEMAP_XML.write_text(content, encoding="utf-8")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print(f"CasinoRadar Robot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    existing_slugs = load_existing_slugs()
    print(f"Artigos existentes: {len(existing_slugs)}")

    print("\n[1] Coletando notícias das fontes RSS...")
    news_items = collect_news(max_items=5)
    print(f"    {len(news_items)} notícias relevantes encontradas.")

    if not news_items:
        print("    Nenhuma notícia relevante encontrada. Encerrando.")
        return

    articles_created = 0

    for i, news in enumerate(news_items, 1):
        print(f"\n[2.{i}] Processando: {news['title'][:60]}...")

        # Gerar slug provisório para verificar duplicata
        provisional_slug = slugify(news["title"])
        if provisional_slug in existing_slugs:
            print(f"    Artigo já existe ({provisional_slug}). Pulando.")
            continue

        print(f"    Gerando artigo com IA...")
        article = generate_article(news)
        if not article:
            print("    Falha na geração. Pulando.")
            continue

        # Garantir slug único
        slug = slugify(article.get("slug", provisional_slug))
        if slug in existing_slugs:
            slug = f"{slug}-{TODAY_STR}"

        article["slug"] = slug
        article["source_url"] = news["link"]

        # Salvar HTML do artigo
        html_path = BLOG_DIR / f"{slug}.html"
        html_content = build_article_html(article)
        html_path.write_text(html_content, encoding="utf-8")
        print(f"    Artigo salvo: docs/blog/{slug}.html")

        # Atualizar blog.html
        add_to_blog_index(article)
        print(f"    Card adicionado ao blog.html")

        # Atualizar sitemap
        update_sitemap(slug)
        print(f"    Sitemap atualizado")

        existing_slugs.add(slug)
        articles_created += 1
        time.sleep(2) # Evitar rate limit

        # Limitar a 2 artigos por execução para economizar créditos de IA
        if articles_created >= 2:
            print(f"\n    Limite de 2 artigos por execução atingido.")
            break

    print(f"\n{'='*60}")
    print(f"Concluído! {articles_created} novo(s) artigo(s) gerado(s).")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
