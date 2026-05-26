import json
import random

# Nomes de cassinos
nomes_base = [
    "Spin", "Bet", "Casino", "Luck", "Fortune", "Royal", "Golden", "Silver", "Platinum", "Diamond",
    "Ace", "King", "Queen", "Jack", "Poker", "Roulette", "Slot", "Jackpot", "Bonus", "Mega",
    "Ultra", "Super", "Turbo", "Flash", "Thunder", "Storm", "Fire", "Ice", "Wind", "Wave",
    "Star", "Moon", "Sun", "Planet", "Galaxy", "Cosmic", "Quantum", "Nexus", "Infinity", "Apex",
    "Elite", "Premium", "Luxury", "Deluxe", "Grand", "Majestic", "Imperial", "Regal", "Noble", "Sovereign",
    "Brasil", "Rio", "Amazon", "Samba", "Carnival", "Tropical", "Paradise", "Eden", "Oasis", "Mirage"
]

sufixos = [
    "Bet", "Casino", "Play", "Games", "Slots", "Pro", "Max", "Plus", "Club", "VIP",
    "777", "888", "999", "Pix", "Rápido", "Express", "Turbo", "Flash", "Mega", "Ultra"
]

# Bônus variados
bonus_templates = [
    "100% até R$ {valor}",
    "200% até R$ {valor}",
    "500% até R$ {valor}",
    "R$ {valor} + {giros} giros",
    "{giros} giros grátis",
    "Cashback {pct}%",
    "Bônus sem rollover",
    "Pacote progressivo até R$ {valor}",
    "R$ {valor} bônus diário",
    "Até R$ {valor} em prêmios"
]

# Categorias
categorias_list = [
    "Melhor Bônus", "Saque Rápido", "Pix", "Depósito Baixo", "Slots",
    "Live Casino", "VIP", "Premium", "Cashback", "Jackpots",
    "High Rollers", "Confiável", "Esportes", "Novidades", "Jogos de Mesa",
    "Bingo", "Dados", "Poker"
]

def gerar_cassinos(quantidade=400):
    cassinos = []
    
    for i in range(1, quantidade + 1):
        nome = random.choice(nomes_base) + random.choice(sufixos)
        
        # Gerar bônus único
        bonus_template = random.choice(bonus_templates)
        if "{valor}" in bonus_template:
            valor = random.choice([500, 1000, 2000, 3000, 5000, 10000])
            bonus = bonus_template.format(valor=valor)
        elif "{giros}" in bonus_template:
            giros = random.choice([50, 100, 150, 200, 300])
            bonus = bonus_template.format(giros=giros)
        elif "{pct}" in bonus_template:
            pct = random.choice([5, 10, 15, 20])
            bonus = bonus_template.format(pct=pct)
        else:
            bonus = bonus_template
        
        deposito_min = random.choice(["R$ 1", "R$ 5", "R$ 10", "R$ 15", "R$ 20", "R$ 25", "R$ 50"])
        saque = random.choice(["Imediato", "5 min", "10 min", "15 min", "30 min", "1 hora", "24 horas"])
        jogos = f"{random.randint(1000, 5000)}+"
        rating = round(random.uniform(4.0, 5.0), 1)
        
        # Selecionar 2-4 categorias aleatórias
        num_categorias = random.randint(2, 4)
        categorias = random.sample(categorias_list, num_categorias)
        
        cassino = {
            "id": i,
            "nome": nome,
            "bonus": bonus,
            "deposito_min": deposito_min,
            "saque": saque,
            "jogos": jogos,
            "categorias": categorias,
            "rating": rating
        }
        
        cassinos.append(cassino)
    
    return cassinos

# Gerar 400 cassinos
cassinos = gerar_cassinos(400)

# Salvar em JSON
data = {
    "cassinos": cassinos,
    "total": len(cassinos),
    "categorias": {cat: f"Cassinos com {cat.lower()}" for cat in categorias_list},
    "aeet": {
        "nome": "AEET - Associação Europeia de Entretenimento em Tempo Real",
        "descricao": "Organização que representa operadores de jogos de azar online na Europa",
        "site": "https://www.aeet.eu",
        "regulamentacao": "Promove práticas responsáveis e conformidade com regulamentações"
    }
}

with open('/home/ubuntu/casino-radar.github.io/docs/cassinos.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(cassinos)} cassinos gerados com sucesso!")
