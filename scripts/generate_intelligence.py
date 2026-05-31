import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from logger import setup_logger

logger = setup_logger("generate_intelligence", "generate_intelligence.log")
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
BASE_URL = "https://casino-radar.github.io"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    replacements = str.maketrans("áàãâäéèêëíìîïóòõôöúùûüç", "aaaaaeeeeiiiiooooouuuuc")
    text = text.translate(replacements)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "item"


def load_casinos() -> list[dict]:
    path = DATA_DIR / "casinos.json"
    if not path.exists():
        logger.warning("data/casinos.json não encontrado; gerando arquivos vazios.")
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("casinos") or data.get("items") or []
    if not isinstance(data, list):
        logger.warning("Formato inválido em data/casinos.json; esperado array.")
        return []
    return [item for item in data if isinstance(item, dict)]


def rating(item: dict) -> float:
    value = item.get("avaliacao", item.get("rating", 0))
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return 0.0


def safe_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str) and value.strip():
        return [part.strip() for part in value.split(",") if part.strip()]
    return []


def casino_url(item: dict) -> str:
    slug = item.get("slug") or slugify(item.get("nome") or item.get("name") or "cassino")
    return f"{BASE_URL}/cassinos/{slug}.html"


def external_domain(item: dict) -> str:
    link = item.get("link") or item.get("url") or ""
    try:
        return urlsplit(link).netloc.lower()
    except Exception:
        return ""


def build_radar_index(casinos: list[dict]) -> dict:
    indexed = []
    for position, item in enumerate(sorted(casinos, key=rating, reverse=True), start=1):
        name = item.get("nome") or item.get("name") or "Cassino"
        slug = item.get("slug") or slugify(name)
        indexed.append(
            {
                "id": slug,
                "slug": slug,
                "name": name,
                "nome": name,
                "rating": rating(item),
                "avaliacao": rating(item),
                "bonus": item.get("bonus", ""),
                "payments": safe_list(item.get("pagamentos")),
                "pagamentos": safe_list(item.get("pagamentos")),
                "category": item.get("categoria", "cassino-online"),
                "categoria": item.get("categoria", "cassino-online"),
                "description": item.get("descricao", ""),
                "descricao": item.get("descricao", ""),
                "image": item.get("imagem", ""),
                "imagem": item.get("imagem", ""),
                "url": casino_url(item),
                "link": item.get("link", casino_url(item)),
                "domain": external_domain(item),
                "rank": position,
                "search_text": " ".join(
                    [
                        str(name),
                        str(item.get("bonus", "")),
                        str(item.get("categoria", "")),
                        " ".join(safe_list(item.get("pagamentos"))),
                    ]
                ).lower(),
            }
        )
    return {"generated_at": now_iso(), "count": len(indexed), "casinos": indexed, "items": indexed}


def build_market_intelligence(casinos: list[dict]) -> dict:
    categories = Counter((item.get("categoria") or "cassino-online") for item in casinos)
    payments = Counter(payment for item in casinos for payment in safe_list(item.get("pagamentos")))
    ratings = [rating(item) for item in casinos if rating(item) > 0]
    top = sorted(casinos, key=rating, reverse=True)[:5]
    return {
        "generated_at": now_iso(),
        "summary": {
            "total_casinos": len(casinos),
            "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
            "best_rating": max(ratings) if ratings else 0,
            "categories": dict(categories),
            "payment_methods": dict(payments),
        },
        "trends": [
            "Cassinos com Pix e saques rápidos continuam sendo prioridade para usuários brasileiros.",
            "Conteúdos educativos sobre rollover, KYC e jogo responsável têm alta relevância editorial.",
            "Páginas comparativas tendem a melhorar descoberta orgânica e decisão do usuário.",
        ],
        "top_ranked": [
            {"slug": item.get("slug") or slugify(item.get("nome", "")), "name": item.get("nome", ""), "rating": rating(item)}
            for item in top
        ],
    }


def build_editorial_automation(casinos: list[dict]) -> dict:
    names = [item.get("nome") or item.get("name") for item in casinos if item.get("nome") or item.get("name")]
    suggestions = [
        {
            "type": "comparativo",
            "title": f"{a} vs {b}: qual cassino combina melhor com seu perfil?",
            "priority": "alta",
        }
        for a, b in zip(names, names[1:])
    ]
    suggestions.extend(
        [
            {"type": "guia", "title": "Como avaliar bônus de cassino sem cair em regras abusivas", "priority": "alta"},
            {"type": "guia", "title": "Pix em cassinos online: critérios de segurança antes de depositar", "priority": "media"},
            {"type": "social", "title": "Checklist de jogo responsável para publicar nas redes sociais", "priority": "media"},
        ]
    )
    return {"generated_at": now_iso(), "suggestions": suggestions[:12]}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    logger.info(f"Arquivo JSON gerado: {path}")


def main() -> None:
    casinos = load_casinos()
    radar_index = build_radar_index(casinos)
    market = build_market_intelligence(casinos)
    editorial = build_editorial_automation(casinos)

    write_json(DATA_DIR / "radar-index.json", radar_index)
    write_json(DATA_DIR / "market-intelligence.json", market)
    write_json(DATA_DIR / "editorial-automation.json", editorial)

    write_json(DOCS_DIR / "radar-index.json", radar_index)
    write_json(DOCS_DIR / "market-intelligence.json", market)
    write_json(DOCS_DIR / "editorial-automation.json", editorial)
    write_json(DOCS_DIR / "cassinos.json", radar_index)


if __name__ == "__main__":
    main()
