import json
from pathlib import Path
from logger import setup_logger
import os
from openai import OpenAI
import itertools
import time
from datetime import datetime

logger = setup_logger("generate_comparisons", "generate_comparisons.log")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
DOCS_DIR = BASE_DIR / "docs"

(DOCS_DIR / "comparativos").mkdir(parents=True, exist_ok=True)

def load_template(template_name):
    """Carrega um template HTML."""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        logger.error(f"Template não encontrado: {template_path}")
        return None
    return template_path.read_text(encoding="utf-8")

def generate_comparison_content(casino1_data, casino2_data, client):
    """Gera conteúdo de comparação entre dois cassinos usando a API da OpenAI."""
    prompt = f"""
    Você é um especialista em cassinos online e SEO. Sua tarefa é escrever uma análise comparativa detalhada e imparcial entre o cassino {casino1_data['nome']} e o cassino {casino2_data['nome']}. O conteúdo deve ter entre 1000 e 1800 palavras, ser humano, natural, útil, escaneável, legível em dispositivos móveis, único, não repetitivo, profundo, original e contextual. Inclua as seguintes seções:

    1.  **Introdução:** Apresente ambos os cassinos e o objetivo da comparação.
    2.  **Visão Geral:** Breve descrição de cada um, licenças e reputação.
    3.  **Bônus e Promoções:** Compare os bônus de boas-vindas ({casino1_data.get('bonus', 'N/A')} vs {casino2_data.get('bonus', 'N/A')}) e outras promoções.
    4.  **Seleção de Jogos:** Compare a variedade e qualidade dos jogos (slots, cassino ao vivo, etc.) e provedores de software.
    5.  **Métodos de Pagamento:** Compare os métodos de depósito e saque (foco em {', '.join(casino1_data.get('pagamentos', []))} vs {', '.join(casino2_data.get('pagamentos', []))}) e a velocidade das transações.
    6.  **Experiência do Usuário:** Compare a usabilidade do site, interface e compatibilidade móvel.
    7.  **Segurança e Suporte:** Compare as medidas de segurança e a qualidade do suporte ao cliente.
    8.  **Pontos Fortes de {casino1_data['nome']}:** Destaque os prós de {casino1_data['nome']} (use os dados de pros: {', '.join(casino1_data.get('pros', []))}).
    9.  **Pontos Fortes de {casino2_data['nome']}:** Destaque os prós de {casino2_data['nome']} (use os dados de pros: {', '.join(casino2_data.get('pros', []))}).
    10. **Veredito Final:** Qual cassino é melhor para qual tipo de jogador, com base na análise.
    11. **FAQ:** 3-5 perguntas frequentes com respostas concisas sobre a escolha entre os dois.

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
        logger.error(f"Erro ao gerar conteúdo de comparação com IA para {casino1_data['nome']} vs {casino2_data['nome']}: {e}")
        return None

def generate_comparison_page(casino1_data, casino2_data, template, client):
    """Gera uma página HTML para a comparação de dois cassinos."""
    if not template: return None

    # Gerar conteúdo completo com IA
    conteudo_completo = generate_comparison_content(casino1_data, casino2_data, client)
    if not conteudo_completo:
        logger.warning(f"Não foi possível gerar conteúdo IA para {casino1_data['nome']} vs {casino2_data['nome']}. Usando placeholder.")
        conteudo_completo = f"<p>Comparativo detalhado entre {casino1_data['nome']} e {casino2_data['nome']}.</p>"

    slug1 = casino1_data.get("slug", "")
    slug2 = casino2_data.get("slug", "")
    
    page_content = template.replace("{{ casino1.nome }}", casino1_data.get("nome", ""))
    page_content = page_content.replace("{{ casino2.nome }}", casino2_data.get("nome", ""))
    page_content = page_content.replace("{{ casino1.bonus }}", casino1_data.get("bonus", "N/A"))
    page_content = page_content.replace("{{ casino2.bonus }}", casino2_data.get("bonus", "N/A"))
    page_content = page_content.replace("{{ casino1.link }}", casino1_data.get("link", "#"))
    page_content = page_content.replace("{{ casino2.link }}", casino2_data.get("link", "#"))
    page_content = page_content.replace("{{ casino1.imagem }}", casino1_data.get("imagem", ""))
    page_content = page_content.replace("{{ casino2.imagem }}", casino2_data.get("imagem", ""))
    page_content = page_content.replace("{{ conteudo_completo }}", conteudo_completo)

    # SEO
    seo_title = f"Comparativo: {casino1_data.get('nome', '')} vs {casino2_data.get('nome', '')} | CasinoRadar"
    seo_desc = f"Análise detalhada e comparação entre {casino1_data.get('nome', '')} e {casino2_data.get('nome', '')}. Descubra qual cassino online é o melhor para você."
    seo_url = f"https://casino-radar.github.io/comparativos/{slug1}-vs-{slug2}.html"
    
    page_content = page_content.replace("{{ seo.title }}", seo_title)
    page_content = page_content.replace("{{ seo.meta_description }}", seo_desc)
    page_content = page_content.replace("{{ seo.canonical_url }}", seo_url)

    # Datas
    today = datetime.now().strftime("%Y-%m-%d")
    page_content = page_content.replace("{{ data_publicacao }}", today)
    page_content = page_content.replace("{{ data_atualizacao }}", today)

    return page_content

def main():
    logger.info("Iniciando geração de páginas de comparação...")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("Variável de ambiente OPENAI_API_KEY não configurada. A geração de conteúdo IA será limitada.")
        client = None
    else:
        client = OpenAI(api_key=api_key)

    casinos_file = DATA_DIR / "casinos.json"
    if not casinos_file.exists():
        logger.error(f"Arquivo de dados de cassinos não encontrado: {casinos_file}")
        return
    
    with open(casinos_file, "r", encoding="utf-8") as f:
        casinos_data = json.load(f)

    comparison_template = load_template("comparison_template.html")
    if not comparison_template:
        logger.error("Não foi possível carregar o template de comparação. Abortando.")
        return

    generated_count = 0
    # Gerar todas as combinações únicas de pares de cassinos
    for casino1, casino2 in itertools.combinations(casinos_data, 2):
        if "slug" not in casino1 or not casino1["slug"] or "slug" not in casino2 or not casino2["slug"]:
            logger.warning(f"Um dos cassinos no par ({casino1.get('nome', 'Desconhecido')} vs {casino2.get('nome', 'Desconhecido')}) não tem slug. Ignorando.")
            continue

        page_content = generate_comparison_page(casino1, casino2, comparison_template, client)
        if page_content:
            slug1 = casino1["slug"]
            slug2 = casino2["slug"]
            output_path = DOCS_DIR / "comparativos" / f"{slug1}-vs-{slug2}.html"
            output_path.write_text(page_content, encoding="utf-8")
            logger.info(f"Página de comparação gerada: {output_path}")
            generated_count += 1
        else:
            logger.error(f"Falha ao gerar página de comparação para {casino1.get('nome', 'Desconhecido')} vs {casino2.get('nome', 'Desconhecido')}")
        time.sleep(5) # Pequeno delay para evitar limites de taxa da API

    logger.info(f"Geração de páginas de comparação concluída. Total de {generated_count} páginas geradas.")

if __name__ == "__main__":
    main()
