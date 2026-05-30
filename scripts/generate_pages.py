import json
from pathlib import Path
from logger import setup_logger
import re
from datetime import datetime
import os
from openai import OpenAI
import time

logger = setup_logger("generate_pages", "generate_pages.log")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
DOCS_DIR = BASE_DIR / "docs"

# Criar diretórios de saída se não existirem
(DOCS_DIR / "cassinos").mkdir(parents=True, exist_ok=True)
(DOCS_DIR / "reviews").mkdir(parents=True, exist_ok=True)
(DOCS_DIR / "guias").mkdir(parents=True, exist_ok=True)
(DOCS_DIR / "comparativos").mkdir(parents=True, exist_ok=True)

def load_template(template_name):
    """Carrega um template HTML."""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        logger.error(f"Template não encontrado: {template_path}")
        return None
    return template_path.read_text(encoding="utf-8")

def generate_ai_content(casino_data, client):
    """Gera conteúdo detalhado para o cassino usando a API da OpenAI."""
    prompt = f"""
    Você é um especialista em cassinos online e SEO. Sua tarefa é escrever uma análise detalhada e imparcial sobre o cassino {casino_data['nome']}. O conteúdo deve ter entre 1000 e 1800 palavras, ser humano, natural, útil, escaneável, legível em dispositivos móveis, único, não repetitivo, profundo, original e contextual. Inclua as seguintes seções:

    1.  **Introdução:** Apresente o cassino {casino_data['nome']} e o que o torna especial.
    2.  **Visão Geral:** Detalhes sobre a plataforma, licença, reputação e anos de operação.
    3.  **Recursos e Jogos:** Tipos de jogos disponíveis (slots, cassino ao vivo, jogos de mesa), provedores de software e experiência de jogo.
    4.  **Bônus e Promoções:** Detalhes sobre o bônus de boas-vindas ({casino_data.get('bonus', 'N/A')}), promoções regulares e requisitos de aposta.
    5.  **Métodos de Pagamento:** Explique os métodos de depósito e saque, com foco em {', '.join(casino_data.get('pagamentos', []))} e a velocidade das transações.
    6.  **Segurança e Suporte:** Medidas de segurança (criptografia SSL), licenciamento e qualidade do suporte ao cliente.
    7.  **Pontos Positivos:** Liste os principais benefícios de jogar no {casino_data['nome']} (use os dados de pros: {', '.join(casino_data.get('pros', []))}).
    8.  **Pontos Negativos:** Liste as desvantagens ou áreas de melhoria (use os dados de cons: {', '.join(casino_data.get('cons', []))}).
    9.  **Comparação (Opcional):** Breve comparação com um concorrente popular, se relevante.
    10. **FAQ:** 3-5 perguntas frequentes com respostas concisas.
    11. **Conclusão:** Resumo final e recomendação.

    Formate o conteúdo usando tags HTML (h2, h3, p, ul, li, strong, em). Garanta que o texto seja otimizado para SEO, com palavras-chave relevantes distribuídas naturalmente. O tom deve ser profissional e informativo.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini", # Ou gpt-4.1-nano, gemini-2.5-flash
            messages=[
                {"role": "system", "content": "Você é um assistente de escrita de conteúdo para SEO e cassinos online."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Erro ao gerar conteúdo com IA para {casino_data['nome']}: {e}")
        return None

def generate_casino_page(casino_data, template, client):
    """Gera uma página HTML para um cassino específico."""
    if not template: return None

    # Gerar conteúdo completo com IA
    descricao_completa = generate_ai_content(casino_data, client)
    if not descricao_completa:
        logger.warning(f"Não foi possível gerar conteúdo IA para {casino_data['nome']}. Usando placeholder.")
        # Fallback para conteúdo placeholder se a IA falhar
        descricao_completa = (
            f"<p>{casino_data.get('descricao', '')}</p>\n"
            f"<p>Este é um texto de exemplo para preencher o conteúdo da página do cassino {casino_data['nome']}. "
            f"Aqui você encontrará informações detalhadas sobre bônus, métodos de pagamento, jogos disponíveis e muito mais. "
            f"Nosso objetivo é fornecer uma análise completa e imparcial para ajudar você a tomar a melhor decisão.</p>\n"
            f"<h2>Bônus e Promoções</h2>\n"
            f"<p>O cassino {casino_data['nome']} oferece um bônus de boas-vindas de {casino_data.get('bonus', 'N/A')}. "
            f"Além disso, existem promoções regulares para jogadores existentes, incluindo rodadas grátis e bônus de recarga.</p>\n"
            f"<h2>Métodos de Pagamento</h2>\n"
            f"<p>Você pode depositar e sacar usando {', '.join(casino_data.get('pagamentos', []))}. "
            f"O PIX é uma opção rápida e segura para transações no Brasil.</p>\n"
            f"<h2>Segurança e Licenciamento</h2>\n"
            f"<p>O cassino {casino_data['nome']} é licenciado e regulamentado por autoridades respeitadas, "
            f"garantindo um ambiente de jogo seguro e justo para todos os jogadores.</p>\n"
            f"<h2>Pontos Positivos</h2>\n<ul>{''.join([f'<li>{p}</li>' for p in casino_data.get('pros', [])])}</ul>\n"
            f"<h2>Pontos Negativos</h2>\n<ul>{''.join([f'<li>{c}</li>' for c in casino_data.get('cons', [])])}</ul>\n"
            f"<h3>FAQ</h3>\n"
            f"<p><strong>É seguro jogar no {casino_data['nome']}?</strong> Sim, o cassino possui licença e criptografia SSL.</p>\n"
            f"<p><strong>Quais jogos estão disponíveis?</strong> Slots, jogos de mesa, cassino ao vivo e muito mais.</p>\n"
        )

    # Substituições no template
    page_content = template.replace("{{ casino.nome }}", casino_data.get("nome", ""))
    page_content = page_content.replace("{{ casino.slug }}", casino_data.get("slug", ""))
    page_content = page_content.replace("{{ casino.bonus }}", casino_data.get("bonus", "N/A"))
    page_content = page_content.replace("{{ casino.avaliacao }}", str(casino_data.get("avaliacao", "N/A")))
    page_content = page_content.replace("{{ casino.pagamentos }}", ", ".join(casino_data.get("pagamentos", [])))
    page_content = page_content.replace("{{ casino.imagem }}", casino_data.get("imagem", ""))
    page_content = page_content.replace("{{ casino.descricao_curta }}", casino_data.get("descricao", ""))
    page_content = page_content.replace("{{ casino.link }}", casino_data.get("link", "#"))
    page_content = page_content.replace("{{ casino.conteudo_completo }}", descricao_completa)

    # SEO
    seo_title = f"{casino_data.get('nome', '')} - Análise Completa e Bônus | CasinoRadar"
    seo_desc = f"Análise detalhada do cassino {casino_data.get('nome', '')}: bônus, jogos, métodos de pagamento e segurança. Encontre o melhor cassino online para você."
    seo_url = f"https://casino-radar.github.io/cassinos/{casino_data.get('slug', '')}.html"
    
    page_content = page_content.replace("{{ seo.title }}", seo_title)
    page_content = page_content.replace("{{ seo.meta_description }}", seo_desc)
    page_content = page_content.replace("{{ seo.canonical_url }}", seo_url)
    
    # Datas
    today = datetime.now().strftime("%Y-%m-%d")
    page_content = page_content.replace("{{ data_publicacao }}", today)
    page_content = page_content.replace("{{ data_atualizacao }}", today)

    return page_content

def main():
    logger.info("Iniciando geração de páginas HTML...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("Variável de ambiente OPENAI_API_KEY não configurada. A geração de conteúdo IA será limitada.")
        client = None
    else:
        client = OpenAI(api_key=api_key)

    # Carregar dados de cassinos
    casinos_file = DATA_DIR / "casinos.json"
    if not casinos_file.exists():
        logger.error(f"Arquivo de dados de cassinos não encontrado: {casinos_file}")
        return
    
    with open(casinos_file, "r", encoding="utf-8") as f:
        casinos_data = json.load(f)

    # Carregar template de cassino
    casino_template = load_template("casino_template.html")
    if not casino_template:
        logger.error("Não foi possível carregar o template de cassino. Abortando.")
        return

    generated_count = 0
    for casino in casinos_data:
        if "slug" not in casino or not casino["slug"]:
            logger.warning(f"Cassino sem slug, ignorando: {casino.get('nome', 'Desconhecido')}")
            continue

        page_content = generate_casino_page(casino, casino_template, client)
        if page_content:
            output_path = DOCS_DIR / "cassinos" / f"{casino['slug']}.html"
            output_path.write_text(page_content, encoding="utf-8")
            logger.info(f"Página gerada: {output_path}")
            generated_count += 1
        else:
            logger.error(f"Falha ao gerar página para o cassino: {casino.get('nome', 'Desconhecido')}")
        time.sleep(5) # Pequeno delay para evitar limites de taxa da API

    logger.info(f"Geração de páginas HTML concluída. Total de {generated_count} páginas geradas.")

if __name__ == "__main__":
    main()
