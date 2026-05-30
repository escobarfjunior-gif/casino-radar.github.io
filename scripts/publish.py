
import subprocess
from logger import setup_logger
from pathlib import Path

logger = setup_logger("publish", "publish.log")

BASE_DIR = Path(__file__).parent.parent

def run_command(command, cwd=BASE_DIR):
    """Executa um comando shell e retorna a saída, ou levanta um erro."""
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
        cmd_str = " ".join(command)
        logger.info(f"Comando executado: {cmd_str}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        cmd_str = " ".join(command)
        logger.error(f"Erro ao executar comando: {cmd_str}")
        logger.error(f"Stdout: {e.stdout}")
        logger.error(f"Stderr: {e.stderr}")
        raise

def publish_to_github(commit_message="🤖 CasinoRadar: Refatoração completa e novo robô v8"):
    """Adiciona, commita e faz push das alterações para o GitHub."""
    logger.info("Iniciando processo de publicação no GitHub...")
    try:
        # 1. Adicionar todas as alterações
        run_command(["git", "add", "."])
        logger.info("Todas as alterações adicionadas.")

        # 2. Verificar se há algo para commitar
        status_output = run_command(["git", "status", "--porcelain"])
        if not status_output:
            logger.info("Nenhuma alteração para commitar. Publicação ignorada.")
            return False

        # 3. Commitar as alterações
        run_command(["git", "commit", "-m", commit_message])
        logger.info(f"Alterações commitadas com a mensagem: '{commit_message}'")

        # 4. Sincronizar com o remoto antes do push para reduzir conflitos entre workflows
        run_command(["git", "pull", "--rebase", "origin", "main"])

        # 5. Fazer push para o repositório remoto
        run_command(["git", "push", "origin", "main"])
        logger.info("Alterações enviadas para o GitHub com sucesso!")
        return True

    except Exception as e:
        logger.critical(f"Falha crítica no processo de publicação: {e}")
        return False

def main():
    publish_to_github()

if __name__ == "__main__":
    main()
