# ₿ BitPricePrev - Análise e Previsão de Criptomoedas

<div align="center">

![BitPricePrev](assets/bpp_diagram.svg)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

## Sobre o Projeto

Aplicação web desenvolvida em Python que combina análise técnica com modelos de machine learning para fornecer insights e previsões sobre o mercado cripto.

- 🎯 **Interface Intuitiva**: Dashboard responsivo desenvolvido com Streamlit
- 🤖 **Múltiplos Modelos de IA**: LSTM, Random Forest e Regressão Linear
- 📊 **Análise Técnica Completa**: Indicadores profissionais e gráficos interativos
- 🌍 **Dados em Tempo Real**: Integração com API CoinGecko
- 📈 **Visualizações Avançadas**: Gráficos candlestick, indicadores técnicos e comparações
- 🎯 **Sinais de Trading**: Recomendações automáticas baseadas em indicadores

## Funcionalidades

### Análise de Preços
- **Gráficos Interativos**: Visualização de preços históricos com Plotly
- **Médias Móveis**: MA 7, 21 e 50 dias
- **Análise de Volume**: Correlação preço-volume
- **Estatísticas Descritivas**: Métricas completas do período selecionado

### 🔮 Modelos de Previsão

#### LSTM (Long Short-Term Memory)
- Rede neural recorrente especializada em séries temporais
- Arquitetura com múltiplas camadas e dropout
- Otimizada para capturar padrões complexos de longo prazo

#### Random Forest
- Ensemble de árvores de decisão
- Utiliza indicadores técnicos como features
- Robusto contra overfitting

#### Regressão Linear
- Modelo baseline com indicadores técnicos
- Rápido e interpretável
- Útil para comparação de performance

### Indicadores Técnicos

| Indicador | Descrição | Uso |
|-----------|-----------|-----|
| **RSI** | Relative Strength Index | Identificar sobrecompra/sobrevenda |
| **Bandas de Bollinger** | Volatilidade e suporte/resistência | Pontos de entrada/saída |
| **MACD** | Moving Average Convergence Divergence | Momentum e tendência |
| **Médias Móveis** | Tendência de curto/médio/longo prazo | Direção do mercado |
| **Volatilidade** | Desvio padrão dos retornos | Gestão de risco |

### Sinais de Trading
- **Sinais de Compra**: RSI < 30, cruzamento dourado das MAs
- **Sinais de Venda**: RSI > 70, cruzamento da morte das MAs
- **Análise de Tendência**: Detecção de padrões de alta/baixa
- **Recomendações Consolidadas**: Combinação de múltiplos sinais

### 🪙 Criptomoedas Suportadas

| Crypto | Símbolo | Crypto | Símbolo |
|--------|---------|--------|---------|
| Bitcoin | BTC | Litecoin | LTC |
| Ethereum | ETH | Avalanche | AVAX |
| Dogecoin | DOGE | Polygon | MATIC |
| Binance Coin | BNB | Cosmos | ATOM |
| Cardano | ADA | NEAR Protocol | NEAR |
| Solana | SOL | Algorand | ALGO |
| XRP | XRP | Fantom | FTM |
| Polkadot | DOT | TRON | TRX |
| Chainlink | LINK | Stellar | XLM |
| E mais... | | Monero | XMR |

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/jvictorferreira3301/BitPricePrev.git
cd BitPricePrev
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
streamlit run src/bpp.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

## Como Usar

### 1. Seleção de Criptomoeda
- Use o seletor na barra lateral para escolher a criptomoeda
- Visualize informações básicas e links oficiais

### 2. Configuração de Análise
- **Período Histórico**: 30 dias a 1 ano
- **Dias de Previsão**: 1 a 90 dias
- **Modelo de IA**: LSTM, Random Forest, Linear ou Todos

### 3. Navegação por Abas

#### Análise de Preços
- Gráficos de preços com médias móveis
- Análise de volume (quando disponível)
- Estatísticas do período selecionado

#### Previsões
- Comparação entre modelos
- Métricas de performance (MAE, RMSE, R²)
- Tabela detalhada de previsões

#### Análise Técnica
- Gráfico candlestick completo
- Indicadores sobrepostos
- Sinais de trading automáticos

#### Indicadores
- Valores atuais dos indicadores
- Interpretação automática
- Métricas de volatilidade

#### Comparação
- Compare múltiplas criptomoedas
- Gráficos comparativos
- Tabela de dados consolidada

## 🤖 Detalhes dos Modelos

### Métricas de Avaliação

| Métrica | Descrição | Interpretação |
|---------|-----------|---------------|
| **MAE** | Mean Absolute Error | Erro médio absoluto (menor = melhor) |
| **RMSE** | Root Mean Square Error | Raiz do erro quadrático médio |
| **R²** | Coeficiente de Determinação | Qualidade do ajuste (0-1, maior = melhor) |
| **MAPE** | Mean Absolute Percentage Error | Erro percentual médio |

### Arquitetura LSTM

```python
model = Sequential([
    LSTM(100, return_sequences=True, input_shape=(60, 1)),
    Dropout(0.2),
    LSTM(100, return_sequences=True),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25),
    Dense(1)
])
```

## Roadmap

### Versão 2.0
- [ ] **Alertas em Tempo Real**: Notificações por email/webhook
- [ ] **Backtesting**: Sistema de teste de estratégias
- [ ] **API RESTful**: Endpoints para integração externa
- [ ] **Modo Escuro**: Tema alternativo para a interface

### Versão 2.1
- [ ] **Mais Exchanges**: Dados de múltiplas fontes
- [ ] **Portfolio Tracker**: Acompanhamento de carteira
- [ ] **Análise Fundamental**: Métricas on-chain
- [ ] **Modelo Ensemble**: Combinação inteligente de previsões

## ⚠️ Disclaimer

**IMPORTANTE**: Esta aplicação é destinada apenas para fins educacionais e de pesquisa. 

- ❌ **NÃO** constitui aconselhamento financeiro
- ❌ **NÃO** garante lucros ou previne perdas
- ❌ **NÃO** deve ser usado como única fonte para decisões de investimento

**Sempre faça sua própria pesquisa (DYOR) e consulte profissionais qualificados antes de investir em criptomoedas.**

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela!**

[![GitHub stars](https://img.shields.io/github/stars/jvictorferreira3301/BitPricePrev.svg?style=social&label=Star)](https://github.com/jvictorferreira3301/BitPricePrev)

</div>
