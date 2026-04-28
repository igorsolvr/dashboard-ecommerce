import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output

from data_loader import preparar_dados
from charts import criar_card_grafico, criar_card_kpi, criar_graficos
from kpis import calcular_kpis, formatar_numero


DADOS_CSV = "ecommerce_estatistica.csv"

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Carrega os dados apenas uma vez na inicialização do aplicativo
df_global = preparar_dados(DADOS_CSV)

if df_global.empty or "Marca" not in df_global.columns:
    marcas_ops = [{"label": "Sem dados", "value": "Sem dados"}]
    valor_inicial_marca = "Sem dados"
else:
    marcas_ops = [{"label": "Todas as Marcas", "value": "Todas"}] + [
        {"label": marca, "value": marca}
        for marca in sorted(df_global["Marca"].dropna().unique())
    ]
    valor_inicial_marca = "Todas"

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Dashboard de Inteligência de Vendas",
                        className="text-primary text-center my-4"
                    ),
                    width=12
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label("Selecione a Marca:", className="fw-bold"),
                                dcc.Dropdown(
                                    id="filtro-marca",
                                    options=marcas_ops,
                                    value=valor_inicial_marca,
                                    clearable=False
                                )
                            ]
                        ),
                        className="shadow-sm mb-4"
                    ),
                    width=12
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(criar_card_kpi("Total de Produtos", "kpi-produtos"), lg=3, md=6, sm=12),
                dbc.Col(criar_card_kpi("Preço Médio", "kpi-preco"), lg=3, md=6, sm=12),
                dbc.Col(criar_card_kpi("Total de Vendas", "kpi-vendas"), lg=3, md=6, sm=12),
                dbc.Col(criar_card_kpi("Nota Média", "kpi-nota"), lg=3, md=6, sm=12),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(criar_card_grafico("graf1", "Distribuição de Preços"), lg=6, md=12),
                dbc.Col(criar_card_grafico("graf2", "Preço vs Vendas"), lg=6, md=12),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(criar_card_grafico("graf3", "Distribuição de produtos por marca"), lg=12, md=12),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(criar_card_grafico("graf4", "Mix de Materiais"), lg=4, md=12),
                dbc.Col(criar_card_grafico("graf5", "Concentração de Notas dos Produtos"), lg=4, md=12),
                dbc.Col(criar_card_grafico("graf6", "Vendas vs Avaliações"), lg=4, md=12),
            ]
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#f8f9fa"}
)


@app.callback(
    [Output(f"graf{i}", "figure") for i in range(1, 7)] +
    [
        Output("kpi-produtos", "children"),
        Output("kpi-preco", "children"),
        Output("kpi-vendas", "children"),
        Output("kpi-nota", "children"),
    ],
    Input("filtro-marca", "value")
)
def update_dashboard(marca):
    # Atualiza gráficos e KPIs com base na marca selecionada.

    if df_global.empty or marca == "Sem dados":
        df_filtrado = pd.DataFrame()
    elif marca == "Todas":
        df_filtrado = df_global.copy()
    else:
        df_filtrado = df_global[df_global["Marca"] == marca].copy()

    figuras =  criar_graficos(df_filtrado)
    kpis = calcular_kpis(df_filtrado)

    return list(figuras) + [
        f"{kpis['total_produtos']}",
        f"R$ {kpis['media_preco']:.2f}",
        formatar_numero(kpis["total_vendas"]),
        f"{kpis['nota_media']:.2f}",
    ]


if __name__ == "__main__":
    app.run(debug=True, port=8050)
