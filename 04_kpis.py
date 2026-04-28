import pandas as pd


def calcular_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total_produtos": 0,
            "media_preco": 0,
            "total_vendas": 0,
            "nota_media": 0,
        }

    total_produtos = len(df)
    media_preco = df["Preço"].mean() if "Preço" in df.columns else 0
    total_vendas = df["Qtd_Vendidos_Cod"].sum() if "Qtd_Vendidos_Cod" in df.columns else 0
    nota_media = df["Nota"].mean() if "Nota" in df.columns else 0

    return {
        "total_produtos": int(total_produtos),
        "media_preco": float(media_preco) if pd.notna(media_preco) else 0,
        "total_vendas": float(total_vendas) if pd.notna(total_vendas) else 0,
        "nota_media": float(nota_media) if pd.notna(nota_media) else 0,
    }

def formatar_numero(valor: float) -> str:
    if valor >= 1_000_000_000:
        return f"{valor/1_000_000_000:.1f}B"
    elif valor >= 1_000_000:
        return f"{valor/1_000_000:.1f}M"
    elif valor >= 1_000:
        return f"{valor/1_000:.1f}K"
    else:
        return f"{valor:.0f}"