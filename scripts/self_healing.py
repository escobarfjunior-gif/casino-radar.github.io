import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
SELF_HEALING_LOG = LOGS_DIR / "self_healing.log"
DIAGNOSIS_LOG = LOGS_DIR / "self_healing_diagnoses.jsonl"
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("SELF_HEALING_TIMEOUT", "900"))
RETRY_DELAY_SECONDS = int(os.getenv("SELF_HEALING_RETRY_DELAY", "8"))


def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"{timestamp} - self_healing - {message}"
    print(line, flush=True)
    with SELF_HEALING_LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def run_command(command: list[str], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> subprocess.CompletedProcess:
    log(f"Executando etapa: {' '.join(command)}")
    return subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def diagnose_failure(command: list[str], result: subprocess.CompletedProcess) -> dict:
    fallback = {
        "causa": "Falha não diagnosticada automaticamente.",
        "sugestao": "Verificar stderr, dependências, variáveis de ambiente e arquivos gerados.",
        "retry_recomendado": True,
        "confianca": "baixa",
    }
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return fallback

    stderr = (result.stderr or "")[-6000:]
    stdout = (result.stdout or "")[-3000:]
    prompt = f"""
Você é um diagnosticador de pipelines Python/GitHub Actions. Analise a falha abaixo e responda SOMENTE com JSON válido.

Comando: {' '.join(command)}
Exit code: {result.returncode}
STDOUT:
{stdout}
STDERR:
{stderr}

Formato obrigatório:
{{
  "causa": "causa provável em uma frase",
  "sugestao": "correção prática em uma frase",
  "retry_recomendado": true,
  "confianca": "baixa|media|alta"
}}
"""
    try:
        client = OpenAI(api_key=api_key, max_retries=2)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Você diagnostica falhas de automação de forma objetiva e retorna apenas JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            timeout=60,
        )
        content = (response.choices[0].message.content or "").strip()
        if content.startswith("```"):
            content = content.strip("`")
            content = content.replace("json\n", "", 1)
        data = json.loads(content)
        for key in ("causa", "sugestao", "retry_recomendado", "confianca"):
            if key not in data:
                data[key] = fallback[key]
        return data
    except Exception as exc:  # pragma: no cover
        fallback["causa"] = f"Falha ao consultar diagnóstico IA: {exc}"
        return fallback


def persist_diagnosis(command: list[str], result: subprocess.CompletedProcess, diagnosis: dict) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "exit_code": result.returncode,
        "diagnosis": diagnosis,
        "stderr_tail": (result.stderr or "")[-3000:],
    }
    with DIAGNOSIS_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def run_with_self_healing(command: list[str]) -> int:
    first = run_command(command)
    if first.stdout:
        print(first.stdout, end="")
    if first.returncode == 0:
        log("Etapa concluída sem necessidade de auto-cura.")
        return 0

    if first.stderr:
        print(first.stderr, file=sys.stderr, end="")
    diagnosis = diagnose_failure(command, first)
    persist_diagnosis(command, first, diagnosis)
    log(f"Diagnóstico IA: causa={diagnosis.get('causa')} | sugestão={diagnosis.get('sugestao')} | retry={diagnosis.get('retry_recomendado')}")

    if not diagnosis.get("retry_recomendado", True):
        return first.returncode

    time.sleep(RETRY_DELAY_SECONDS)
    second = run_command(command)
    if second.stdout:
        print(second.stdout, end="")
    if second.stderr:
        print(second.stderr, file=sys.stderr, end="")
    if second.returncode == 0:
        log("Auto-cura bem-sucedida após nova execução.")
    else:
        log(f"Auto-cura não resolveu a etapa. Exit code final: {second.returncode}")
    return second.returncode


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python scripts/self_healing.py <comando> [args...]", file=sys.stderr)
        sys.exit(2)
    sys.exit(run_with_self_healing(sys.argv[1:]))


if __name__ == "__main__":
    main()
