"""
build_legal_pages.py
====================
Gera as páginas institucionais obrigatórias para aprovação no Google AdSense
e conformidade com a LGPD (Lei nº 13.709/2018):
1. privacidade.html (Política de Privacidade com cláusula Google AdSense/DART)
2. termos.html (Termos de Uso e Isenção CVM nº 20/2021)
"""

import os
import shutil

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
BRAIN_DIR = r"C:\Users\dougl\.gemini\antigravity\brain\19bf6b03-9073-46f6-9498-57b18f1f9a41"

PRIVACY_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Política de Privacidade • MOAT TERMINAL</title>
  <meta name="description" content="Política de Privacidade e Proteção de Dados do MOAT TERMINAL em conformidade com a LGPD e Google AdSense.">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- GOOGLE ADSENSE -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8661500874049196" crossorigin="anonymous"></script>

  <!-- Google Analytics 4 (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QJPB4NM5PW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-QJPB4NM5PW');
  </script>
  <style>
    body { font-family: 'Inter', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#F8FAFC] text-slate-800 min-h-screen flex flex-col">

  <!-- Header Institucional -->
  <header class="bg-white border-b border-slate-200 px-4 sm:px-8 py-3.5 flex items-center justify-between sticky top-0 z-20 shadow-xs">
    <a href="index.html" class="flex items-center gap-2.5 text-slate-900 hover:text-emerald-700 transition">
      <div class="w-8 h-8 rounded-xl bg-slate-950 flex items-center justify-center text-white shadow-xs">
        <svg class="w-4 h-4 text-emerald-400 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3"/></svg>
      </div>
      <div class="flex flex-col">
        <span class="font-bold text-xs tracking-wider font-mono">MOAT TERMINAL</span>
        <span class="text-[10px] text-slate-500 font-mono">Economic Moats &amp; Compounding</span>
      </div>
    </a>
    <a href="index.html" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-800 text-xs font-mono font-semibold transition flex items-center gap-1.5">
      <span>←</span> <span>Voltar ao Terminal</span>
    </a>
  </header>

  <!-- Conteúdo Central -->
  <main class="flex-1 max-w-4xl mx-auto w-full p-4 sm:p-8 space-y-6">
    
    <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-6">
      
      <div>
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-mono font-bold uppercase mb-2">
          <span>🔒 Privacidade &amp; LGPD</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold font-mono text-slate-950">
          Política de Privacidade
        </h1>
        <p class="text-xs text-slate-500 font-mono mt-1">
          Última atualização: 29 de setembro de 2026 • Em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018) e Requisitos Google AdSense
        </p>
      </div>

      <div class="prose prose-slate max-w-none text-xs sm:text-sm text-slate-600 leading-relaxed space-y-4">
        
        <p>
          O <b>MOAT TERMINAL</b> ("nós", "nosso" ou "plataforma") preza pela transparência, privacidade e proteção dos dados dos usuários que acessam nossos serviços de inteligência fundamentalista e pesquisa quantitativa de mercado. Esta Política descreve como coletamos, tratamos e protegemos suas informações.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          1. Informações que Coletamos
        </h2>
        <p>
          O <b>MOAT TERMINAL</b> não exige cadastro obrigatório para consulta pública. Coletamos apenas dados técnicos essenciais:
        </p>
        <ul class="list-disc pl-5 space-y-1">
          <li><b>Dados de Navegação e Dispositivo:</b> endereço IP, tipo de navegador, resolução de tela, páginas consultadas e tempo de permanência, coletados automaticamente para otimização da interface e telemetria de tráfego.</li>
          <li><b>Preferências Locais (Local Storage):</b> preferências de layout salvas localmente no seu dispositivo (como estado recolhido do banner ou filtros selecionados), sem transmissão a servidores externos.</li>
          <li><b>Comunicação Voluntária:</b> endereço de e-mail e conteúdo de mensagens quando você entra em contato conosco para sugestões ou suporte.</li>
        </ul>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          2. Uso de Cookies e Google AdSense
        </h2>
        <p>
          Utilizamos cookies para aprimorar sua experiência de navegação e exibir conteúdos relevantes:
        </p>
        <ul class="list-disc pl-5 space-y-1">
          <li><b>Cookies Essenciais:</b> necessários para o funcionamento técnico da plataforma e preservação das suas escolhas de navegação.</li>
          <li><b>Google AdSense e Fornecedores Terceiros:</b> O Google, como fornecedor de anúncios terceirizado, utiliza cookies (incluindo o cookie DoubleClick/DART) para veicular anúncios neste site com base nas visitas anteriores dos usuários a este ou a outros sites na internet.</li>
          <li><b>Desativação de Anúncios Personalizados:</b> Os usuários podem optar por desativar a publicidade personalizada acessando as <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer" class="text-emerald-700 underline font-semibold">Configurações de Anúncios do Google</a> ou pelo portal <a href="https://www.aboutads.info" target="_blank" rel="noopener noreferrer" class="text-emerald-700 underline font-semibold">aboutads.info</a>.</li>
        </ul>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          3. Finalidade do Tratamento dos Dados
        </h2>
        <p>
          Os dados coletados destinam-se exclusivamente a:
        </p>
        <ul class="list-disc pl-5 space-y-1">
          <li>Garantir a estabilidade, velocidade e segurança da infraestrutura contra ataques cibernéticos e acessos automatizados abusivos (DDoS).</li>
          <li>Aperfeiçoar as ferramentas analíticas, responsividade para telas móveis e usabilidade das matrizes financeiras.</li>
          <li>Viabilizar a sustentabilidade econômica do projeto por meio de publicidade não intrusiva e parcerias credenciadas.</li>
        </ul>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          4. Seus Direitos (LGPD - Lei nº 13.709/2018)
        </h2>
        <p>
          Você tem o direito de solicitar a qualquer momento a confirmação da existência de tratamento, acesso aos dados, correção de dados incompletos ou inexatos, anonimização, bloqueio ou eliminação de dados desnecessários, nos termos do artigo 18 da LGPD.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          5. Isenção sobre Dados de Mercado e Financeiros
        </h2>
        <p>
          As cotações, demonstrativos contábeis, múltiplos e notas de qualidade (Moat Score) exibidos no terminal provêm de fontes públicas auditadas (Comissão de Valores Mobiliários - CVM e B3). Esses dados referem-se estritamente a pessoas jurídicas abertas e métricas econômicas, não configurando dados pessoais de qualquer natureza.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          6. Contato com o Encarregado de Dados
        </h2>
        <p>
          Para esclarecimento de dúvidas sobre esta Política de Privacidade ou para exercer seus direitos sob a LGPD, entre em contato através do e-mail: 
          <a href="mailto:privacidade@moatterminal.com.br" class="text-emerald-700 font-mono font-bold underline">privacidade@moatterminal.com.br</a>.
        </p>

      </div>

    </div>

  </main>

  <!-- Rodapé -->
  <footer class="bg-white border-t border-slate-200 py-6 px-4 text-center text-xs text-slate-500 font-mono space-y-2">
    <div class="flex items-center justify-center gap-4 flex-wrap">
      <a href="index.html" class="hover:text-emerald-700 transition">Terminal</a>
      <span>•</span>
      <a href="termos.html" class="hover:text-emerald-700 transition">Termos de Uso</a>
      <span>•</span>
      <span class="text-slate-900 font-bold">Política de Privacidade</span>
    </div>
    <p class="text-[11px] text-slate-400">
      © 2026 MOAT TERMINAL PRO • Economic Moats &amp; Capital Compounding • Todos os direitos reservados.
    </p>
  </footer>

</body>
</html>
"""

TERMS_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Termos de Uso &amp; Isenção CVM • MOAT TERMINAL</title>
  <meta name="description" content="Termos de Uso e Termo de Isenção de Responsabilidade CVM nº 20/2021 do MOAT TERMINAL.">
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <!-- GOOGLE ADSENSE -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8661500874049196" crossorigin="anonymous"></script>

  <!-- Google Analytics 4 (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QJPB4NM5PW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-QJPB4NM5PW');
  </script>
  <style>
    body { font-family: 'Inter', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
  </style>
</head>
<body class="bg-[#F8FAFC] text-slate-800 min-h-screen flex flex-col">

  <!-- Header Institucional -->
  <header class="bg-white border-b border-slate-200 px-4 sm:px-8 py-3.5 flex items-center justify-between sticky top-0 z-20 shadow-xs">
    <a href="index.html" class="flex items-center gap-2.5 text-slate-900 hover:text-emerald-700 transition">
      <div class="w-8 h-8 rounded-xl bg-slate-950 flex items-center justify-center text-white shadow-xs">
        <svg class="w-4 h-4 text-emerald-400 stroke-[2.2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M3 10h18M5 10v11M19 10v11M9 10v11M15 10v11M4 10l2-6h12l2 6M9 4v3M15 4v3"/></svg>
      </div>
      <div class="flex flex-col">
        <span class="font-bold text-xs tracking-wider font-mono">MOAT TERMINAL</span>
        <span class="text-[10px] text-slate-500 font-mono">Economic Moats &amp; Compounding</span>
      </div>
    </a>
    <a href="index.html" class="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-800 text-xs font-mono font-semibold transition flex items-center gap-1.5">
      <span>←</span> <span>Voltar ao Terminal</span>
    </a>
  </header>

  <!-- Conteúdo Central -->
  <main class="flex-1 max-w-4xl mx-auto w-full p-4 sm:p-8 space-y-6">
    
    <div class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-6">
      
      <div>
        <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded-md bg-amber-50 text-amber-900 border border-amber-200 text-xs font-mono font-bold uppercase mb-2">
          <span>⚖️ Termos &amp; Conformidade CVM</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-bold font-mono text-slate-950">
          Termos de Uso &amp; Aviso Legal
        </h1>
        <p class="text-xs text-slate-500 font-mono mt-1">
          Última atualização: 29 de setembro de 2026 • Em conformidade com a Resolução CVM nº 20/2021
        </p>
      </div>

      <!-- Aviso Destaque CVM -->
      <div class="p-4 rounded-xl bg-amber-50/80 border border-amber-300 text-amber-950 text-xs sm:text-sm leading-relaxed space-y-1.5">
        <div class="font-mono font-bold text-amber-900 uppercase text-xs tracking-wider flex items-center gap-2">
          <span>⚠️</span> AVISO REGULATÓRIO FUNDAMENTAL (RESOLUÇÃO CVM Nº 20/2021)
        </div>
        <p>
          O <b>MOAT TERMINAL</b> é uma ferramenta de computação analítica, pesquisa quantitativa e organização de dados contábeis de <b>finalidade estritamente educacional e informativa</b>. 
          Nenhum conteúdo, algoritmo, pontuação (Moat Score), enquadramento de múltiplos ou visualização gráfica <b>constitui relatório de análise, consultoria de investimentos, oferta pública ou recomendação de compra e venda de valores mobiliários</b>.
        </p>
      </div>

      <div class="prose prose-slate max-w-none text-xs sm:text-sm text-slate-600 leading-relaxed space-y-4">
        
        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          1. Aceitação dos Termos
        </h2>
        <p>
          Ao acessar e navegar pelo <b>MOAT TERMINAL</b>, você declara ter lido, compreendido e concordado integralmente com as disposições destes Termos de Uso e com nossa Política de Privacidade. Caso discorde de qualquer cláusula, solicitamos a descontinuação imediata do uso da plataforma.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          2. Natureza dos Dados e Ausência de Garantia
        </h2>
        <p>
          Os dados contábeis e mercadológicos consolidados na plataforma são extraídos de fontes públicas oficiais da Comissão de Valores Mobiliários (CVM) e da B3 (Brasil, Bolsa, Balcão). Embora envidemos os melhores esforços técnicos para garantir a precisão e integridade dos cálculos matemáticos:
        </p>
        <ul class="list-disc pl-5 space-y-1">
          <li>Não garantimos a isenção absoluta de erros tipográficos, atrasos nas transmissões públicas da CVM ou distorções ocasionadas por eventos corporativos atípicos.</li>
          <li>Os algoritmos de modelagem (Moat Score, assimetria valuation vs NTN-B, ROIC/ROE normalizados) expressam critérios objetivos inspirados na literatura clássica de Graham e Munger, mas não representam juízo de valor discricionário sobre o futuro de qualquer empresa.</li>
          <li><b>Rentabilidade passada não representa garantia de rentabilidade futura.</b> Investimentos em ações e renda variável envolvem risco soberano, setorial e de mercado, inclusive a possibilidade de perda do capital investido.</li>
        </ul>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          3. Responsabilidade Exclusiva do Investidor
        </h2>
        <p>
          O investidor é o único e exclusivo responsável por suas decisões patrimoniais de investimento, alocação e desinvestimento. Recomendamos enfaticamente que cada usuário realize sua própria diligência, avalie seus objetivos pessoais e perfil de risco e, quando julgar oportuno, consulte profissionais devidamente autorizados e credenciados (CNPI, CFP, CEA) antes de qualquer tomada de decisão financeira.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          4. Parcerias Comerciais e Publicidade
        </h2>
        <p>
          O MOAT TERMINAL pode veicular anúncios publicitários de terceiros (como Google AdSense) ou exibir links de afiliados de instituições financeiras credenciadas (corretoras, plataformas de imposto de renda e ferramentas parceiras). A veiculação de anúncios não implica endosso, garantia de retorno ou corresponsabilidade pelos serviços prestados por terceiros.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          5. Propriedade Intelectual
        </h2>
        <p>
          A arquitetura de software, o código-fonte, o design da interface, os layouts gráficos das matrizes 2x2 e a compilação do banco de dados são protegidos pelas leis de propriedade intelectual e direitos autorais. É vedada a reprodução comercial integral ou engenharia reversa sem autorização expressa por escrito.
        </p>

        <h2 class="text-base font-bold font-mono text-slate-900 border-b border-slate-100 pb-1 mt-6">
          6. Legislação Aplicável e Foro
        </h2>
        <p>
          Estes Termos são regidos pelas leis da República Federativa do Brasil. Para dirimir quaisquer controvérsias oriundas do presente instrumento, fica eleito o Foro da Comarca de domicílio do usuário ou da sede da mantenedora da plataforma.
        </p>

      </div>

    </div>

  </main>

  <!-- Rodapé -->
  <footer class="bg-white border-t border-slate-200 py-6 px-4 text-center text-xs text-slate-500 font-mono space-y-2">
    <div class="flex items-center justify-center gap-4 flex-wrap">
      <a href="index.html" class="hover:text-emerald-700 transition">Terminal</a>
      <span>•</span>
      <span class="text-slate-900 font-bold">Termos de Uso</span>
      <span>•</span>
      <a href="privacidade.html" class="hover:text-emerald-700 transition">Política de Privacidade</a>
    </div>
    <p class="text-[11px] text-slate-400">
      © 2026 MOAT TERMINAL PRO • Economic Moats &amp; Capital Compounding • Todos os direitos reservados.
    </p>
  </footer>

</body>
</html>
"""

def build_pages():
    priv_file = os.path.join(OUTPUT_DIR, "privacidade.html")
    with open(priv_file, "w", encoding="utf-8") as f:
        f.write(PRIVACY_HTML)
    print(f"Gerado: {priv_file}")

    terms_file = os.path.join(OUTPUT_DIR, "termos.html")
    with open(terms_file, "w", encoding="utf-8") as f:
        f.write(TERMS_HTML)
    print(f"Gerado: {terms_file}")

    # Copiar para artifacts
    if os.path.exists(BRAIN_DIR):
        shutil.copy(priv_file, os.path.join(BRAIN_DIR, "privacidade.html"))
        shutil.copy(terms_file, os.path.join(BRAIN_DIR, "termos.html"))
        print("Copiado para o diretório de artefatos com sucesso!")

if __name__ == '__main__':
    build_pages()
