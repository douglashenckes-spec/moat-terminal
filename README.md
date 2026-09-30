# JP Morgan | Charlie Munger B3 Screener & Diagnostic Terminal

> *"É muito melhor comprar uma empresa maravilhosa a um preço justo do que uma empresa justa a um preço maravilhoso."*  
> — **Charlie Munger**

Aplicação analítica institucional de alta performance para triagem e diagnóstico de ações listadas na B3 (Brasil), desenvolvida sob os mais rigorosos padrões de Equity Research do JP Morgan e certificação CFA.

---

## 🏛️ Filosofia e Arquitetura do Duplo Filtro

A aplicação separa rigidamente a qualidade intrínseca do negócio do preço de tela: **múltiplos de preço NÃO afetam o Quality Score**.

### Filtro 1: Business Quality Score (0 a 100)
Avalia a resiliência estrutural, eficiência na alocação de capital e vantagens competitivas sustentáveis (*Moats*):
1. **Rentabilidade e Eficiência do Capital (Peso: 40%)**
   - **ROIC:** >18% (Nota 100) | 12%–18% (Nota 75) | 8%–12% (Nota 50) | <8% (Nota 20)
   - **ROE:** >20% (Nota 100) | 14%–20% (Nota 75) | 10%–14% (Nota 50) | <10% (Nota 20)
   - **Margem Líquida:** >15% (Nota 100) | 10%–15% (Nota 75) | 5%–10% (Nota 50) | <5% (Nota 25)
2. **Solidez Financeira & Balanço (Peso: 35%)**
   - **Dívida Líquida / EBITDA:** <0x (Caixa Líquido = Nota 100) | 0x–1,5x (Nota 90) | 1,5x–2,5x (Nota 70) | 2,5x–3,5x (Nota 40) | >3,5x (Nota 0)
   - **Liquidez Corrente:** >1,8x (Nota 100) | 1,3x–1,8x (Nota 80) | 1,0x–1,3x (Nota 50) | <1,0x (Nota 15)
3. **Consistência e Defensibilidade (Peso: 25%)**
   - **Crescimento de Receita (5 anos):** >10% a.a. (Nota 100) | 5%–10% (Nota 70) | 0%–5% (Nota 40) | <0% (Nota 10)
   - **Margem Bruta:** >30% (Nota 100) | 20%–30% (Nota 70) | <20% (Nota 40)

**Classificação:**
- **Score ≥ 80:** *Tier 1: Classe Mundial (Wide / Narrow Moat)*
- **Score 65 a 79:** *Tier 2: Empresa Sólida / Saudável*
- **Score 50 a 64:** *Tier 3: Operação Medíocre / Concorrência Predatória*
- **Score < 50:** *Tier 4: Risco Estrutural / Destruidor de Valor*

---

### Filtro 2: Condição de Entrada (Entry Valuation & Margin of Safety)
Avalia a assimetria risco/retorno sem recorrer a modelos especulativos de fluxo de caixa descontado (DCF) perpétuo:
- **Earnings Yield ($1 / [P/L]$):** Retorno operacional de lucros sobre o valor da ação.
- **P/L e EV/EBITDA:** Múltiplos relativos de mercado.
- **Status Institucional:**
  - 🟢 **ZONA DE ASSIMETRIA FAVORÁVEL:** P/L < 8x, Earnings Yield > 12,5%, EV/EBITDA < 6x.
  - 🟡 **PREÇO JUSTO / CARREGO:** P/L 8x a 14x, Earnings Yield 7% a 12,5%.
  - 🔴 **ENTRADA ESTICADA / CARA:** P/L > 15x ou EV/EBITDA > 10x (risco de compressão de múltiplos).

---

## 📡 Pipeline de Dados 100% Fundamentus & Auditoria Ativa

- **Fonte Oficial Única:** Raspagem direta resiliente do Fundamentus (`resultado.php` e `detalhes.php?papel={TICKER}`).
- **Carimbo de Auditoria:** Exibição explícita de timestamp em horário de Brasília (`Auditado via Fundamentus em: DD/MM/AAAA HH:MM:SS`).
- **Filtro de Corte Institucional:** Descarte automático de ativos com Liquidez Média Diária (2 meses) < R$ 1.000.000 (prevenção de armadilhas de iliquidez).
- **Tratamento de Dados:** Dados numéricos brasileiros convertidos rigorosamente; campos ausentes sinalizados como `N/D` auditado, sem jamais imputar médias artificiais.
- **Cache com TTL:** Cache local de 15 minutos para velocidade máxima de consulta e proteção contra requisições repetidas ao servidor.

---

## 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar a aplicação:**
   ```bash
   streamlit run app.py
   ```
   Acesse no navegador: `http://localhost:8501`.

3. **Executar os testes unitários:**
   ```bash
   python -m unittest discover -s tests
   ```
