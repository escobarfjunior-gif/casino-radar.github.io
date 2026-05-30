import html
import json
import os
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
BLOG_DIR = DOCS_DIR / "blog"
HISTORY_FILE = Path(__file__).parent / "history.json"
MAX_HISTORY = 300
MAX_ATTEMPTS = 3

TOPICS = [
    "Como escolher um cassino online seguro no Brasil em 2026",
    "Cassinos com Pix: critérios de segurança antes de depositar",
    "Jogo responsável: sinais de alerta e limites práticos",
    "Bônus de cassino: como ler regras de rollover sem cair em armadilhas",
    "Slots online: volatilidade, RTP e gestão de banca",
    "Cassino ao vivo: vantagens, riscos e critérios de avaliação",
    "Verificação de identidade em cassinos: por que o KYC existe",
    "Métodos de saque em cassinos online: velocidade, taxas e segurança",
    "Como comparar cassinos online além do bônus de boas-vindas",
    "Regulamentação de apostas no Brasil: impactos para jogadores de cassino",
    "Criptografia e proteção de dados em plataformas de cassino",
    "Autoexclusão e ferramentas de controle para jogadores brasileiros",
]


def slugify(text: str) -> str:
    text = text.lower()
    replacements = {
        "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u", "ç": "c",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:75].strip("-") or "artigo-casinoradar"


def load_history() -> list[str]:
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup = HISTORY_FILE.with_suffix(".json.bak")
        HISTORY_FILE.replace(backup)
        print(f"⚠️ Histórico inválido movido para {backup.name}; iniciando histórico limpo.")
        return []

    if isinstance(data, dict):
        data = data.get("published_topics") or data.get("history") or []
    if not isinstance(data, list):
        return []

    cleaned: list[str] = []
    seen = set()
    for item in data:
        if not isinstance(item, str):
            continue
        item = item.strip()
        if not item or item.upper() == "RESTART" or item in seen:
            continue
        cleaned.append(item)
        seen.add(item)
    return cleaned[-MAX_HISTORY:]


def save_history(history: list[str]) -> None:
    HISTORY_FILE.write_text(
        json.dumps(history[-MAX_HISTORY:], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def choose_topic(history: list[str]) -> str | None:
    recent = set(history[-len(TOPICS):])
    available = [topic for topic in TOPICS if topic not in recent]
    if not available:
        # Mantém o histórico rotativo, sem gravar sentinelas do tipo RESTART.
        del history[: max(0, len(history) - MAX_HISTORY // 2)]
        available = [topic for topic in TOPICS if topic not in set(history[-len(TOPICS)//2:])]
    if not available:
        return None
    random.seed(datetime.now(timezone.utc).strftime("%Y-%m-%d-%H"))
    return random.choice(available)


def extract_json(content: str) -> dict:
    content = content.strip()
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.I | re.S)
    match = re.search(r"\{.*\}", content, flags=re.S)
    payload = match.group(0) if match else content
    data = json.loads(payload)
    required = {"title", "description", "body_html"}
    missing = required.difference(data)
    if missing:
        raise ValueError(f"JSON sem campos obrigatórios: {', '.join(sorted(missing))}")
    for key in required:
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f"Campo inválido no JSON: {key}")
    return data


def generate_with_ai(topic: str) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        print("ℹ️ OPENAI_API_KEY ausente; usando conteúdo fallback seguro.")
        return None

    client = OpenAI(api_key=api_key)
    prompt = f"""
Crie um artigo educativo em português do Brasil para o site CasinoRadar sobre: {topic}.
Responda SOMENTE com JSON válido, sem markdown, no formato:
{{
  "title": "título SEO claro",
  "description": "meta descrição com até 155 caracteres",
  "body_html": "HTML com h2, h3, p, ul e li, com tom responsável, sem prometer ganhos"
}}
O texto deve orientar, comparar critérios e reforçar jogo responsável. Não incentive apostas impulsivas.
"""
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"🤖 Gerando artigo via IA, tentativa {attempt}/{MAX_ATTEMPTS}...")
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Você escreve conteúdo educativo, responsável e otimizado para SEO sobre cassinos online."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6,
                max_tokens=2600,
                timeout=90,
            )
            content = response.choices[0].message.content or ""
            return extract_json(content)
        except Exception as exc:
            last_error = exc
            wait = min(60, 2 ** attempt * 5)
            print(f"⚠️ Falha na IA: {exc}. Aguardando {wait}s antes de tentar novamente.")
            time.sleep(wait)
    print(f"❌ IA indisponível após {MAX_ATTEMPTS} tentativas: {last_error}")
    return None


def fallback_article(topic: str) -> dict:
    safe_topic = html.escape(topic)
    title = topic
    description = f"Guia educativo do CasinoRadar sobre {topic.lower()} com foco em segurança e jogo responsável."
    body = f"""
<h2>Visão geral</h2>
<p>{safe_topic} é um tema importante para quem avalia plataformas de cassino online com mais segurança. Antes de qualquer cadastro, o jogador deve observar licença, reputação, termos de bônus, política de saque e ferramentas de controle.</p>
<h2>Critérios práticos de análise</h2>
<ul>
<li><strong>Licenciamento e transparência:</strong> verifique se a plataforma informa regras, operador responsável e canais de suporte.</li>
<li><strong>Pagamentos:</strong> confirme prazos de saque, possíveis limites e exigências de verificação de identidade.</li>
<li><strong>Bônus:</strong> leia rollover, validade, jogos elegíveis e limite máximo de conversão antes de aceitar promoções.</li>
<li><strong>Jogo responsável:</strong> dê preferência a sites com limite de depósito, pausa temporária e autoexclusão.</li>
</ul>
<h2>Como evitar problemas</h2>
<p>Não trate jogos de cassino como fonte de renda. Estabeleça orçamento, acompanhe perdas e interrompa a sessão quando houver pressão emocional. O CasinoRadar recomenda usar as informações do site apenas para educação e comparação.</p>
<h2>Conclusão</h2>
<p>Uma boa decisão depende de pesquisa, leitura cuidadosa dos termos e controle pessoal. Se a plataforma não for clara sobre segurança, saque ou suporte, o melhor caminho é procurar alternativas mais transparentes.</p>
"""
    return {"title": title, "description": description[:155], "body_html": body}


def render_article(article: dict, slug: str) -> str:
    now = datetime.now(timezone.utc)
    title = html.escape(article["title"])
    description = html.escape(article["description"][:155])
    body = article["body_html"]
    canonical = f"https://casino-radar.github.io/blog/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title} | CasinoRadar</title>
    <meta name=\"description\" content=\"{description}\">
    <link rel=\"canonical\" href=\"{canonical}\">
    <style>
        :root {{ --primary: #d4af37; --bg: #05070a; --card: #0f121d; --text: #f3f4f6; }}
        body {{ background: var(--bg); color: var(--text); font-family: Arial, sans-serif; line-height: 1.8; margin: 0; }}
        header, footer {{ background: #0f121d; padding: 24px 20px; text-align: center; }}
        a {{ color: var(--primary); }}
        .container {{ max-width: 960px; margin: 0 auto; padding: 40px 20px; }}
        article {{ background: var(--card); border: 1px solid rgba(212,175,55,.18); border-radius: 24px; padding: 42px; }}
        h1 {{ color: #fff; font-size: 2.6rem; line-height: 1.15; }}
        h2 {{ color: var(--primary); margin-top: 2rem; }}
        .meta {{ color: #9ca3af; margin-bottom: 28px; }}
        .responsavel {{ border-left: 4px solid var(--primary); padding: 16px; background: rgba(212,175,55,.08); margin: 24px 0; }}
        @media (max-width: 720px) {{ article {{ padding: 24px; }} h1 {{ font-size: 2rem; }} }}
    </style>
</head>
<body>
<header><a href=\"../index.html\">♠ CasinoRadar</a> · <a href=\"../blog.html\">Blog</a></header>
<main class=\"container\">
    <article>
        <p class=\"meta\">Publicado em {now.strftime('%d/%m/%Y às %H:%M')} UTC · Conteúdo educativo · +18</p>
        <h1>{title}</h1>
        <div class=\"responsavel\"><strong>Jogue com responsabilidade:</strong> cassinos envolvem risco financeiro e não devem ser tratados como investimento ou renda garantida.</div>
        {body}
    </article>
</main>
<footer>© 2026 CasinoRadar. Informação educativa. Jogue com responsabilidade.</footer>
</body>
</html>
"""


def update_blog_index(article: dict, slug: str) -> None:
    blog_index = DOCS_DIR / "blog.html"
    if not blog_index.exists():
        print("⚠️ docs/blog.html não encontrado; pulando atualização do índice.")
        return
    content = blog_index.read_text(encoding="utf-8")
    if f"blog/{slug}.html" in content:
        return
    card = f"""\n            <!-- Artigo automático: {slug} -->
            <div class="blog-card">
                <div class="blog-header">
                    <div class="blog-icon">🎰</div>
                    <div class="blog-title">{html.escape(article["title"])}</div>
                    <div class="blog-date">{datetime.now(timezone.utc).strftime("%d/%m/%Y")}</div>
                </div>
                <div class="blog-content">
                    <p class="blog-excerpt">{html.escape(article["description"][:180])}</p>
                    <div class="blog-meta"><span class="blog-tag">Cassinos</span><span class="blog-tag">Jogo responsável</span></div>
                    <a href="blog/{slug}.html" class="read-btn">Ler Artigo Completo</a>
                </div>
            </div>\n"""
    marker = '<div class="blog-grid">'
    if marker in content:
        content = content.replace(marker, marker + card, 1)
    else:
        content = content.replace("</main>", card + "\n</main>", 1)
    blog_index.write_text(content, encoding="utf-8")


def update_sitemap(slug: str) -> None:
    sitemap = DOCS_DIR / "sitemap.xml"
    if not sitemap.exists():
        return
    url = f"https://casino-radar.github.io/blog/{slug}.html"
    content = sitemap.read_text(encoding="utf-8")
    if url in content:
        return
    entry = f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{datetime.now(timezone.utc).date().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.70</priority>
  </url>
"""
    content = content.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(content, encoding="utf-8")


def main() -> None:
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    history = load_history()
    topic = choose_topic(history)
    if not topic:
        print("ℹ️ Nenhum tópico disponível para publicação nesta execução.")
        return

    article = generate_with_ai(topic) or fallback_article(topic)
    slug = slugify(article["title"])
    output = BLOG_DIR / f"{slug}.html"

    if output.exists():
        suffix = datetime.now(timezone.utc).strftime("%Y%m%d%H%M")
        slug = f"{slug}-{suffix}"
        output = BLOG_DIR / f"{slug}.html"

    output.write_text(render_article(article, slug), encoding="utf-8")
    update_blog_index(article, slug)
    update_sitemap(slug)

    history.append(topic)
    save_history(history)
    print(f"✅ Artigo publicado com sucesso: {output.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
