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

* **Identificação de Outliers:** O uso de filtros por quantil (0.99) permitiu identificar produtos de alto valor que mantêm volume de vendas consistente.

* **Prova Social:** Observou-se uma correlação positiva entre o número de avaliações e a quantidade vendida, reforçando a importância do feedback do cliente.

* **Eficiência de Catálogo:** A análise do mix de materiais revelou oportunidades de otimização de estoque baseada na preferência histórica de consumo.
