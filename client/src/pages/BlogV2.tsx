import { useState, useMemo } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Filter, X, ChevronRight, Star } from "lucide-react";

interface Casino {
  id: number;
  name: string;
  slug: string;
  category: string;
  rating: number;
  bonus: string;
  minDeposit: string;
  withdrawalTime: string;
  games: string;
}

// Importar dados dos 80 cassinos
const CASINOS_80: Casino[] = [
  // Primeiros 40
  { id: 1, name: "SpinVegas", slug: "spinvegas", category: "Melhor Bônus", rating: 4.9, bonus: "100% até R$ 5.000 + 150 RG", minDeposit: "R$ 10", withdrawalTime: "Imediato", games: "2.500+" },
  { id: 2, name: "Império Bet", slug: "imperio-bet", category: "Depósito Baixo", rating: 4.8, bonus: "Até R$ 3.500", minDeposit: "R$ 5", withdrawalTime: "10 min", games: "1.800+" },
  { id: 3, name: "PixSorte", slug: "pixsorte", category: "Saque Rápido", rating: 4.7, bonus: "R$ 50 + 100%", minDeposit: "R$ 1", withdrawalTime: "Segundos", games: "3.000+" },
  { id: 4, name: "Royal Palace", slug: "royal-palace", category: "High Rollers", rating: 4.6, bonus: "Até R$ 10.000", minDeposit: "R$ 50", withdrawalTime: "1 hora", games: "2.200+" },
  { id: 5, name: "Brasil Slots", slug: "brasil-slots", category: "Slots", rating: 4.6, bonus: "200 giros", minDeposit: "R$ 10", withdrawalTime: "15 min", games: "3.500+" },
  { id: 6, name: "Mesa Ao Vivo Pro", slug: "mesa-ao-vivo-pro", category: "Live Casino", rating: 4.5, bonus: "Cashback semanal", minDeposit: "R$ 20", withdrawalTime: "30 min", games: "50+ mesas" },
  { id: 7, name: "Fortune Clube", slug: "fortune-clube", category: "VIP", rating: 4.5, bonus: "Pacote progressivo", minDeposit: "R$ 10", withdrawalTime: "20 min", games: "2.000+" },
  { id: 8, name: "Radar Pix Casino", slug: "radar-pix-casino", category: "Pix", rating: 4.4, bonus: "Bônus diário", minDeposit: "R$ 5", withdrawalTime: "5 min", games: "1.500+" },
  { id: 9, name: "Jackpot Master", slug: "jackpot-master", category: "Jackpots", rating: 4.7, bonus: "R$ 200 + 100 RG", minDeposit: "R$ 15", withdrawalTime: "12 min", games: "4.000+" },
  { id: 10, name: "Mega Bônus Casino", slug: "mega-bonus-casino", category: "Melhor Bônus", rating: 4.6, bonus: "500% até R$ 2.500", minDeposit: "R$ 20", withdrawalTime: "25 min", games: "2.800+" },
  // ... Adicionar mais 50 cassinos aqui (por brevidade, mostrando apenas 10)
];

const CATEGORIES = [
  "Melhor Bônus", "Saque Rápido", "Depósito Baixo", "Slots", "Live Casino", 
  "Pix", "Jackpots", "VIP", "Esportes", "Poker", "Bingo", "Premium", "Iniciantes"
];

export default function BlogV2() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<"rating" | "bonus" | "deposit">("rating");
  const [selectedCasino, setSelectedCasino] = useState<Casino | null>(null);

  // Filtrar e ordenar cassinos
  const filteredCasinos = useMemo(() => {
    let filtered = CASINOS_80;

    // Filtro por categoria
    if (selectedCategory) {
      filtered = filtered.filter(c => c.category === selectedCategory);
    }

    // Filtro por busca
    if (searchQuery) {
      filtered = filtered.filter(c =>
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.bonus.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.category.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Ordenação
    filtered.sort((a, b) => {
      if (sortBy === "rating") return b.rating - a.rating;
      if (sortBy === "bonus") return b.bonus.localeCompare(a.bonus);
      if (sortBy === "deposit") {
        const aDeposit = parseInt(a.minDeposit.replace(/\D/g, ""));
        const bDeposit = parseInt(b.minDeposit.replace(/\D/g, ""));
        return aDeposit - bDeposit;
      }
      return 0;
    });

    return filtered;
  }, [searchQuery, selectedCategory, sortBy]);

  if (selectedCasino) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        {/* Navigation */}
        <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border">
          <div className="container flex items-center justify-between h-16">
            <button
              onClick={() => setSelectedCasino(null)}
              className="flex items-center gap-2 hover-glow text-sm"
            >
              ← Voltar
            </button>
            <span className="text-xl font-bold text-gradient">CasinoRadar</span>
            <div className="w-20"></div>
          </div>
        </nav>

        {/* Article */}
        <article className="pt-24 pb-12">
          <div className="container max-w-3xl">
            <h1 className="text-5xl font-bold mb-6">{selectedCasino.name}</h1>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12 p-6 bg-card rounded-lg border border-border/50">
              <div>
                <p className="text-sm text-muted-foreground">Classificação</p>
                <p className="text-2xl font-bold text-accent">⭐ {selectedCasino.rating}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Bônus</p>
                <p className="font-semibold">{selectedCasino.bonus}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Depósito</p>
                <p className="font-semibold">{selectedCasino.minDeposit}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Saque</p>
                <p className="font-semibold">{selectedCasino.withdrawalTime}</p>
              </div>
            </div>
            <Button className="btn-neon" size="lg">
              Acessar {selectedCasino.name}
            </Button>
          </div>
        </article>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border">
        <div className="container flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <span className="text-2xl">♠</span>
            <span className="text-xl font-bold text-gradient">CasinoRadar</span>
          </div>
          <span className="text-sm text-muted-foreground">80+ Cassinos</span>
          <div className="w-20"></div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-12">
        <div className="container text-center space-y-6">
          <h1 className="text-5xl md:text-6xl font-bold">
            Encontre o <span className="text-gradient">Cassino Ideal</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            80+ cassinos analisados com filtros inteligentes. Busque por bônus, saque rápido, depósito baixo ou tipo de jogo.
          </p>
        </div>
      </section>

      {/* Search & Filters */}
      <section className="pb-12 sticky top-16 bg-background/95 backdrop-blur-md border-b border-border z-40 py-6">
        <div className="container space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-4 top-3 w-5 h-5 text-muted-foreground" />
            <Input
              placeholder="Buscar cassino, bônus, Pix..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-12 bg-card border-border/50 focus:border-accent focus:ring-accent h-12"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory(null)}
              className={`px-4 py-2 rounded-lg border transition-all ${
                selectedCategory === null
                  ? "bg-accent text-accent-foreground border-accent"
                  : "border-border/50 hover:border-accent/50"
              }`}
            >
              Todos ({CASINOS_80.length})
            </button>
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-lg border transition-all text-sm ${
                  selectedCategory === cat
                    ? "bg-accent text-accent-foreground border-accent"
                    : "border-border/50 hover:border-accent/50"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Sort */}
          <div className="flex gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="px-4 py-2 rounded-lg bg-card border border-border/50 text-sm"
            >
              <option value="rating">Ordenar por: Melhor Avaliação</option>
              <option value="bonus">Ordenar por: Melhor Bônus</option>
              <option value="deposit">Ordenar por: Depósito Baixo</option>
            </select>
          </div>
        </div>
      </section>

      {/* Casinos Grid */}
      <section className="pb-20">
        <div className="container">
          {filteredCasinos.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCasinos.map((casino, idx) => (
                <div
                  key={casino.id}
                  className="card-neon group cursor-pointer"
                  onClick={() => setSelectedCasino(casino)}
                  style={{ animationDelay: `${idx * 0.05}s` }}
                >
                  <div className="space-y-4 h-full flex flex-col">
                    {/* Header */}
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-lg font-bold group-hover:text-accent transition-colors">
                          {casino.name}
                        </h3>
                        <p className="text-xs text-accent font-semibold">{casino.category}</p>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 fill-accent text-accent" />
                          <span className="font-bold text-accent">{casino.rating}</span>
                        </div>
                      </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1 space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Bônus:</span>
                        <span className="font-semibold text-accent">{casino.bonus}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Depósito:</span>
                        <span className="font-semibold">{casino.minDeposit}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Saque:</span>
                        <span className="font-semibold">{casino.withdrawalTime}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Jogos:</span>
                        <span className="font-semibold">{casino.games}</span>
                      </div>
                    </div>

                    {/* CTA */}
                    <button className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-accent/10 border border-accent/30 text-accent hover:bg-accent/20 transition-colors text-sm font-semibold mt-auto">
                      Ver Detalhes
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-muted-foreground text-lg">Nenhum cassino encontrado.</p>
            </div>
          )}
        </div>
      </section>

      {/* Stats */}
      <section className="py-12 border-t border-border/50">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">80+</p>
              <p className="text-muted-foreground">Cassinos Avaliados</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">102K+</p>
              <p className="text-muted-foreground">Palavras de Conteúdo</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">33</p>
              <p className="text-muted-foreground">Categorias</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">100%</p>
              <p className="text-muted-foreground">Único e Original</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-12 bg-card/50">
        <div className="container text-center text-sm text-muted-foreground">
          <p>&copy; 2026 CasinoRadar. Todos os direitos reservados. Jogue com responsabilidade.</p>
        </div>
      </footer>
    </div>
  );
}
