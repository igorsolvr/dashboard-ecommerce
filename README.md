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

**Padronização de dados:**
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
**Tratamento de Erros:**
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
Contém a lógica de negócio para cálculo automático de indicadores de desempenho.

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

## `charts.py` 
Camada isolada dedicada exclusivamente à criação de visualizações dinâmicas com Plotly.

<img width="1905" height="879" alt="Image" src="https://github.com/user-attachments/assets/1016814d-9aca-4c63-922b-c1553adacc87" />

* **`app.py`**: Orquestrador principal que gerencia o layout Dash, componentes Bootstrap e os callbacks de interatividade.

---

## Funcionalidades e Análises
O dashboard oferece uma visão 360º da operação de vendas:
* **Filtro em Tempo Real:** Explore dados por marcas específicas de forma dinâmica.
* **Monitor de KPIs:** Acompanhamento imediato de Total de Produtos, Preço Médio, Volume de Vendas e Nota Média.
* **Análise de Elasticidade:** Visualização da relação entre Preço e Quantidade Vendida com tratamento de outliers.
* **Saúde do Produto:** Densidade de notas e correlação estatística entre avaliações e performance de vendas.

---


## Insights Extraídos
* Identificação de Outliers: O uso de filtros por quantil (0.99) permitiu identificar produtos de alto valor que mantêm volume de vendas consistente.

* Prova Social: Observou-se uma correlação positiva entre o número de avaliações e a quantidade vendida, reforçando a importância do feedback do cliente.

* Eficiência de Catálogo: A análise do mix de materiais revelou oportunidades de otimização de estoque baseada na preferência histórica de consumo.
