import re
from pathlib import Path

COMPARADOR_FILE = Path("/home/ubuntu/casino-radar.github.io/docs/comparador.html")

def optimize_comparador():
    if not COMPARADOR_FILE.exists():
        return

    content = COMPARADOR_FILE.read_text(encoding="utf-8")

    # 1. Substituir a carga estática por carga dinâmica do JSON
    dynamic_load_js = """
        let cassinosData = {};
        
        async function loadData() {
            try {
                const response = await fetch('cassinos.json');
                const data = await response.json();
                // Transformar array em objeto para busca rápida
                data.cassinos.forEach(c => {
                    cassinosData[c.id] = {
                        nome: c.nome,
                        rating: c.rating,
                        bonus: c.bonus,
                        deposito: c.deposito_min,
                        saque: c.saque,
                        jogos: c.jogos,
                        licenca: 'SPA/MF',
                        pix: 'Sim',
                        suporte: '24/7',
                        url: c.link || '#'
                    };
                });
                populateSelectors(data.cassinos);
                updateComparison();
            } catch (e) {
                console.error("Erro ao carregar dados:", e);
            }
        }

        function populateSelectors(cassinos) {
            const selectors = ['casino1', 'casino2', 'casino3'];
            selectors.forEach((id, idx) => {
                const sel = document.getElementById(id);
                sel.innerHTML = '<option value="">-- Selecione --</option>';
                cassinos.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c.id;
                    opt.textContent = c.nome;
                    if (idx === 0 && c.id === 1) opt.selected = true;
                    if (idx === 1 && c.id === 2) opt.selected = true;
                    if (idx === 2 && c.id === 3) opt.selected = true;
                    sel.appendChild(opt);
                });
            });
        }

        window.onload = loadData;
    """

    # Remover o objeto estático e a chamada inicial
    content = re.sub(r'const cassinosData = \{.*?\};', '', content, flags=re.DOTALL)
    content = content.replace('updateComparison();', dynamic_load_js)
    
    # Ajustar a função updateComparison para usar IDs numéricos se necessário
    content = content.replace('const data = casinos.map(id => cassinosData[id]);', 'const data = casinos.map(id => cassinosData[id]).filter(d => d);')

    COMPARADOR_FILE.write_text(content, encoding="utf-8")
    print("✅ comparador.html otimizado para carga dinâmica!")

if __name__ == "__main__":
    optimize_comparador()
