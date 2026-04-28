import pandas as pd


def preparar_dados(caminho_arquivo: str) -> pd.DataFrame:

    try:
        df = pd.read_csv(caminho_arquivo)

        # Padronização de Material
        if "Material" in df.columns:
            df["Material"] = df["Material"].replace("jean", "jeans")

        # Padronização de Marca
        if "Marca" in df.columns:
            df["Marca"] = (
                df["Marca"]
                .astype(str)
                .str.strip()
                .str.lower()
                .str.title()
            )

        return df

    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()


def filtrar_outliers(df: pd.DataFrame, colunas: list[str], quantil: float = 0.99) -> pd.DataFrame:

    df_filtrado = df.copy()

    for coluna in colunas:
        if coluna in df_filtrado.columns and not df_filtrado[coluna].dropna().empty:
            limite = df_filtrado[coluna].quantile(quantil)
            df_filtrado = df_filtrado[df_filtrado[coluna] <= limite] # Remove valores extremos com base no quantil informado.

    return df_filtrado
