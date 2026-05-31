import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from logger import setup_logger

logger = setup_logger("deduplicate", "deduplicate.log")
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TRACKING_PREFIXES = ("utm_",)
TRACKING_PARAMS = {"fbclid", "gclid", "msclkid", "igshid", "ref", "source", "campaign"}


def normalize_text(value: object) -> str:
    value = str(value or "").strip().lower()
    value = re.sub(r"\s+", " ", value)
    return value


def clean_url(url: object) -> str:
    raw = str(url or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        key_lower = key.lower()
        if key_lower in TRACKING_PARAMS or any(key_lower.startswith(prefix) for prefix in TRACKING_PREFIXES):
            continue
        query.append((key, value))
    path = parts.path.rstrip("/") or parts.path
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def to_positive_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value) if value >= 0 else default
    text = str(value).strip().replace("%", "").replace(",", ".")
    text = re.sub(r"[^0-9.\-]", "", text)
    try:
        number = float(text)
        return number if number >= 0 else default
    except ValueError:
        return default


def get_name(item: dict) -> str:
    return str(item.get("nome") or item.get("name") or item.get("title") or "").strip()


def get_slug(item: dict) -> str:
    return str(item.get("slug") or item.get("id") or "").strip().lower()


def get_price(item: dict) -> float:
    # Suporta tanto o radar de preços do PDF quanto o schema atual de cassinos.
    for key in ("price", "preco", "valor", "deposito_min"):
        number = to_positive_float(item.get(key), 0.0)
        if number > 0:
            return number
    return 0.0


def get_discount(item: dict) -> float:
    return to_positive_float(
        item.get("custom_discount_pct")
        or item.get("discount_pct")
        or item.get("desconto")
        or item.get("avaliacao")
        or item.get("rating"),
        0.0,
    )


def valid_item(item: object) -> bool:
    if not isinstance(item, dict):
        return False
    name = get_name(item)
    if not name:
        logger.info("Item ignorado por não ter nome/título.")
        return False
    price = get_price(item)
    if any(k in item for k in ("price", "preco", "valor")) and price <= 0:
        logger.info(f"Item ignorado por preço inválido: {name}")
        return False
    return True


def is_same_offer(a: dict, b: dict) -> bool:
    slug_a, slug_b = get_slug(a), get_slug(b)
    if slug_a and slug_b and slug_a == slug_b:
        return True

    url_a, url_b = clean_url(a.get("url") or a.get("link")), clean_url(b.get("url") or b.get("link"))
    if url_a and url_b and url_a == url_b:
        return True

    name_a, name_b = normalize_text(get_name(a)), normalize_text(get_name(b))
    if not name_a or not name_b:
        return False

    name_similarity = SequenceMatcher(None, name_a, name_b).ratio()
    if name_similarity < 0.96:
        return False

    price_a, price_b = get_price(a), get_price(b)
    if price_a > 0 and price_b > 0:
        diff_ratio = abs(price_a - price_b) / max(price_a, price_b)
        return diff_ratio < 0.01

    return True


def choose_best(current: dict, candidate: dict) -> dict:
    current_score = get_discount(current)
    candidate_score = get_discount(candidate)
    if candidate_score > current_score:
        return candidate
    if candidate_score == current_score:
        current_len = len(json.dumps(current, ensure_ascii=False))
        candidate_len = len(json.dumps(candidate, ensure_ascii=False))
        if candidate_len > current_len:
            return candidate
    return current


def deduplicate_records(records: list[dict]) -> list[dict]:
    unique: list[dict] = []
    for item in records:
        if not valid_item(item):
            continue
        duplicate_index = None
        for index, existing in enumerate(unique):
            if is_same_offer(existing, item):
                duplicate_index = index
                break
        if duplicate_index is None:
            unique.append(item)
        else:
            best = choose_best(unique[duplicate_index], item)
            if best is not unique[duplicate_index]:
                logger.info(f"Duplicata substituída pela melhor oferta/registro: {get_name(item)}")
                unique[duplicate_index] = best
            else:
                logger.info(f"Duplicata descartada: {get_name(item)}")
    return unique


def load_json_array(path: Path) -> list[dict]:
    if not path.exists():
        logger.warning(f"Arquivo não encontrado: {path}")
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("casinos", "products", "items", "data"):
            if isinstance(data.get(key), list):
                return data[key]
    if isinstance(data, list):
        return data
    logger.warning(f"Formato JSON inesperado em {path}; esperado array ou envelope com lista.")
    return []


def deduplicate_file(input_file: Path = DATA_DIR / "casinos.json", output_file: Path = DATA_DIR / "casinos.json") -> None:
    logger.info(f"Iniciando deduplicação agressiva em {input_file}...")
    records = load_json_array(input_file)
    unique = deduplicate_records(records)
    if len(records) != len(unique):
        logger.info(f"Deduplicação concluída: {len(records) - len(unique)} duplicata(s) removida(s).")
    else:
        logger.info("Nenhuma duplicata encontrada.")
    output_file.write_text(json.dumps(unique, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    logger.info(f"Base deduplicada salva em {output_file} com {len(unique)} registro(s).")


def main() -> None:
    deduplicate_file()


if __name__ == "__main__":
    main()
