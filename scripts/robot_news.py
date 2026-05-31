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
Crie um artigo educativo EXTREMAMENTE LONGO e aprofundado em português do Brasil para o site CasinoRadar sobre: {topic}.

REQUISITOS OBRIGATÓRIOS PARA ADSENSE (CONTEÚDO RICO):
1. EXTENSÃO: O artigo deve ter no mínimo 1500 palavras de texto útil. Seja muito detalhista em cada seção.
2. ESTRUTURA: Use pelo menos 8 subtítulos (h2) e várias subseções (h3).
3. ELEMENTOS: Inclua uma introdução longa, análise técnica de segurança, exemplos de casos reais, uma tabela HTML comparativa, um guia passo a passo e um FAQ com 6 perguntas detalhadas.
4. QUALIDADE: O texto deve ser digno de um portal de notícias de autoridade.

Responda SOMENTE com JSON válido no formato:
{{
  "title": "Título SEO de Autoridade",
  "description": "Meta descrição de alto clique (max 155 chars)",
  "body_html": "Conteúdo HTML vasto e rico (h2, h3, p, ul, li, table, strong)"
}}
"""
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"🤖 Gerando artigo via IA, tentativa {attempt}/{MAX_ATTEMPTS}...")
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "Você é um especialista em cassinos online e jogo responsável no Brasil. Sua tarefa é criar artigos educativos, aprofundados, otimizados para SEO e com alto valor para o usuário. O conteúdo deve ser objetivo, imparcial e focar em orientar o leitor sobre escolhas seguras e práticas de jogo consciente. Inclua exemplos práticos e, se possível, um pequeno FAQ no final do artigo."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.6, # Equilíbrio entre criatividade e precisão para textos longos
                max_tokens=4500, # Limite alto para garantir que o artigo não seja cortado
                timeout=120, # Aumenta o timeout para permitir respostas mais longas
            )
            content = response.choices[0].message.content or ""
            print(f"DEBUG: Conteúdo bruto da IA (primeiros 100 chars): {content[:100]}...")
            # Validação adicional para garantir que o conteúdo não seja muito curto ou genérico
            if len(content) < 500:
                raise ValueError(f"Conteúdo gerado pela IA é muito curto ({len(content)} chars).")
            data = extract_json(content)
            print(f"✅ JSON extraído com sucesso: {data.get('title')}")
            return data
        except Exception as exc:
            last_error = exc
            wait = min(90, 2 ** attempt * 10) # Aumenta o tempo de espera
            print(f"⚠️ Falha na IA: {exc}. Aguardando {wait}s antes de tentar novamente.")
            time.sleep(wait)
    print(f"❌ IA indisponível após {MAX_ATTEMPTS} tentativas: {last_error}")
    return None


def fallback_article(topic: str) -> dict:
    safe_topic = html.escape(topic)
    title = topic
    description = f"Guia educativo do CasinoRadar sobre {topic.lower()} com foco em segurança e jogo responsável. Aprenda a escolher cassinos, entender bônus e jogar de forma consciente."
    body = f"""
<h2>Introdução: A Importância de Escolhas Conscientes</h2>
<p>No universo dos cassinos online, a informação é a sua maior aliada. Este guia do CasinoRadar explora {safe_topic}, um tema crucial para garantir uma experiência de jogo segura, divertida e, acima de tudo, responsável. Entender os critérios de avaliação e as práticas recomendadas é fundamental para evitar armadilhas e maximizar sua diversão.</p>

<h2>Critérios Essenciais para Avaliar um Cassino Online</h2>
<ul>
<li><strong>Licenciamento e Regulamentação:</strong> Verifique sempre se o cassino possui licença de operação de autoridades reconhecidas (ex: MGA, Curaçao). Isso garante que a plataforma segue padrões rigorosos de segurança e justiça.</li>
<li><strong>Reputação e Avaliações de Usuários:</strong> Pesquise a reputação do cassino em fóruns e sites especializados. A experiência de outros jogadores pode oferecer insights valiosos.</li>
<li><strong>Segurança de Dados e Transações:</strong> Certifique-se de que o site utiliza criptografia SSL e outras tecnologias de proteção para seus dados pessoais e financeiros.</li>
<li><strong>Variedade e Qualidade dos Jogos:</strong> Um bom cassino oferece uma vasta gama de jogos de provedores renomados, garantindo diversão e justiça nos resultados.</li>
<li><strong>Bônus e Termos Transparentes:</strong> Bônus são atrativos, mas é vital ler os termos e condições (rollover, validade) para entender o que é exigido.</li>
<li><strong>Métodos de Pagamento Eficientes:</strong> Opte por cassinos que ofereçam métodos de depósito e saque convenientes e rápidos, como PIX, boleto e transferência bancária.</li>
<li><strong>Suporte ao Cliente:</strong> Um suporte eficiente e acessível (chat ao vivo, e-mail, telefone) é crucial para resolver dúvidas e problemas rapidamente.</li>
</ul>

<h2>Jogo Responsável: Sua Prioridade Número Um</h2>
<p>O CasinoRadar enfatiza a importância do jogo responsável. Cassinos online são formas de entretenimento, não fontes de renda. Defina limites de tempo e dinheiro, nunca jogue sob influência e procure ajuda se sentir que o jogo está se tornando um problema. Ferramentas como autoexclusão e limites de depósito são recursos valiosos oferecidos por plataformas sérias.</p>

<h2>Conclusão: Faça Escolhas Informadas</h2>
<p>A decisão de onde jogar online deve ser baseada em pesquisa e consciência. Utilize as análises e guias do CasinoRadar para fazer escolhas informadas, priorizando sempre sua segurança e bem-estar. Lembre-se: o objetivo é a diversão, com responsabilidade.</p>

<h3>FAQ Rápido</h3>
<ul>
<li><strong>Como sei se um cassino é seguro?</strong> Verifique o licenciamento, reputação e tecnologias de segurança (SSL).</li>
<li><strong>Devo aceitar todos os bônus?</strong> Leia sempre os termos e condições. Bônus podem ter requisitos de aposta altos.</li>
<li><strong>O que é jogo responsável?</strong> É jogar de forma consciente, definindo limites e buscando ajuda se necessário.</li>
</ul>
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
        h3 {{ color: #fff; margin-top: 1.5rem; }}
        ul {{ list-style-type: disc; margin-left: 20px; }}
        li {{ margin-bottom: 8px; }}
        .meta {{ color: #9ca3af; margin-bottom: 28px; }}
        .responsavel {{ border-left: 4px solid var(--primary); padding: 16px; background: rgba(212,175,55,.08); margin: 24px 0; }}
        @media (max-width: 720px) {{ article {{ padding: 24px; }} h1 {{ font-size: 2rem; }} }}
    </style>
</head>
<body>
    <div class="affiliate-banner">
        Este site contém links de afiliado. Ao clicar e fazer uma compra, podemos receber uma comissão sem custo adicional para você.
    </div>
<header><a href=\"../index.html\">♠ CasinoRadar</a> · <a href=\"../blog.html\">Blog</a></header>
<main class=\"container\">
    <article>
        <p class=\"meta\">Publicado em {now.strftime('%d/%m/%Y às %H:%M')} UTC · Conteúdo educativo · +18</p>
        <h1>{title}</h1>
        <div class=\"responsavel\"><strong>Jogue com responsabilidade:</strong> cassinos envolvem risco financeiro e não devem ser tratados como investimento ou renda garantida.</div>
        {body}
    </article>
</main>
<footer>
    <div style="margin-bottom: 15px;">
        <a href="index.html">Início</a> | 
        <a href="sobre.html">Sobre Nós</a> | 
        <a href="privacidade.html">Privacidade</a> | 
        <a href="termos.html">Termos de Uso</a> | 
        <a href="contato.html">Contato</a>
    </div>
    <p>© 2026 CasinoRadar. Conteúdo educativo sobre cassinos. Proibido para menores de 18 anos. Jogue com responsabilidade.</p>
</footer>
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
    
    # Se o slug já existe no histórico ou como arquivo, tenta variar o título
    if output.exists() or any(slugify(h) == slug for h in history):
        print(f"⚠️ Slug '{slug}' já existe. Tentando variar...")
        slug = f"{slug}-{random.randint(100, 999)}"
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
