# CasinoRadar - Robô Supremo v2

Este repositório foi atualizado para operar com a configuração **Robô Supremo v2**, inspirada na arquitetura de alta performance descrita no documento de replicação. O foco da versão é aumentar a resiliência do pipeline, melhorar a qualidade dos dados publicados e disponibilizar uma camada de JSONs estáticos que funcionam como uma pequena API para o front-end.

## Arquitetura aplicada

O ciclo principal continua executado pelo workflow `.github/workflows/robot_v8.yml`, que roda automaticamente a cada duas horas e também pode ser disparado manualmente pelo GitHub Actions. Como a autenticação disponível para publicação pode não ter permissão `workflow`, os ganhos da versão v2 foram concentrados nos scripts já chamados pelo workflow existente; assim, a automação passa a usar deduplicação reforçada, sitemap único, publicação resiliente e geração de JSONs de inteligência acoplada à etapa de sitemap.

| Etapa | Script | Função |
|---|---|---|
| Preparação Git | `scripts/publish.py` | Configura identidade do bot, `pull.rebase=true` e fallback com merge resiliente antes do push. |
| Coleta | `scripts/fetch_data.py` | Coleta, normaliza e preserva dados existentes quando não há dados novos. |
| Deduplicação | `scripts/deduplicate.py` | Remove duplicatas por slug, URL limpa, similaridade de nome e preço quando aplicável. |
| Inteligência | `scripts/generate_intelligence.py` via `scripts/build_sitemap.py` | Gera `radar-index.json`, `market-intelligence.json` e `editorial-automation.json` mesmo sem alterar o YAML do workflow. |
| Geração HTML | `scripts/generate_pages.py` | Cria páginas estáticas de cassinos com conteúdo SEO e fallback seguro. |
| Comparativos | `scripts/generate_comparisons.py` | Cria páginas comparativas entre cassinos. |
| Sitemap | `scripts/build_sitemap.py` | Gera `sitemap.xml` com conjunto único de URLs. |
| Publicação | `scripts/publish.py` | Commit, pull resiliente e push para `main`. |

## Sistema de auto-cura

O arquivo `scripts/self_healing.py` executa cada etapa crítica do pipeline. Se uma etapa falhar, ele captura `stdout`, `stderr` e `exit_code`, consulta o modelo configurado quando `OPENAI_API_KEY` está disponível, grava um diagnóstico em `logs/self_healing_diagnoses.jsonl` e tenta uma nova execução.

> O objetivo da auto-cura não é alterar código automaticamente sem revisão, mas aumentar a chance de recuperação contra falhas transitórias de rede, API, dependências e tempo de resposta.

## Deduplicação agressiva e blindagem de dados

A deduplicação agora aplica validações defensivas antes de salvar a base final. Registros sem nome são ignorados, preços inválidos são rejeitados quando o campo de preço existe, URLs passam por limpeza de parâmetros de rastreamento e registros semelhantes são comparados por slug, URL, nome e variação de preço inferior a 1%.

Quando duas entradas representam o mesmo item, o robô mantém o registro com melhor `custom_discount_pct`, `discount_pct`, `desconto`, `avaliacao` ou `rating`. Em empate, mantém o registro mais completo.

## JSONs de inteligência publicados

Os arquivos abaixo são gerados tanto em `/data` quanto em `/docs`, sendo que os arquivos em `/docs` ficam acessíveis publicamente pelo GitHub Pages.

| Arquivo | Uso |
|---|---|
| `docs/radar-index.json` | Índice otimizado para busca, filtros e comparadores. |
| `docs/market-intelligence.json` | Resumo de mercado, categorias, métodos de pagamento e destaques. |
| `docs/editorial-automation.json` | Sugestões de pautas, comparativos e posts sociais. |
| `docs/cassinos.json` | Envelope compatível com consumidores front-end que esperam `casinos`. |

## Publicação resiliente

Antes do push, o publicador executa um pull com rebase. Se houver conflito ou falha de sincronização, tenta uma estratégia alternativa com `--no-rebase --strategy-option=ours --no-edit`, preservando arquivos gerados pelo robô.

## Manutenção

Para validar localmente os componentes centrais, use:

```bash
python3.11 -m py_compile scripts/self_healing.py scripts/deduplicate.py scripts/generate_intelligence.py scripts/build_sitemap.py scripts/publish.py
python3.11 scripts/deduplicate.py
python3.11 scripts/generate_intelligence.py
python3.11 scripts/build_sitemap.py
```

Os logs ficam em `/logs` e são ignorados pelo Git, exceto pelo arquivo `.gitkeep` que mantém a pasta versionada.
