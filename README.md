# 📊 Dashboard de Inteligência de Vendas

Este projeto é uma aplicação de Business Intelligence interativa desenvolvida em **Python**. O dashboard transforma dados brutos de e-commerce em insights visuais, permitindo a análise de métricas de vendas, comportamento de preços e performance de marcas.

---

## Tecnologias Utilizadas
* **Linguagem:** Python  
* **Processamento de Dados:** Pandas, NumPy  
* **Visualização de Dados:** Plotly Express  
* **Desenvolvimento Web:** Dash & Dash Bootstrap Components (Layout Responsivo)

---

## Como Executar
1. **Clone este repositório:**

```Bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
```
2. **Instale as dependências:**

```Bash
pip install -r requirements.txt
```

3. **Inicie o dashboard:**
```Bash
python app.py
```

4. **Acesse em seu navegador:** ```http://127.0.0.1:8050/```

---

## Estrutura do Repositório
```bash
.
├── app.py             # Entrada da aplicação e layout
├── charts.py          # Funções de geração de gráficos
├── data_loader.py     # Script de carregamento e limpeza
├── kpis.py            # Lógica dos indicadores de performance
├── readme.md          # Documentação do Projeto
├── requirements.txt   # Dependências do projeto
└── ecommerce_estatistica.csv
```
---

## Arquitetura Modular
Diferente de scripts convencionais, este projeto foi estruturado com base em princípios de **Clean Code** e **Modularização**. A separação de responsabilidades permite que cada parte do sistema (dados, cálculos e interface) seja testada, mantida e escalada de forma independente, tornando a manutenção e alteração do código mais simples e eficiente. 

O projeto está divido em 4 módulos principais: 

### `data_loader.py`
Responsável pelo carregamento, padronização e limpeza dos dados (*Data Wrangling*).

* #### Padronização de dados:
```python
# Material
if "Material" in df.columns:
    df["Material"] = df["Material"].replace("jean", "jeans")

# Marca
if "Marca" in df.columns:
    df["Marca"] = (
        df["Marca"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.title()
    )        
```
* #### Tratamento de Erros:
```python
try:
    df = pd.read_csv(caminho_arquivo)
    ...
    return df
except Exception as e:
    print(f"Erro ao carregar os dados: {e}")
    return pd.DataFrame()
``` 
Esse trecho evita que a aplicação quebre em caso de falha no carregamento dos dados, permitindo que o sistema continue funcionando com um DataFrame vazio e trate esse cenário de forma controlada.

---
### `kpis.py`
A função centraliza o cálculo dos principais indicadores do dashboard, tratando cenários de dados vazios e possíveis ausências de colunas para garantir resultados consistentes nas visualizações.

```python
def calcular_kpis(df: pd.DataFrame) -> dict:
    # Tratamento para dataset vazio
    if df.empty:
        return {...}
    
    #Cálculo dos KPIs principais:    
    total_produtos = len(df)
    media_preco = df["Preço"].mean() if "Preço" in df.columns else 0
    total_vendas = df["Qtd_Vendidos_Cod"].sum() if "Qtd_Vendidos_Cod" in df.columns else 0
    nota_media = df["Nota"].mean() if "Nota" in df.columns else 0

    return {...}
```
A função calcular_kpis é responsável por centralizar o cálculo dos principais indicadores de desempenho do dashboard a partir de um DataFrame. Inicialmente, ela verifica se o conjunto de dados está vazio, retornando valores zerados para evitar falhas na aplicação. Em seguida, calcula métricas como total de produtos, preço médio, total de vendas e nota média, considerando possíveis ausências de colunas. Por fim, aplica validações e conversões para garantir que os resultados sejam consistentes e seguros para uso nas visualizações do dashboard.

---

### `charts.py` 
Este módulo concentra a lógica analítica e visual dos gráficos, garantindo que apenas dados válidos e representativos sejam exibidos.

* #### Função `tem_dados_suficientes`
```python
def tem_dados_suficientes(df: pd.DataFrame, minimo: int = MIN_DADOS_ESTATISTICOS) -> bool:
    return len(df) >= minimo
```
Verifica se o conjunto de dados possui volume mínimo para gerar análises confiáveis, evitando a criação de gráficos com baixa relevância estatística.

* #### Função `tem_variedade_suficiente`
```python
def tem_variedade_suficiente(df: pd.DataFrame, colunas: list[str], minimo_valores_unicos: int = 2) -> bool:
    for coluna in colunas:
    ...
    return True
```
Garante que as variáveis analisadas possuam diversidade suficiente de valores, evitando a geração de gráficos e análises com dados constantes ou pouco representativos.

* #### Funções `criar_card_grafico` e `criar_card_kpi`
```python
def criar_card_grafico(...):
    ...

def criar_card_kpi(...):
    ...
```
Funções responsáveis por encapsular gráficos e indicadores em componentes reutilizáveis, garantindo padronização visual e organização do layout do dashboard.

* #### Função `figura_vazia`
```python
def figura_vazia(titulo="Sem dados disponíveis", mensagem="Tente ajustar os filtros"):

    fig = px.scatter()
    ...
    return fig
```
Cria um estado visual para situações em que não há dados suficientes para gerar um gráfico, exibindo uma mensagem centralizada e amigável ao usuário. Essa abordagem melhora a experiência de uso e evita visualizações vazias ou enganosas.

* #### Função `criar_graficos`
```python
def criar_graficos(df: pd.DataFrame):
    
    if df.empty:
        return [figura_vazia()] * 6
    ...
    return fig1, fig2, fig3, fig4, fig5, fig6
```
Responsável por gerar todos os gráficos do dashboard de forma dinâmica, aplicando validações de dados, filtros de outliers e tratamento para cenários com dados insuficientes. A função garante consistência visual entre os gráficos e evita análises enganosas, exibindo mensagens apropriadas quando os dados não atendem aos critérios mínimos.

#### 📊 Exemplos de visualizações geradas:

**Dashboard**
<img width="1905" height="879" alt="Image" src="https://github.com/user-attachments/assets/cecf0d96-7830-4312-ad6e-98d9917fa431" />


**Distribuição de Preços**
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/10047c96-a15a-4697-b6f4-b68d6003661d" />


**Preço vs Vendas**
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/cc86a78b-e9c8-45ad-82f7-87511508c999" />


**Distribuição de produtos por marca**
<img width="1900" height="540" alt="Image" src="https://github.com/user-attachments/assets/77171961-d5e4-4cc1-966b-6c67b3dbba90" />


**Mix de materiais**
<img width="600" height="500" alt="Image" src="https://github.com/user-attachments/assets/8237fd4b-fdc9-4231-b19b-34a32db7e7e4" />


**Concentração de Notas dos Produtos**
<img width="600" height="500" alt="Image" src="https://github.com/user-attachments/assets/601facee-e7c8-4509-a8d0-3c59146d6456" />


**Vendas vs Avaliações**
<img width="600" height="500" alt="Image" src="https://github.com/user-attachments/assets/112526d3-8ee5-4343-bcbf-352a1a693efe" />

---

### `app.py`

Orquestrador principal que gerencia o layout Dash, componentes Bootstrap e os callbacks de interatividade.

* #### Inicialização da aplicação e carregamento dos dados:
```python
DADOS_CSV = "ecommerce_estatistica.csv"

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

df_global = preparar_dados(DADOS_CSV)
```
Esse trecho inicializa o aplicativo Dash com um tema Bootstrap e carrega os dados apenas uma vez na inicialização, evitando leituras repetidas do arquivo CSV.

* #### Filtro dinâmico por marca:
```python
if df_global.empty or "Marca" not in df_global.columns:
    marcas_ops = [{"label": "Sem dados", "value": "Sem dados"}]
    valor_inicial_marca = "Sem dados"
else:
    marcas_ops = [{"label": "Todas as Marcas", "value": "Todas"}] + [
        {"label": marca, "value": marca}
        for marca in sorted(df_global["Marca"].dropna().unique())
    ]
    valor_inicial_marca = "Todas"
```
Cria dinamicamente as opções do filtro de marcas a partir dos dados disponíveis, com tratamento para cenários em que o dataset esteja vazio ou sem a coluna necessária.

* #### Estrutura do layout:
```python
app.layout = dbc.Container(
    [
        dbc.Row([...]),  # Título
        dbc.Row([...]),  # Filtro
        dbc.Row([...]),  # KPIs
        dbc.Row([...]),  # Gráficos
    ],
    fluid=True,
    style={"backgroundColor": "#f8f9fa"}
)
```
Organiza o dashboard em uma estrutura responsiva usando Container, Row e Col do Bootstrap, separando título, filtro, indicadores e gráficos.

* #### Callback de atualização:
```python
@app.callback(
    [Output(f"graf{i}", "figure") for i in range(1, 7)] + [...],
    Input("filtro-marca", "value")
)
def update_dashboard(marca):
    ...
    figuras = criar_graficos(df_filtrado)
    kpis = calcular_kpis(df_filtrado)

    return list(figuras) + [...]
```
Atualiza gráficos e KPIs automaticamente com base na marca selecionada, conectando a interação do usuário às funções responsáveis pelos cálculos e visualizações.

---

## Funcionalidades e Análises
O dashboard oferece uma visão 360º da operação de vendas:
* **Filtro em Tempo Real:** Explore dados por marcas específicas de forma dinâmica.
* **Monitor de KPIs:** Acompanhamento imediato de Total de Produtos, Preço Médio, Volume de Vendas e Nota Média.
* **Análise de Elasticidade:** Visualização da relação entre Preço e Quantidade Vendida com tratamento de outliers.
* **Saúde do Produto:** Densidade de notas e correlação estatística entre avaliações e performance de vendas.

---


## Insights Extraídos

**1. Composição e Preços**
* **Dominância do Algodão:** Metade do seu mix de materiais (50,4%) é composta por algodão. Somado ao poliéster (24,1%), esses dois materiais representam quase 75% da sua oferta, indicando um foco em tecidos tradicionais e de alta rotatividade.

* **Concentração de Preços:** O histograma mostra que a maior parte dos seus 295 produtos está na faixa de R$ 50 a R$ 80. Existe uma queda nítida após os R$ 200, mostrando que o seu negócio é focado no mercado de massa ou "entry-level", com poucos itens de luxo ou ticket muito alto.

* **Ticket Médio:** O valor médio de R$ 130,84 é superior à faixa de maior frequência (R$ 50-80), o que sugere que os produtos mais caros, embora em menor quantidade, estão "puxando" a média para cima.

**2. Desempenho de Vendas e Engajamento**
* **Vendas vs. Avaliações:** O gráfico de dispersão com linha de tendência mostra uma correlação positiva forte. Isso indica que, quanto mais um produto vende, mais avaliações ele recebe. Isso é um sinal saudável de engajamento orgânico.

* **Anomalias de Venda (Outliers):** No gráfico "Preço vs Vendas", notamos produtos específicos que atingiram 50k unidades vendidas em diferentes faixas de preço (um próximo a R$ 40, outro a R$ 200 e outro a R$ 240). Esses itens são seus "best-sellers" e merecem uma análise profunda: o que faz um produto de R$ 240 vender tanto quanto um de R$ 40? Pode ser exclusividade de marca ou uma necessidade específica de mercado.

**3. Qualidade e Satisfação**
* **Alta Aprovação:** A nota média de 4,48 é excelente. O gráfico de densidade mostra que a grande massa de produtos está concentrada entre as notas 4,0 e 5,0.

* **Baixo Risco:** Há pouquíssima densidade abaixo de 3,5, indicando que você não tem problemas críticos de qualidade ou de expectativa frustrada com os clientes na maioria do catálogo.
