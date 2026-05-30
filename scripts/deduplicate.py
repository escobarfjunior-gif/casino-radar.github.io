
import json
import hashlib
from pathlib import Path
from logger import setup_logger

logger = setup_logger("deduplicate", "deduplicate.log")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

def calculate_hash(data):
    """Calcula um hash SHA256 de um dicionário de dados."""
    # Converte o dicionário para uma string JSON ordenada para garantir hash consistente
    json_string = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(json_string.encode("utf-8")).hexdigest()

def deduplicate_casinos(input_file=DATA_DIR / "casinos.json", output_file=DATA_DIR / "casinos.json"):
    """Remove cassinos duplicados com base no slug e no hash do conteúdo."""
    logger.info(f"Iniciando deduplicação de cassinos em {input_file}...")
    if not input_file.exists():
        logger.warning(f"Arquivo de entrada não encontrado: {input_file}. Pulando deduplicação.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        all_casinos = json.load(f)

    unique_casinos = []
    seen_slugs = set()
    seen_hashes = set()

    for casino in all_casinos:
        slug = casino.get("slug")
        content_hash = calculate_hash(casino) # Hash de todo o conteúdo do cassino

        if slug and slug in seen_slugs:
            logger.info(f"Cassino com slug duplicado encontrado e ignorado: {slug}")
            continue
        if content_hash in seen_hashes:
            logger.info(f"Cassino com conteúdo duplicado encontrado e ignorado (hash: {content_hash}).")
            continue

        unique_casinos.append(casino)
        if slug: seen_slugs.add(slug)
        seen_hashes.add(content_hash)

    if len(all_casinos) != len(unique_casinos):
        logger.info(f"Deduplicação concluída: {len(all_casinos) - len(unique_casinos)} duplicatas removidas.")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(unique_casinos, f, ensure_ascii=False, indent=4)
        logger.info(f"Dados deduplicados salvos em {output_file}.")
    else:
        logger.info("Nenhuma duplicata encontrada.")

def main():
    deduplicate_casinos()

if __name__ == "__main__":
    main()
