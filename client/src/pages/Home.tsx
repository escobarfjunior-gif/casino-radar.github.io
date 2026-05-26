import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Sparkles, Zap, Shield, TrendingUp, Heart, Dice5 } from "lucide-react";
import { useState } from "react";

const HERO_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310519663697524081/m6JmXYFonBksNXfMtEy6oo/hero-casino-modern-ftma3NBNDoHeLxHgyc3gVm.webp";
const CARDS_PATTERN = "https://d2xsxph8kpxj0f.cloudfront.net/310519663697524081/m6JmXYFonBksNXfMtEy6oo/cards-pattern-modern-Ao47Mc89TrzRxhg5WcBrk4.webp";
const GRADIENT_BG = "https://d2xsxph8kpxj0f.cloudfront.net/310519663697524081/m6JmXYFonBksNXfMtEy6oo/gradient-accent-modern-B6yuPwFf4ehJfcp4MMiB3X.webp";

interface Casino {
  id: number;
  name: string;
  rating: number;
  bonus: string;
  minDeposit: string;
  withdrawalTime: string;
  icon: string;
}

const casinos: Casino[] = [
  {
    id: 1,
    name: "SpinVegas",
    rating: 4.9,
    bonus: "100% até R$ 5.000 + 150 RG",
    minDeposit: "R$ 10",
    withdrawalTime: "Imediato via Pix",
    icon: "🎰",
  },
  {
    id: 2,
    name: "Império Bet",
    rating: 4.8,
    bonus: "Bônus até R$ 3.500",
    minDeposit: "R$ 5",
    withdrawalTime: "Até 10 min via Pix",
    icon: "👑",
  },
  {
    id: 3,
    name: "PixSorte",
    rating: 4.7,
    bonus: "R$ 50 + 100% bônus",
    minDeposit: "R$ 1",
    withdrawalTime: "Segundos via Pix",
    icon: "⚡",
  },
  {
    id: 4,
    name: "Royal Palace",
    rating: 4.6,
    bonus: "Bônus VIP até R$ 10.000",
    minDeposit: "R$ 50",
    withdrawalTime: "Até 1 hora",
    icon: "🏰",
  },
  {
    id: 5,
    name: "Brasil Slots",
    rating: 4.6,
    bonus: "200 giros em slots",
    minDeposit: "R$ 10",
    withdrawalTime: "Até 15 min via Pix",
    icon: "🍀",
  },
  {
    id: 6,
    name: "Mesa Ao Vivo Pro",
    rating: 4.5,
    bonus: "Cashback semanal",
    minDeposit: "R$ 20",
    withdrawalTime: "Até 30 min via Pix",
    icon: "🃏",
  },
];

const guides = [
  { title: "Bônus de Boas-Vindas", desc: "Tipos, requisitos e como maximizar", icon: "🎁" },
  { title: "Estratégias Roleta", desc: "Dicas para iniciantes e experientes", icon: "🎲" },
  { title: "Blackjack Online", desc: "Regras, contagem de cartas e variantes", icon: "🂡" },
  { title: "Cassinos Móveis", desc: "Apps seguros e vantagens do mobile", icon: "📱" },
  { title: "Segurança Online", desc: "Proteja seus dados e transações", icon: "🔐" },
  { title: "Jogo Responsável", desc: "Limites, autoexclusão e ajuda", icon: "🛡️" },
];

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [guideSearch, setGuideSearch] = useState("");

  const filteredCasinos = casinos.filter((c) =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredGuides = guides.filter((g) =>
    g.title.toLowerCase().includes(guideSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-background text-foreground overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-background/80 border-b border-border">
        <div className="container flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <span className="text-2xl">♠</span>
            <span className="text-xl font-bold text-gradient">CasinoRadar</span>
          </div>
          <div className="hidden md:flex gap-8">
            <a href="#rankings" className="hover-glow text-sm">Rankings</a>
            <a href="/blog" className="hover-glow text-sm">Blog</a>
            <a href="#guias" className="hover-glow text-sm">Guias</a>
            <a href="#responsavel" className="hover-glow text-sm">Jogo Responsável</a>
          </div>
          <Button className="btn-neon">Pegar Bônus</Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
        <div
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('${HERO_IMAGE}')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/50 to-transparent"></div>
        </div>

        <div className="container relative z-10 grid md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6 slide-in-up">
            <div className="inline-block">
              <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/30 w-fit">
                <Sparkles className="w-4 h-4 text-accent" />
                <span className="text-sm text-accent">100% conteúdo verificado</span>
              </div>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              Encontre seu <span className="text-gradient">cassino ideal</span> no Brasil
            </h1>

            <p className="text-lg text-muted-foreground max-w-lg">
              Rankings verificados, guias completos, bônus explicados e jogo responsável. Tudo que você precisa saber antes de apostar.
            </p>

            <div className="flex gap-4 pt-4">
              <Button className="btn-neon" size="lg">
                Ver Rankings
              </Button>
              <Button variant="outline" size="lg" className="border-accent/50 hover:border-accent">
                Saiba Mais
              </Button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8">
              <div className="space-y-1">
                <p className="text-2xl font-bold text-accent">45+</p>
                <p className="text-sm text-muted-foreground">Cassinos analisados</p>
              </div>
              <div className="space-y-1">
                <p className="text-2xl font-bold text-accent">20</p>
                <p className="text-sm text-muted-foreground">Guias +800 palavras</p>
              </div>
              <div className="space-y-1">
                <p className="text-2xl font-bold text-accent">100%</p>
                <p className="text-sm text-muted-foreground">Conteúdo original</p>
              </div>
              <div className="space-y-1">
                <p className="text-2xl font-bold text-accent">24h</p>
                <p className="text-sm text-muted-foreground">Atualização editorial</p>
              </div>
            </div>
          </div>

          <div className="hidden md:flex justify-center fade-in" style={{ animationDelay: "0.2s" }}>
            <div className="relative w-full max-w-md h-96 float">
              <img
                src={CARDS_PATTERN}
                alt="Casino cards"
                className="w-full h-full object-cover rounded-2xl pulse-glow"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Rankings Section */}
      <section id="rankings" className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 opacity-5 pointer-events-none" style={{
          backgroundImage: `url('${GRADIENT_BG}')`,
          backgroundSize: "cover",
        }}></div>

        <div className="container relative z-10">
          <div className="space-y-4 mb-12 text-center">
            <h2 className="text-4xl md:text-5xl font-bold">
              Os melhores <span className="text-gradient">cassinos online</span> verificados
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Filtrados por Pix, bônus, saque rápido e suporte 24h. Sempre confirme a autorização do operador.
            </p>
          </div>

          <div className="mb-8">
            <Input
              placeholder="Pesquisar cassino, bônus ou Pix..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-card border-border/50 focus:border-accent focus:ring-accent"
            />
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCasinos.map((casino, idx) => (
              <div
                key={casino.id}
                className="card-neon group"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="text-3xl">{casino.icon}</div>
                      <h3 className="text-xl font-bold">{casino.name}</h3>
                      <div className="flex items-center gap-1">
                        <span className="text-accent">★</span>
                        <span className="text-sm">{casino.rating}</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2 py-4 border-y border-border/50">
                    <p className="font-semibold text-accent">{casino.bonus}</p>
                    <div className="text-sm text-muted-foreground space-y-1">
                      <p>Depósito mín.: {casino.minDeposit}</p>
                      <p>Saque: {casino.withdrawalTime}</p>
                    </div>
                  </div>

                  <Button className="btn-neon w-full">Acessar Site</Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Guides Section */}
      <section id="guias" className="py-20 relative">
        <div className="container">
          <div className="space-y-4 mb-12 text-center">
            <h2 className="text-4xl md:text-5xl font-bold">
              Guias <span className="text-gradient">educativos</span> completos
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Artigos de 800+ palavras sobre bônus, segurança, estratégias e jogo responsável.
            </p>
          </div>

          <div className="mb-8">
            <Input
              placeholder="Pesquisar guia por tema..."
              value={guideSearch}
              onChange={(e) => setGuideSearch(e.target.value)}
              className="bg-card border-border/50 focus:border-accent focus:ring-accent"
            />
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredGuides.map((guide, idx) => (
              <div
                key={idx}
                className="card-neon group cursor-pointer"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="space-y-4">
                  <div className="text-4xl">{guide.icon}</div>
                  <div className="space-y-2">
                    <h3 className="text-lg font-bold group-hover:text-accent transition-colors">
                      {guide.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">{guide.desc}</p>
                  </div>
                  <div className="pt-4 border-t border-border/50">
                    <a href="#" className="text-accent text-sm font-semibold hover:text-accent/80 transition-colors">
                      Ler guia completo →
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 gradient-animate opacity-10 pointer-events-none"></div>

        <div className="container relative z-10">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="space-y-4 text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 rounded-full bg-accent/10 border border-accent/30">
                  <Shield className="w-8 h-8 text-accent" />
                </div>
              </div>
              <h3 className="text-xl font-bold">100% Seguro</h3>
              <p className="text-muted-foreground">
                Todos os cassinos são verificados e licenciados. Seus dados estão protegidos.
              </p>
            </div>

            <div className="space-y-4 text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 rounded-full bg-accent/10 border border-accent/30">
                  <Zap className="w-8 h-8 text-accent" />
                </div>
              </div>
              <h3 className="text-xl font-bold">Saques Rápidos</h3>
              <p className="text-muted-foreground">
                Pix instantâneo, transferência bancária e e-wallets. Saque em segundos.
              </p>
            </div>

            <div className="space-y-4 text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 rounded-full bg-accent/10 border border-accent/30">
                  <Heart className="w-8 h-8 text-accent" />
                </div>
              </div>
              <h3 className="text-xl font-bold">Jogo Responsável</h3>
              <p className="text-muted-foreground">
                Limites de depósito, autoexclusão e recursos de ajuda sempre disponíveis.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative overflow-hidden">
        <div
          className="absolute inset-0 z-0"
          style={{
            backgroundImage: `url('${GRADIENT_BG}')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-transparent"></div>
        </div>

        <div className="container relative z-10 text-center space-y-8">
          <h2 className="text-4xl md:text-5xl font-bold max-w-2xl mx-auto">
            Pronto para começar? <span className="text-gradient">Escolha seu cassino</span>
          </h2>

          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Acesse um dos nossos cassinos recomendados e comece a jogar com segurança e responsabilidade.
          </p>

          <Button className="btn-neon" size="lg">
            Ver Todos os Cassinos
          </Button>

          <div className="pt-8 border-t border-border/50 mt-12">
            <p className="text-sm text-muted-foreground">
              ⚠️ Jogo é para maiores de 18 anos. Jogue com responsabilidade. Consulte nossa política de jogo responsável.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-12 bg-card/50">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold mb-4">CasinoRadar</h3>
              <p className="text-sm text-muted-foreground">
                Guia confiável de cassinos online no Brasil com foco em segurança e jogo responsável.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Cassinos</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-accent transition-colors">Cassino Seguro</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Cassinos com Pix</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Bônus e Rollover</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Informações</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-accent transition-colors">Sobre</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Metodologia</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Contato</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-accent transition-colors">Privacidade</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Termos</a></li>
                <li><a href="#" className="hover:text-accent transition-colors">Jogo Responsável</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-border/50 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2026 CasinoRadar. Todos os direitos reservados. Jogue com responsabilidade.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
