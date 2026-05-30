
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import json
import time
import unicodedata
import re
from pathlib import Path
from logger import setup_logger

logger = setup_logger('fetch_data', 'fetch_data.log')

# Configurações
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# URLs de exemplo para coleta (estas precisarão ser refinadas ou substituídas por fontes reais)
# Para o MVP, vamos simular a coleta de alguns dados.
EXAMPLE_SOURCES = [
    "https://www.example.com/casino-reviews", # Exemplo: site de reviews de cassinos
    "https://www.example.com/promotions",    # Exemplo: site de promoções
]

def get_resilient_session():
    """Cria uma sessão de requests com retries e backoff."""
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

http = get_resilient_session()

def slugify(text):
    """Converte texto em um slug amigável para URL."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text

def fetch_and_parse_data(url):
    """Busca uma URL e tenta extrair dados de cassinos."""
    logger.info(f"Buscando dados de: {url}")
    try:
        response = http.get(url, timeout=10) # Timeout para evitar travamentos
        response.raise_for_status() # Levanta HTTPError para códigos de status ruins (4xx ou 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Lógica de extração de dados (placeholder) ---
        # Esta parte precisará ser adaptada para cada fonte de dados real.
        # Por enquanto, vamos simular alguns dados.
        casinos_data = []
        if "casino-reviews" in url:
            # Simula a extração de 2 cassinos
            casinos_data.append({
                "nome": "Casino Teste 1",
                "bonus": "100% até R$200",
                "avaliacao": 4.5,
                "pagamentos": ["PIX", "Boleto"],
                "imagem": "https://via.placeholder.com/150",
                "descricao": "Um cassino divertido para iniciantes.",
                "categoria": "cassino-online",
                "link": "https://www.example.com/casino1",
                "pros": ["Bônus generoso", "Interface amigável"],
                "cons": ["Poucos jogos de mesa"]
            })
            casinos_data.append({
                "nome": "Casino Teste 2",
                "bonus": "50% até R$100",
                "avaliacao": 4.0,
                "pagamentos": ["Visa", "Mastercard"],
                "imagem": "https://via.placeholder.com/150",
                "descricao": "Focado em slots e jogos rápidos.",
                "categoria": "slots",
                "link": "https://www.example.com/casino2",
                "pros": ["Grande variedade de slots", "Saques rápidos"],
                "cons": ["Bônus menor", "Suporte limitado"]
            })
        elif "promotions" in url:
            # Simula a extração de 1 promoção
            casinos_data.append({
                "nome": "Promoção de Verão",
                "bonus": "Gire a roleta e ganhe!",
                "avaliacao": 0, # Não aplicável para promoção
                "pagamentos": [],
                "imagem": "https://via.placeholder.com/150",
                "descricao": "Promoção especial de verão com prêmios diários.",
                "categoria": "promocao",
                "link": "https://www.example.com/promocao-verao",
                "pros": ["Prêmios diários"],
                "cons": ["Requisitos de aposta altos"]
            })

        # Normalização e adição de slug
        for casino in casinos_data:
            casino["slug"] = slugify(casino["nome"])

        return casinos_data

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Erro inesperado ao processar {url}: {e}")
        return []

def main():
    logger.info("Iniciando coleta de dados...")
    all_casinos_data = []
    for source_url in EXAMPLE_SOURCES:
        data = fetch_and_parse_data(source_url)
        if data:
            all_casinos_data.extend(data)
            logger.info(f"Coletados {len(data)} itens de {source_url}")
        time.sleep(1) # Pequeno delay entre as requisições

    # Salvar dados em JSON estruturado
    output_file = DATA_DIR / "casinos.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_casinos_data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados salvos em {output_file} com {len(all_casinos_data)} itens.")

    # Para o MVP, vamos criar um arquivo de promoções e reviews também, mesmo que vazios por enquanto
    with open(DATA_DIR / "promocoes.json", 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    with open(DATA_DIR / "reviews.json", 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    logger.info("Arquivos promocoes.json e reviews.json criados (vazios).")

    logger.info("Coleta de dados concluída.")

if __name__ == "__main__":
    main()
