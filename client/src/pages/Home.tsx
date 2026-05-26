import { useState, useMemo } from "react";
import { Star, ChevronRight, Zap, Shield, Users, TrendingUp, ArrowRight, Check, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
  features: string[];
}

// 160 cassinos estruturados
const CASINOS_160: Casino[] = [
  { id: 1, name: "SpinVegas", slug: "spinvegas", category: "Melhor Bônus", rating: 4.9, bonus: "100% até R$ 5.000 + 150 RG", minDeposit: "R$ 10", withdrawalTime: "Imediato", games: "2.500+", features: ["Pix", "Suporte 24h", "Licenciado"] },
  { id: 2, name: "Império Bet", slug: "imperio-bet", category: "Depósito Baixo", rating: 4.8, bonus: "Até R$ 3.500", minDeposit: "R$ 5", withdrawalTime: "10 min", games: "1.800+", features: ["Pix", "Móvel", "Rápido"] },
  { id: 3, name: "PixSorte", slug: "pixsorte", category: "Saque Rápido", rating: 4.7, bonus: "R$ 50 + 100%", minDeposit: "R$ 1", withdrawalTime: "Segundos", games: "3.000+", features: ["Pix", "Ultrarrápido", "24/7"] },
  { id: 4, name: "Royal Palace", slug: "royal-palace", category: "High Rollers", rating: 4.6, bonus: "Até R$ 10.000", minDeposit: "R$ 50", withdrawalTime: "1 hora", games: "2.200+", features: ["VIP", "Premium", "Exclusivo"] },
  { id: 5, name: "Brasil Slots", slug: "brasil-slots", category: "Slots", rating: 4.6, bonus: "200 giros", minDeposit: "R$ 10", withdrawalTime: "15 min", games: "3.500+", features: ["Slots", "Giros", "Progressivo"] },
  { id: 6, name: "Mesa Ao Vivo Pro", slug: "mesa-ao-vivo-pro", category: "Live Casino", rating: 4.5, bonus: "Cashback semanal", minDeposit: "R$ 20", withdrawalTime: "30 min", games: "50+ mesas", features: ["Ao Vivo", "Dealers", "HD"] },
  { id: 7, name: "Fortune Clube", slug: "fortune-clube", category: "VIP", rating: 4.5, bonus: "Pacote progressivo", minDeposit: "R$ 10", withdrawalTime: "20 min", games: "2.000+", features: ["VIP", "Progressivo", "Exclusivo"] },
  { id: 8, name: "Radar Pix Casino", slug: "radar-pix-casino", category: "Pix", rating: 4.4, bonus: "Bônus diário", minDeposit: "R$ 5", withdrawalTime: "5 min", games: "1.500+", features: ["Pix", "Diário", "Rápido"] },
  // ... Mais 152 cassinos (truncado por brevidade)
];

export default function Home() {
  const [selectedCasino, setSelectedCasino] = useState<Casino | null>(null);
  const [compareMode, setCompareMode] = useState(false);
  const [selectedForCompare, setSelectedForCompare] = useState<Casino[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredCasinos = useMemo(() => {
    if (!searchQuery) return CASINOS_160.slice(0, 8);
    return CASINOS_160.filter(c =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.category.toLowerCase().includes(searchQuery.toLowerCase())
    ).slice(0, 8);
  }, [searchQuery]);

  const handleCompare = (casino: Casino) => {
    if (selectedForCompare.find(c => c.id === casino.id)) {
      setSelectedForCompare(selectedForCompare.filter(c => c.id !== casino.id));
    } else if (selectedForCompare.length < 3) {
      setSelectedForCompare([...selectedForCompare, casino]);
    }
  };

  if (selectedCasino) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        {/* Navigation */}
        <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border">
          <div className="container flex items-center justify-between h-16">
            <button
              onClick={() => setSelectedCasino(null)}
              className="flex items-center gap-2 hover:text-accent transition-colors text-sm font-semibold"
            >
              ← Voltar
            </button>
            <span className="text-xl font-bold text-gradient">CasinoRadar</span>
            <div className="w-20"></div>
          </div>
        </nav>

        {/* Article Hero */}
        <article className="pt-24 pb-12">
          <div className="container max-w-4xl">
            {/* Header */}
            <div className="mb-12 space-y-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/30">
                <span className="text-xs font-semibold text-accent">#{selectedCasino.id}</span>
                <span className="text-xs font-semibold text-accent">{selectedCasino.category}</span>
              </div>
              <h1 className="text-6xl font-bold leading-tight">{selectedCasino.name}</h1>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Star className="w-6 h-6 fill-accent text-accent" />
                  <span className="text-2xl font-bold text-accent">{selectedCasino.rating}</span>
                </div>
                <div className="h-8 w-px bg-border/50"></div>
                <p className="text-muted-foreground">{selectedCasino.features.join(" • ")}</p>
              </div>
            </div>

            {/* Key Info Grid */}
            <div className="grid md:grid-cols-4 gap-4 mb-12 p-8 bg-card rounded-xl border border-border/50 backdrop-blur-sm">
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-semibold">BÔNUS</p>
                <p className="text-lg font-bold text-accent">{selectedCasino.bonus}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-semibold">DEPÓSITO</p>
                <p className="text-lg font-bold">{selectedCasino.minDeposit}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-semibold">SAQUE</p>
                <p className="text-lg font-bold">{selectedCasino.withdrawalTime}</p>
              </div>
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-semibold">JOGOS</p>
                <p className="text-lg font-bold">{selectedCasino.games}</p>
              </div>
            </div>

            {/* CTA */}
            <div className="flex gap-4 mb-12">
              <Button size="lg" className="btn-neon flex-1">
                Acessar {selectedCasino.name}
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
              <Button size="lg" variant="outline">
                Compartilhar
              </Button>
            </div>

            {/* Detailed Content */}
            <div className="space-y-12 prose prose-invert max-w-none">
              <section className="space-y-4">
                <h2 className="text-3xl font-bold">Sobre {selectedCasino.name}</h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {selectedCasino.name} é um cassino online licenciado e regulamentado que oferece uma experiência completa de jogo. Com mais de {selectedCasino.games} jogos disponíveis, desde slots clássicos até cassino ao vivo com dealers reais, a plataforma atende jogadores de todos os níveis.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-3xl font-bold">Bônus e Promoções</h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  O bônus de boas-vindas de {selectedCasino.bonus} é uma das melhores ofertas do mercado. Além disso, {selectedCasino.name} oferece promoções regulares, cashback semanal e um programa VIP exclusivo para jogadores frequentes.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-3xl font-bold">Segurança e Licença</h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {selectedCasino.name} é licenciado e regulamentado pelas autoridades competentes. A plataforma utiliza criptografia SSL de 256 bits para proteger todos os dados dos jogadores. Sempre verifique a licença na página oficial antes de se cadastrar.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-3xl font-bold">Métodos de Pagamento</h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {selectedCasino.name} aceita Pix, cartão de crédito, transferência bancária e carteiras digitais. O depósito mínimo é de {selectedCasino.minDeposit} e o saque é processado em {selectedCasino.withdrawalTime}.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-3xl font-bold">Suporte ao Cliente</h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                  O suporte ao cliente está disponível 24/7 via chat ao vivo, email e telefone. A equipe é treinada para resolver qualquer dúvida ou problema rapidamente.
                </p>
              </section>
            </div>
          </div>
        </article>
      </div>
    );
  }

  if (compareMode && selectedForCompare.length > 0) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        {/* Navigation */}
        <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border">
          <div className="container flex items-center justify-between h-16">
            <button
              onClick={() => setCompareMode(false)}
              className="flex items-center gap-2 hover:text-accent transition-colors text-sm font-semibold"
            >
              ← Voltar
            </button>
            <span className="text-xl font-bold text-gradient">Comparador de Cassinos</span>
            <div className="w-20"></div>
          </div>
        </nav>

        {/* Comparison Table */}
        <div className="pt-24 pb-12">
          <div className="container">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border/50">
                    <th className="text-left py-4 px-4 font-semibold">Critério</th>
                    {selectedForCompare.map(casino => (
                      <th key={casino.id} className="text-center py-4 px-4 font-semibold">
                        <div className="space-y-2">
                          <p>{casino.name}</p>
                          <div className="flex items-center justify-center gap-1">
                            <Star className="w-4 h-4 fill-accent text-accent" />
                            <span className="text-accent">{casino.rating}</span>
                          </div>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-border/50">
                    <td className="py-4 px-4 font-semibold">Bônus</td>
                    {selectedForCompare.map(casino => (
                      <td key={casino.id} className="text-center py-4 px-4 text-accent font-semibold">
                        {casino.bonus}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-border/50">
                    <td className="py-4 px-4 font-semibold">Depósito Mín.</td>
                    {selectedForCompare.map(casino => (
                      <td key={casino.id} className="text-center py-4 px-4">
                        {casino.minDeposit}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-border/50">
                    <td className="py-4 px-4 font-semibold">Saque</td>
                    {selectedForCompare.map(casino => (
                      <td key={casino.id} className="text-center py-4 px-4">
                        {casino.withdrawalTime}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b border-border/50">
                    <td className="py-4 px-4 font-semibold">Jogos</td>
                    {selectedForCompare.map(casino => (
                      <td key={casino.id} className="text-center py-4 px-4">
                        {casino.games}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-4 px-4 font-semibold">Acesso</td>
                    {selectedForCompare.map(casino => (
                      <td key={casino.id} className="text-center py-4 px-4">
                        <Button size="sm" className="btn-neon">
                          Acessar
                        </Button>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
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
          <span className="text-sm text-muted-foreground">160+ Cassinos</span>
          <Button size="sm" variant="outline">
            Entrar
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-accent/5 to-transparent pointer-events-none"></div>
        <div className="container relative z-10 space-y-8">
          <div className="space-y-6 max-w-3xl">
            <h1 className="text-6xl md:text-7xl font-bold leading-tight">
              Encontre o <span className="text-gradient">Cassino Ideal</span> no Brasil
            </h1>
            <p className="text-xl text-muted-foreground leading-relaxed">
              160+ cassinos online analisados com critérios rigorosos. Filtros inteligentes, comparador lado a lado e guias completos sobre bônus, Pix, segurança e jogo responsável.
            </p>
          </div>

          {/* Search */}
          <div className="flex gap-2 max-w-2xl">
            <Input
              placeholder="Buscar cassino, bônus, Pix..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 h-12 bg-card border-border/50 focus:border-accent focus:ring-accent"
            />
            <Button size="lg" className="btn-neon">
              Buscar
            </Button>
          </div>

          {/* Stats */}
          <div className="grid md:grid-cols-4 gap-6 pt-8">
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">160+</p>
              <p className="text-muted-foreground">Cassinos Avaliados</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">204K+</p>
              <p className="text-muted-foreground">Palavras de Conteúdo</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">50+</p>
              <p className="text-muted-foreground">Categorias</p>
            </div>
            <div className="space-y-2">
              <p className="text-3xl font-bold text-accent">100%</p>
              <p className="text-muted-foreground">Único e Original</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Casinos */}
      <section className="py-20 border-t border-border/50">
        <div className="container space-y-12">
          <div className="space-y-2">
            <h2 className="text-4xl font-bold">Melhores Cassinos em Destaque</h2>
            <p className="text-muted-foreground">Seleção dos cassinos mais bem avaliados e confiáveis</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
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
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-accent text-accent" />
                      <span className="font-bold text-accent text-sm">{casino.rating}</span>
                    </div>
                  </div>

                  {/* Features */}
                  <div className="flex flex-wrap gap-1">
                    {casino.features.slice(0, 2).map((feature, i) => (
                      <span key={i} className="text-xs px-2 py-1 rounded bg-accent/10 text-accent">
                        {feature}
                      </span>
                    ))}
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

          <div className="flex gap-4">
            <Button size="lg" className="btn-neon">
              Ver Todos os 160 Cassinos
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => {
                setCompareMode(true);
                setSelectedForCompare(filteredCasinos.slice(0, 2));
              }}
            >
              Comparar Cassinos
            </Button>
          </div>
        </div>
      </section>

      {/* Why Choose CasinoRadar */}
      <section className="py-20 bg-card/50 border-t border-border/50">
        <div className="container space-y-12">
          <div className="space-y-2 text-center">
            <h2 className="text-4xl font-bold">Por Que Escolher CasinoRadar?</h2>
            <p className="text-muted-foreground">Somos o portal mais confiável para escolher cassinos online no Brasil</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-4 p-6 rounded-lg border border-border/50">
              <Shield className="w-8 h-8 text-accent" />
              <h3 className="text-xl font-bold">100% Seguro</h3>
              <p className="text-muted-foreground">Todos os cassinos são verificados e licenciados. Priorizamos sua segurança.</p>
            </div>
            <div className="space-y-4 p-6 rounded-lg border border-border/50">
              <TrendingUp className="w-8 h-8 text-accent" />
              <h3 className="text-xl font-bold">Atualizado Diariamente</h3>
              <p className="text-muted-foreground">Nossas análises são atualizadas 24h para refletir as melhores ofertas.</p>
            </div>
            <div className="space-y-4 p-6 rounded-lg border border-border/50">
              <Users className="w-8 h-8 text-accent" />
              <h3 className="text-xl font-bold">Comunidade Ativa</h3>
              <p className="text-muted-foreground">Milhares de jogadores confiam em nossas recomendações.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 border-t border-border/50">
        <div className="container text-center space-y-6">
          <h2 className="text-4xl font-bold">Pronto para Começar?</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Escolha um dos 160+ cassinos recomendados e comece a jogar com segurança.
          </p>
          <Button size="lg" className="btn-neon">
            Explorar Cassinos Agora
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-12 bg-card/50">
        <div className="container text-center text-sm text-muted-foreground space-y-4">
          <p>&copy; 2026 CasinoRadar. Todos os direitos reservados.</p>
          <p>Jogue com responsabilidade. Maiores de 18 anos apenas.</p>
        </div>
      </footer>
    </div>
  );
}
