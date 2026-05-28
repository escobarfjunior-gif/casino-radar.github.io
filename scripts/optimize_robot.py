import os
import re
import json
import requests
import time
from pathlib import Path
from openai import OpenAI

# Configurações
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
ROBOT_FILE = SCRIPTS_DIR / "robot_news.py"

def optimize_robot():
    if not ROBOT_FILE.exists():
        print("Erro: robot_news.py não encontrado.")
        return

    content = ROBOT_FILE.read_text(encoding="utf-8")

    # 1. Adicionar retry logic para requests
    if "from requests.adapters import HTTPAdapter" not in content:
        content = content.replace("import requests", "import requests\nfrom requests.adapters import HTTPAdapter\nfrom urllib3.util.retry import Retry")
        
        retry_setup = """
def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = get_session()
"""
        content = content.replace("client = OpenAI()", "client = OpenAI()\n" + retry_setup)
        content = content.replace("requests.get(", "session.get(")

    # 2. Melhorar o tratamento de erro no fetch_rss
    content = content.replace("except Exception as e:", "except requests.exceptions.RequestException as e:")

    # 3. Adicionar timeout global e tratamento de erro na IA
    content = content.replace("temperature=0.7,", "temperature=0.7,\n            timeout=60,")

    # 4. Corrigir o problema de travamento no loop principal (adicionar delay entre gerações)
    content = content.replace("articles_created += 1", "articles_created += 1\n        time.sleep(2) # Evitar rate limit")

    ROBOT_FILE.write_text(content, encoding="utf-8")
    print("✅ robot_news.py otimizado com sucesso!")

if __name__ == "__main__":
    optimize_robot()
