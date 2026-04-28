import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc
from data_loader import filtrar_outliers

MIN_DADOS_ESTATISTICOS = 3


def tem_dados_suficientes(df: pd.DataFrame, minimo: int = MIN_DADOS_ESTATISTICOS) -> bool:
    return len(df) >= minimo


def tem_variedade_suficiente(df: pd.DataFrame, colunas: list[str], minimo_valores_unicos: int = 2) -> bool:
    for coluna in colunas:
        if coluna not in df.columns:
            return False
        if df[coluna].dropna().nunique() < minimo_valores_unicos:
            return False
    return True

def criar_card_grafico(id_grafico: str, titulo: str):
    # Envolve cada gráfico em um card Bootstrap

    return dbc.Card(
        [
            dbc.CardHeader(html.H5(titulo, className="card-title mb-0 text-center")),
            dbc.CardBody(dcc.Graph(id=id_grafico, config={"displayModeBar": False})),
        ],
        className="shadow-sm mb-4"
    )


def criar_card_kpi(titulo: str, id_kpi: str):
    # Cria um card visual para os indicadores principais.

    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(titulo, className="text-muted text-center"),
                html.H3(id=id_kpi, className="text-center text-primary mb-0"),
            ]
        ),
        className="shadow-sm mb-4"
    )


def figura_vazia(titulo="Sem dados disponíveis", mensagem="Tente ajustar os filtros"):

    fig = px.scatter()

    fig.update_layout(
        template="plotly_white",
        title={
            "text": titulo,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18}
        },
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "⚠️",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.65,
                "showarrow": False,
                "font": {"size": 40}
            },
            {
                "text": "<b>Dados insuficientes</b>",
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.5,
                "showarrow": False,
                "font": {"size": 18}
            },
            {
                "text": mensagem,
                "xref": "paper",
                "yref": "paper",
                "x": 0.5,
                "y": 0.42,
                "showarrow": False,
                "font": {"size": 14, "color": "#7f8c8d"}
            }
        ],
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


def criar_graficos(df: pd.DataFrame):
    
    if df.empty:
        return [figura_vazia()] * 6

    layout_padrao = dict(
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        title_x=0.5
    )

    # 1. Distribuição de preços
    if "Preço" in df.columns:
        fig1 = px.histogram(
            df,
            x="Preço",
            nbins=30,
            color_discrete_sequence=["#3498db"],
        )
        fig1.update_layout(**layout_padrao, bargap=0.1)
        fig1.update_xaxes(title="Preço")
        fig1.update_yaxes(title="Frequência")
    else:
        fig1 = figura_vazia("Distribuição de Preços")


    # 2. Preço vs vendas
    if (
            {"Preço", "Qtd_Vendidos_Cod"}.issubset(df.columns)
            and tem_dados_suficientes(df)
            and tem_variedade_suficiente(df, ["Preço", "Qtd_Vendidos_Cod"])
    ):
        df_p = filtrar_outliers(df, ["Preço", "Qtd_Vendidos_Cod"])
        # exige dados suficientes e variabilidade

        if len(df_p) >= 3:
            fig2 = px.scatter(
                df_p,
                x="Preço",
                y="Qtd_Vendidos_Cod",
                opacity=0.6,
                render_mode="svg",
                hover_data=[col for col in ["Marca", "Material"] if col in df_p.columns]
            )
            fig2.update_layout(**layout_padrao)
            fig2.update_xaxes(title="Preço")
            fig2.update_yaxes(title="Quantidade Vendida")
        else:
            fig2 = figura_vazia(
                "Preço vs Vendas",
                "Poucos dados após o filtro de outliers"
            )
    else:
        fig2 = figura_vazia(
            "Dados insuficientes para análise de dispersão"
        )


    # 3. Distribuição de produtos por marca
    if "Marca" in df.columns and df["Marca"].dropna().nunique() >= 2: # Exige mais de uma marca

        top_marcas = (
            df["Marca"]
            .dropna()
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_marcas.columns = ["Marca", "Quantidade"]

        fig3 = px.bar(
            top_marcas,
            x="Marca",
            y="Quantidade",
            color="Quantidade",
            color_continuous_scale="Viridis",
        )

        fig3.update_layout(**layout_padrao, showlegend=False)
        fig3.update_xaxes(title="Marca")
        fig3.update_yaxes(title="Quantidade")

    else:
        fig3 = figura_vazia(
            "É necessário haver mais de uma marca para exibir o ranking"
        )

    # 4. Mix de materiais
    if "Material" in df.columns:
        top5_mat = df["Material"].value_counts().head(5) # Mostra apenas os 5 materiais principais
        fig4 = px.pie(
            names=top5_mat.index,
            values=top5_mat.values,
            hole=0.4,
        )
        fig4.update_layout(**layout_padrao)
    else:
        fig4 = figura_vazia("Mix de Materiais")

    # 5. Densidade de notas
    fig5 = figura_vazia()

    if "Nota" in df.columns:
        notas = df["Nota"].dropna()

        if len(notas) > 1:
            import plotly.figure_factory as ff
            import numpy as np

            fig5 = ff.create_distplot(
                [notas],
                group_labels=["Notas"],
                colors=["#e67e22"],
                show_hist=True,
                bin_size=0.12
            )

            media = np.mean(notas)

            fig5.add_vline(
                x=media,
                line_dash="dash",
                line_color="#e74c3c",
                annotation_text=f"Média: {media:.2f}",
                annotation_position="top"
            )

            fig5.update_layout(
                **layout_padrao,
                xaxis_title="Nota",
                yaxis_title="Densidade"
            )

            fig5.update_traces(opacity=0.45)

        else:
            fig5 = figura_vazia("Dados insuficientes para densidade")

    # 6. Vendas vs avaliações
    if {"Qtd_Vendidos_Cod", "N_Avaliações"}.issubset(df.columns):
        df_reg = filtrar_outliers(df, ["Qtd_Vendidos_Cod", "N_Avaliações"])
        fig6 = px.scatter(
            df_reg,
            x="Qtd_Vendidos_Cod",
            y="N_Avaliações",
            trendline="ols",
            hover_data=[col for col in ["Marca", "Material"] if col in df_reg.columns]
        )
        fig6.update_layout(**layout_padrao)
        fig6.update_xaxes(title="Quantidade Vendida")
        fig6.update_yaxes(title="Número de Avaliações")
    else:
        fig6 = figura_vazia("Vendas vs Avaliações")

    return fig1, fig2, fig3, fig4, fig5, fig6
