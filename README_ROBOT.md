# 🤖 CasinoRadar - Robô Automático v8

Este projeto foi totalmente refatorado para garantir estabilidade absoluta, eliminando o uso de automação de navegador (Selenium/Playwright) e focando em uma arquitetura de dados estruturados.

## 🚀 Arquitetura

O sistema funciona em um ciclo de 8 etapas, executado automaticamente a cada 2 horas via GitHub Actions:

1.  **Coleta (`fetch_data.py`):** Busca informações reais online (APIs/RSS) e normaliza os dados.
2.  **Deduplicação (`deduplicate.py`):** Garante que nenhum conteúdo seja repetido usando hashes SHA256.
3.  **JSON Estruturado:** Salva os dados limpos em `/data/casinos.json`.
4.  **Geração de Páginas (`generate_pages.py`):** Transforma os dados JSON em páginas HTML estáticas usando templates profissionais em `/templates/`.
5.  **SEO Completo:** Cada página gerada inclui JSON-LD, Open Graph, Twitter Cards e Meta Tags otimizadas.
6.  **Sitemap (`build_sitemap.py`):** Atualiza automaticamente o `sitemap.xml` com as novas URLs.
7.  **Logs:** Registra cada etapa em `/logs/` para fácil monitoramento.
8.  **Publicação (`publish.py`):** Faz o commit e push automático para o GitHub Pages.

## 📁 Estrutura de Pastas

- `/scripts/`: Motores em Python do robô.
- `/templates/`: Templates HTML para cassinos, reviews e guias.
- `/data/`: Banco de dados em JSON.
- `/docs/`: Site final publicado no GitHub Pages.
- `/logs/`: Histórico de execução do robô.
- `.github/workflows/`: Configuração do agendamento (Cron).

## 🛠️ Como Personalizar

- **Novos Cassinos:** Adicione manualmente no `data/casinos.json` ou configure novas fontes no `scripts/fetch_data.py`.
- **Design:** Edite os arquivos em `/templates/` para mudar o visual de todas as páginas geradas.
- **Frequência:** Altere o arquivo `.github/workflows/robot_v8.yml` para mudar o intervalo de execução.

---
Projeto construído por **Manus AI** para **CasinoRadar**.
