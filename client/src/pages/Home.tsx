import React, { useState } from "react";
import { 
  Shield, 
  Search, 
  CheckCircle, 
  HelpCircle, 
  ArrowUpRight, 
  BookOpen, 
  Coins, 
  Smartphone, 
  FileText, 
  ExternalLink, 
  Info, 
  AlertTriangle,
  UserCheck,
  Scale,
  Award,
  ChevronDown,
  Clock
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

// Dados fictícios/estruturados para simular a metodologia de avaliação e comparativos transparentes
interface CasinoModel {
  id: string;
  name: string;
  rating: number;
  bonus: string;
  minDeposit: string;
  payoutTime: string;
  license: string;
  pros: string[];
  status: "autorizado" | "analise" | "nao-recomendado";
}

const CASINOS_DATA: CasinoModel[] = [
  {
    id: "1",
    name: "SpinVegas",
    rating: 4.9,
    bonus: "100% até R$ 5.000 + 150 Rodadas Grátis",
    minDeposit: "R$ 10,00",
    payoutTime: "Imediato (Pix)",
    license: "SPA/MF nº 0042/2026",
    pros: ["Suporte 24h em português", "Excelente catálogo de slots", "Saques instantâneos"],
    status: "autorizado"
  },
  {
    id: "2",
    name: "Império Bet",
    rating: 4.8,
    bonus: "Boas-vindas até R$ 3.500",
    minDeposit: "R$ 5,00",
    payoutTime: "Até 10 min (Pix)",
    license: "SPA/MF nº 0019/2026",
    pros: ["Depósito mínimo muito baixo", "App Android nativo", "Rollover justo"],
    status: "autorizado"
  },
  {
    id: "3",
    name: "PixSorte",
    rating: 4.7,
    bonus: "R$ 50,00 no cadastro + 100% de bônus",
    minDeposit: "R$ 1,00",
    payoutTime: "Segundos (Pix)",
    license: "SPA/MF nº 0088/2026",
    pros: ["Saque automatizado", "Cadastro simplificado", "Promoções diárias"],
    status: "autorizado"
  },
  {
    id: "4",
    name: "Royal Palace Casino",
    rating: 4.6,
    bonus: "Bônus VIP até R$ 10.000",
    minDeposit: "R$ 50,00",
    payoutTime: "Até 1 hora",
    license: "SPA/MF nº 0102/2026",
    pros: ["Clube VIP exclusivo", "Mesas de Blackjack exclusivas", "Altos limites de saque"],
    status: "autorizado"
  },
  {
    id: "5",
    name: "Brasil Slots",
    rating: 4.6,
    bonus: "200 Giros Grátis em jogos selecionados",
    minDeposit: "R$ 10,00",
    payoutTime: "Até 15 min (Pix)",
    license: "SPA/MF nº 0077/2026",
    pros: ["Milhares de caça-níqueis", "Provedores certificados", "Torneios semanais"],
    status: "autorizado"
  }
];

const GUIDES_DATA = [
  {
    id: "bonus",
    category: "Bônus",
    title: "Guia Completo de Bônus de Boas-Vindas",
    desc: "Aprenda a analisar os requisitos de aposta (rollover), prazos de validade e contribuição de jogos antes de aceitar uma promoção.",
    words: 1062,
    icon: Coins
  },
  {
    id: "seguranca",
    category: "Segurança",
    title: "Como Identificar um Cassino Seguro",
    desc: "Um checklist detalhado para avaliar licenças oficiais, criptografia de dados, políticas de KYC e a reputação do operador no mercado brasileiro.",
    words: 1073,
    icon: Shield
  },
  {
    id: "pix",
    category: "Pagamentos",
    title: "Cassinos com Pix: Taxas e Limites",
    desc: "Entenda as regras de transação via Pix, como evitar taxas ocultas e por que a velocidade do saque não deve anular a verificação de segurança.",
    words: 1070,
    icon: UserCheck
  },
  {
    id: "responsavel",
    category: "Jogo Responsável",
    title: "Diretrizes de Jogo Responsável",
    desc: "Como configurar limites de depósito, tempo de sessão e utilizar ferramentas de autoexclusão para manter as apostas apenas como entretenimento.",
    words: 1069,
    icon: Scale
  }
];

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterStatus, setFilterStatus] = useState<string>("todos");
  const [expandedCasino, setExpandedCasino] = useState<string | null>(null);

  const filteredCasinos = CASINOS_DATA.filter(casino => {
    const matchesSearch = casino.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          casino.bonus.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  const handleAction = (casinoName: string) => {
    toast.info(`Você está sendo redirecionado para a verificação oficial de ${casinoName}.`, {
      description: "Sempre confirme a autorização do operador no site do Ministério da Fazenda antes de se cadastrar.",
      duration: 5000,
    });
  };

  const handlePlaceholderClick = (title: string) => {
    toast.success(`Guia "${title}" carregado com sucesso!`, {
      description: "Conteúdo educativo otimizado para leitura responsável.",
    });
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans selection:bg-primary/20 selection:text-primary">
      {/* Top Banner - Aviso Legal Obrigatório */}
      <div className="bg-amber-950/40 border-b border-amber-900/40 py-2 px-4 text-center text-xs text-amber-200/90 flex items-center justify-center gap-2">
        <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0" />
        <span>
          <strong>Aviso de Responsabilidade:</strong> Apostas online envolvem risco financeiro. Este site é estritamente informativo para maiores de 18 anos. Verifique a regularidade do operador na Secretaria de Prêmios e Apostas (SPA/MF) antes de jogar.
        </span>
      </div>

      {/* Header */}
      <header className="border-b border-border/60 bg-background/80 backdrop-blur-md sticky top-0 z-50 transition-all">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-primary to-amber-600 flex items-center justify-center shadow-md shadow-primary/10">
              <span className="font-serif text-lg font-bold text-background">♠</span>
            </div>
            <div className="flex flex-col">
              <span className="font-serif text-lg font-bold tracking-tight text-white">CasinoRadar</span>
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest font-semibold">Guia de Escolha Segura</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
            <a href="#rankings" className="hover:text-primary transition-colors">Rankings</a>
            <a href="#metodologia" className="hover:text-primary transition-colors">Metodologia</a>
            <a href="#guias" className="hover:text-primary transition-colors">Guias Educativos</a>
            <a href="#jogo-responsavel" className="hover:text-primary transition-colors">Jogo Responsável</a>
          </nav>

          <div className="flex items-center gap-3">
            <Badge variant="outline" className="border-emerald-500/30 text-emerald-400 bg-emerald-950/20 px-2.5 py-1 text-xs font-semibold gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              Conteúdo Verificado
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-28 border-b border-border/40 bg-gradient-to-b from-card/30 via-background to-background">
        {/* Elemento Decorativo de Fundo */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary/5 rounded-full blur-3xl pointer-events-none"></div>

        <div className="container relative z-10 grid lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6 text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-primary/20 bg-primary/5 text-primary text-xs font-semibold">
              <Award className="h-3.5 w-3.5" />
              <span>Análise Técnica e Isenta de Operadores</span>
            </div>
            
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-serif font-bold tracking-tight text-white leading-[1.1]">
              Decisões Inteligentes em <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-amber-400 to-primary">Cassinos Online</span> no Brasil
            </h1>
            
            <p className="text-muted-foreground text-base sm:text-lg max-w-2xl leading-relaxed">
              O CasinoRadar é um portal independente que avalia operadores com base em critérios técnicos estritos de segurança, conformidade legal, clareza nos bônus e eficiência de pagamento. Ajudamos você a pesquisar antes de apostar.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-background font-semibold px-8 shadow-lg shadow-primary/20" onClick={() => window.location.href = "#rankings"}>
                Ver Rankings Técnicos
              </Button>
              <Button size="lg" variant="outline" className="border-border hover:bg-card text-white px-8" onClick={() => window.location.href = "#metodologia"}>
                Nossa Metodologia
              </Button>
            </div>

            <div className="grid grid-cols-3 gap-6 pt-8 border-t border-border/40 max-w-md">
              <div>
                <p className="text-2xl font-serif font-bold text-white">100%</p>
                <p className="text-xs text-muted-foreground">Foco em Segurança</p>
              </div>
              <div>
                <p className="text-2xl font-serif font-bold text-white">SPA/MF</p>
                <p className="text-xs text-muted-foreground">Fontes Oficiais</p>
              </div>
              <div>
                <p className="text-2xl font-serif font-bold text-white">20+</p>
                <p className="text-xs text-muted-foreground">Guias de Estudo</p>
              </div>
            </div>
          </div>

          {/* Destaque do Mês Card */}
          <div className="lg:col-span-5">
            <div className="bg-gradient-to-b from-card to-card/90 border border-primary/20 rounded-2xl p-6 shadow-xl relative overflow-hidden group">
              {/* Brilho sutil no hover */}
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <div className="absolute top-0 right-0 bg-primary text-background text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-bl-xl">
                Destaque do Mês
              </div>

              <div className="space-y-5">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-serif text-xl font-bold">
                    SV
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white font-serif">SpinVegas</h3>
                    <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                      <span className="text-primary font-bold">★ 4.9</span>
                      <span>•</span>
                      <span>Autorizado SPA/MF</span>
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-background/50 border border-border/40 space-y-2">
                  <p className="text-[10px] text-muted-foreground uppercase tracking-widest font-semibold">Bônus de Boas-Vindas</p>
                  <p className="text-base font-bold text-primary">100% até R$ 5.000 + 150 Rodadas Grátis</p>
                  <div className="flex justify-between text-xs text-muted-foreground pt-2 border-t border-border/20">
                    <span>Dep. Mínimo: <strong>R$ 10</strong></span>
                    <span>Saque: <strong>Imediato (Pix)</strong></span>
                  </div>
                </div>

                <div className="space-y-2 text-xs text-muted-foreground">
                  <p className="flex items-center gap-2">
                    <CheckCircle className="h-3.5 w-3.5 text-primary shrink-0" />
                    <span>Licença ativa sob regulação federal brasileira</span>
                  </p>
                  <p className="flex items-center gap-2">
                    <CheckCircle className="h-3.5 w-3.5 text-primary shrink-0" />
                    <span>Termos de rollover explicados de forma clara</span>
                  </p>
                </div>

                <Button className="w-full bg-primary hover:bg-primary/90 text-background font-bold py-5 rounded-xl transition-all" onClick={() => handleAction("SpinVegas")}>
                  Acessar Site & Verificar Bônus
                  <ArrowUpRight className="ml-2 h-4 w-4" />
                </Button>
                
                <p className="text-[10px] text-center text-muted-foreground">
                  *Sempre consulte os Termos & Condições diretamente no operador.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Rankings Section */}
      <section id="rankings" className="py-20 bg-background border-b border-border/40">
        <div className="container space-y-12">
          <div className="text-center max-w-3xl mx-auto space-y-4">
            <h2 className="text-3xl sm:text-4xl font-serif font-bold text-white">
              Operadores Verificados no Brasil
            </h2>
            <p className="text-muted-foreground text-sm sm:text-base">
              Abaixo apresentamos a nossa seleção de cassinos que cumprem os requisitos de segurança e possuem autorização ativa ou em andamento junto ao Ministério da Fazenda. Use os filtros para refinar sua busca.
            </p>

            {/* Search and Filters */}
            <div className="flex flex-col sm:flex-row gap-4 max-w-xl mx-auto pt-4">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Pesquisar por nome ou bônus..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-card border border-border rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                />
              </div>
            </div>
          </div>

          {/* Casinos Grid/Table */}
          <div className="space-y-4 max-w-5xl mx-auto">
            {filteredCasinos.length > 0 ? (
              filteredCasinos.map((casino, index) => {
                const isExpanded = expandedCasino === casino.id;
                return (
                  <div 
                    key={casino.id}
                    className={`bg-card border transition-all duration-300 rounded-xl overflow-hidden ${
                      isExpanded ? "border-primary/40 shadow-lg shadow-primary/5" : "border-border/60 hover:border-border"
                    }`}
                  >
                    {/* Main Row */}
                    <div className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-6">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 rounded-lg bg-secondary flex items-center justify-center text-primary font-serif text-lg font-bold border border-border">
                          {casino.name.substring(0, 2)}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-primary font-bold">#{index + 1}</span>
                            <h3 className="text-lg font-bold text-white font-serif">{casino.name}</h3>
                            <Badge variant="outline" className="border-primary/20 text-primary bg-primary/5 text-[10px] px-2 py-0.5">
                              ★ {casino.rating}
                            </Badge>
                          </div>
                          <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                            <Shield className="h-3 w-3 text-emerald-500" />
                            Licença: <span className="text-emerald-400 font-mono">{casino.license}</span>
                          </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-8 flex-1 max-w-md">
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Bônus</p>
                          <p className="text-xs font-bold text-white mt-0.5 line-clamp-1">{casino.bonus}</p>
                        </div>
                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Dep. Mínimo</p>
                          <p className="text-xs font-semibold text-white mt-0.5">{casino.minDeposit}</p>
                        </div>
                        <div className="col-span-2 md:col-span-1">
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold">Saque</p>
                          <p className="text-xs font-semibold text-white mt-0.5 flex items-center gap-1">
                            <Clock className="h-3 w-3 text-primary" />
                            {casino.payoutTime}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2.5">
                        <Button 
                          variant="outline" 
                          size="sm"
                          onClick={() => setExpandedCasino(isExpanded ? null : casino.id)}
                          className="border-border text-xs hover:bg-secondary text-white"
                        >
                          {isExpanded ? "Ocultar" : "Detalhes"}
                          <ChevronDown className={`ml-1.5 h-3.5 w-3.5 transition-transform duration-300 ${isExpanded ? "rotate-180" : ""}`} />
                        </Button>
                        <Button 
                          size="sm"
                          onClick={() => handleAction(casino.name)}
                          className="bg-primary hover:bg-primary/90 text-background font-semibold text-xs px-4"
                        >
                          Verificar
                          <ExternalLink className="ml-1.5 h-3 w-3" />
                        </Button>
                      </div>
                    </div>

                    {/* Expanded Content */}
                    {isExpanded && (
                      <div className="px-5 pb-5 pt-1 border-t border-border/40 bg-secondary/20 grid md:grid-cols-2 gap-6 animate-fadeIn">
                        <div className="space-y-3">
                          <h4 className="text-xs font-bold uppercase tracking-wider text-primary">Pontos de Destaque</h4>
                          <ul className="space-y-1.5 text-xs text-muted-foreground">
                            {casino.pros.map((pro, i) => (
                              <li key={i} className="flex items-center gap-2">
                                <span className="h-1.5 w-1.5 rounded-full bg-primary"></span>
                                {pro}
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="space-y-3">
                          <h4 className="text-xs font-bold uppercase tracking-wider text-primary">Aviso de Verificação</h4>
                          <p className="text-xs text-muted-foreground leading-relaxed">
                            Nossa equipe analisou os termos de rollover e políticas de saque deste operador. Certifique-se de que seus dados cadastrais (CPF) coincidem com a chave Pix utilizada para depósitos e saques para evitar atrasos na verificação de identidade (KYC).
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })
            ) : (
              <div className="text-center py-12 border border-dashed border-border rounded-xl">
                <Info className="h-8 w-8 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">Nenhum operador corresponde aos termos de pesquisa.</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Metodologia Section */}
      <section id="metodologia" className="py-20 bg-card/30 border-b border-border/40">
        <div className="container max-w-5xl space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-4">
            <Badge variant="outline" className="border-primary/20 text-primary bg-primary/5">Como Avaliamos</Badge>
            <h2 className="text-3xl sm:text-4xl font-serif font-bold text-white">Nossa Metodologia Editorial</h2>
            <p className="text-muted-foreground text-sm sm:text-base">
              A transparência é o nosso principal pilar. Nossas notas e posicionamentos nos rankings não são patrocinados e seguem critérios técnicos rigorosos.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-card border border-border/60 p-6 rounded-xl space-y-4">
              <div className="h-10 w-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                <Shield className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white font-serif">1. Licença e Regulação</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Verificamos ativamente a validade da licença do operador junto à Secretaria de Prêmios e Apostas (SPA/MF) do Ministério da Fazenda. Cassinos sem registro ou em situação irregular são imediatamente desqualificados.
              </p>
            </div>

            <div className="bg-card border border-border/60 p-6 rounded-xl space-y-4">
              <div className="h-10 w-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                <Coins className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white font-serif">2. Termos de Rollover</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Calculamos o custo real de cada bônus. Analisamos se as exigências de apostas são realistas para o jogador comum e se os prazos de validade das ofertas são adequados e transparentes.
              </p>
            </div>

            <div className="bg-card border border-border/60 p-6 rounded-xl space-y-4">
              <div className="h-10 w-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                <UserCheck className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-bold text-white font-serif">3. Práticas de Pagamento</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Avaliamos a velocidade de processamento dos saques via Pix, a presença de limites diários ocultos e a clareza nas exigências de verificação de identidade (KYC) antes do primeiro saque.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Guides Section */}
      <section id="guias" className="py-20 bg-background border-b border-border/40">
        <div className="container max-w-5xl space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-4">
            <Badge variant="outline" className="border-primary/20 text-primary bg-primary/5">Conteúdo Educativo</Badge>
            <h2 className="text-3xl sm:text-4xl font-serif font-bold text-white">Guias Completos para Apostadores</h2>
            <p className="text-muted-foreground text-sm sm:text-base">
              Nossa equipe escreve artigos aprofundados para ajudar você a entender o ecossistema de apostas online de forma crítica e analítica.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 gap-6">
            {GUIDES_DATA.map((guide) => {
              const IconComp = guide.icon;
              return (
                <div 
                  key={guide.id}
                  onClick={() => handlePlaceholderClick(guide.title)}
                  className="bg-card border border-border/60 p-6 rounded-xl hover:border-primary/30 transition-all duration-300 cursor-pointer group flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] text-primary font-bold uppercase tracking-wider">{guide.category}</span>
                      <span className="text-[10px] text-muted-foreground">{guide.words} palavras</span>
                    </div>
                    <h3 className="text-lg font-bold text-white font-serif group-hover:text-primary transition-colors">
                      {guide.title}
                    </h3>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      {guide.desc}
                    </p>
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-primary font-semibold pt-2">
                    <span>Ler guia completo</span>
                    <ArrowUpRight className="h-3.5 w-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Jogo Responsável Section */}
      <section id="jogo-responsavel" className="py-20 bg-emerald-950/10 border-b border-emerald-900/20">
        <div className="container max-w-4xl bg-card border border-emerald-900/30 p-8 sm:p-12 rounded-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 h-32 w-32 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none"></div>
          
          <div className="space-y-6 relative z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/20 bg-emerald-500/5 text-emerald-400 text-xs font-semibold">
              <Scale className="h-3.5 w-3.5" />
              <span>Compromisso com o Jogo Responsável</span>
            </div>

            <h2 className="text-3xl font-serif font-bold text-white">
              Apostas devem ser uma forma de entretenimento, nunca uma solução financeira
            </h2>

            <p className="text-muted-foreground text-sm sm:text-base leading-relaxed">
              O CasinoRadar apoia firmemente as diretrizes de Jogo Responsável estabelecidas pela legislação brasileira. Incentivamos todos os usuários a definirem limites estritos de depósito, perda e tempo de sessão antes de iniciar qualquer atividade de aposta.
            </p>

            <div className="grid sm:grid-cols-2 gap-6 pt-4 border-t border-border/40">
              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  Defina Limites Claros
                </h4>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Nunca jogue com dinheiro destinado a despesas essenciais (aluguel, alimentação, saúde). Estabeleça um orçamento mensal de entretenimento e cumpra-o rigorosamente.
                </p>
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  Reconheça os Sinais
                </h4>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Se você sentir necessidade de recuperar perdas, mentir sobre seus hábitos de aposta ou deixar de cumprir obrigações pessoais para jogar, busque ajuda especializada imediatamente.
                </p>
              </div>
            </div>

            <div className="pt-6 flex flex-wrap gap-4 items-center">
              <span className="text-xs text-muted-foreground">Precisa de ajuda ou orientação?</span>
              <a 
                href="https://falabr.cgu.gov.br/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs text-emerald-400 hover:text-emerald-300 font-semibold flex items-center gap-1.5 underline"
              >
                Canais de Apoio do Governo Federal
                <ExternalLink className="h-3 w-3" />
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-card/40 border-t border-border/60 py-12 text-xs text-muted-foreground">
        <div className="container max-w-5xl space-y-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 pb-8 border-b border-border/40">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center text-background font-serif text-base font-bold">
                ♠
              </div>
              <div>
                <span className="font-serif text-base font-bold text-white block">CasinoRadar</span>
                <span className="text-[9px] uppercase tracking-wider text-muted-foreground block">Guia de Escolha Segura</span>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-6 text-xs font-medium">
              <a href="#rankings" className="hover:text-primary transition-colors">Rankings</a>
              <a href="#metodologia" className="hover:text-primary transition-colors">Metodologia</a>
              <a href="#guias" className="hover:text-primary transition-colors">Guias</a>
              <a href="#jogo-responsavel" className="hover:text-primary transition-colors">Jogo Responsável</a>
            </div>
          </div>

          <div className="space-y-4">
            <p className="leading-relaxed">
              O CasinoRadar é um portal informativo e educativo independente. Não operamos jogos de azar e não recebemos depósitos de jogadores. Todas as avaliações, pontuações e rankings são elaborados de acordo com nossa metodologia editorial técnica e independente.
            </p>
            <p className="leading-relaxed">
              A exploração de apostas de quota fixa no Brasil é regulamentada pela Lei nº 14.790/2023 e supervisionada pela Secretaria de Prêmios e Apostas do Ministério da Fazenda (SPA/MF). O cadastro e participação em plataformas de apostas são estritamente proibidos para menores de 18 anos.
            </p>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pt-4 text-[10px] border-t border-border/20">
              <p>© {new Date().getFullYear()} CasinoRadar. Todos os direitos reservados. Conteúdo estritamente informativo.</p>
              <div className="flex gap-4">
                <a href="#" onClick={(e) => { e.preventDefault(); toast.info("Política de Privacidade em conformidade com a LGPD."); }} className="hover:text-white transition-colors">Privacidade</a>
                <a href="#" onClick={(e) => { e.preventDefault(); toast.info("Termos de Uso do portal CasinoRadar."); }} className="hover:text-white transition-colors">Termos de Uso</a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
