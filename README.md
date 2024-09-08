# ₿itPricePrev 🪙

BitPricePrev é uma aplicação interativa desenvolvida com Streamlit para visualizar o preço atual de criptomoedas como Bitcoin, Ethereum e Dogecoin. A aplicação também exibe gráficos de preços históricos e previsões de preços futuros utilizando modelos de aprendizado de máquina.

<img src="./assets/bpp_diagram.svg">

## 🛠️ Tecnologias Usadas

- <a href='https://streamlit.io/' target="_blank"><img alt='streamlit' src='https://img.shields.io/badge/Streamlit-100000?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=FF6600&color=FF6600'/></a> : Framework para criação de aplicativos web interativos.
- ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) Biblioteca para manipulação e análise de dados.
- ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white) Biblioteca para criação de gráficos interativos.
- ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) Biblioteca para aprendizado de máquina.
- ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white) Biblioteca para construção e treinamento de modelos de aprendizado profundo.
- ![Keras](https://img.shields.io/badge/Keras-%23D00000.svg?style=for-the-badge&logo=Keras&logoColor=white) Biblioteca de alto nível para construção e treinamento de redes neurais, integrada ao TensorFlow.


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
