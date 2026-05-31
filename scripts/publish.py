import subprocess
import sys
from pathlib import Path

from logger import setup_logger

logger = setup_logger("publish", "publish.log")
BASE_DIR = Path(__file__).parent.parent


def run_command(command: list[str], cwd: Path = BASE_DIR, check: bool = True) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    cmd_str = " ".join(command)
    logger.info(f"Comando executado: {cmd_str}")
    if result.stdout:
        logger.info(f"Stdout: {result.stdout.strip()}")
    if result.stderr:
        logger.info(f"Stderr: {result.stderr.strip()}")
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
    return result.stdout.strip()


def resilient_pull() -> None:
    logger.info("Sincronizando com remoto usando pull resiliente...")
    run_command(["git", "config", "pull.rebase", "true"])
    try:
        run_command(["git", "pull", "origin", "main", "--no-edit"])
    except subprocess.CalledProcessError:
        logger.warning("Pull com rebase falhou; tentando merge preservando arquivos gerados locais.")
        run_command(["git", "pull", "origin", "main", "--no-rebase", "--strategy-option=ours", "--no-edit"])


def publish_to_github(commit_message: str = "🤖 CasinoRadar: Robô Supremo v2") -> bool:
    logger.info("Iniciando processo de publicação no GitHub...")
    try:
        run_command(["git", "config", "user.name", "CasinoRadar Bot"])
        run_command(["git", "config", "user.email", "bot@casino-radar.github.io"])
        run_command(["git", "add", "."])
        status_output = run_command(["git", "status", "--porcelain"])
        if not status_output:
            logger.info("Nenhuma alteração para commitar. Publicação ignorada.")
            return False
        run_command(["git", "commit", "-m", commit_message])
        resilient_pull()
        run_command(["git", "push", "origin", "main"])
        logger.info("Alterações enviadas para o GitHub com sucesso.")
        return True
    except Exception as exc:
        logger.critical(f"Falha crítica no processo de publicação: {exc}")
        return False


def main() -> None:
    message = sys.argv[1] if len(sys.argv) > 1 else "🤖 CasinoRadar: Robô Supremo v2"
    publish_to_github(message)


if __name__ == "__main__":
    main()
