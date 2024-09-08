# ₿itPricePrev 🪙

BitPricePrev é uma aplicação interativa desenvolvida com Streamlit para visualizar o preço atual de criptomoedas como Bitcoin, Ethereum e Dogecoin. A aplicação também exibe gráficos de preços históricos e previsões de preços futuros utilizando modelos de aprendizado de máquina.

<img src="./assets/bpp_diagram.svg">

## 🛠️ Tecnologias Usadas

- **Streamlit**: Framework para criação de aplicativos web interativos.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Plotly**: Biblioteca para criação de gráficos interativos.
- **Scikit-learn**: Biblioteca para aprendizado de máquina.
- **TensorFlow**: Biblioteca para construção e treinamento de modelos de aprendizado profundo.
- **Keras**: Biblioteca de alto nível para construção e treinamento de redes neurais, integrada ao TensorFlow.


## 📥 Rodando localmente

Clone o projeto

```bash
git clone https://github.com/jvictorferreira3301/BitPricePrev.git
```

Entre no diretório do projeto

```bash
cd BitPricePrev
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Inicie o servidor

```bash
streamlit run src/bpp.py
```

## 📊 Estrutura do Projeto

```plaintext
BitPricePrev/
├── assets/                 # Arquivos de mídia e diagramas
├── src/                    # Código fonte da aplicação
│   ├── bpp.py              # Arquivo principal da aplicação Streamlit
│   ├── data_fetcher.py     # Funções para obter dados de criptomoedas
│   ├── predictor.py        # Funções para previsão de preços
│   └── in_utils.py         # Funções, por ora, (in)utilitárias
├── requirements.txt        # Arquivo de dependências
└── README.md               # Este arquivo
```