
import pandas as pd
import plotly.express as px
import os

# Veri setini yükle
try:
    df = pd.read_csv("Datasets/owid-co2-data.csv")
except FileNotFoundError:
    df = pd.read_csv("Nature-Pollution/Datasets/owid-co2-data.csv")

# df_eda hazırla - eksik değerleri doldur
df_eda = df.sort_values(["country", "year"])
cols_to_interpolate = ["co2", "co2_per_capita", "gdp", "population", "energy_per_capita"]
cols_to_interpolate = [c for c in cols_to_interpolate if c in df_eda.columns]

def fill_group(group):
    group[cols_to_interpolate] = group[cols_to_interpolate].interpolate(
        method="linear", limit_direction="both"
    )
    return group

df_eda = df_eda.groupby("country", group_keys=False).apply(fill_group)

def make_3d_globe_from_df_eda(
    df_eda: pd.DataFrame,
    metric: str = "co2_per_capita",
    year_min: int = 1990,
    year_max: int = 2024,
    output_html: str = "img/co2_globe_df_eda.html",
):
    """
    3D globe visualization STRICTLY based on df_eda output.
    - No fabricated years
    - No fabricated countries
    - Only real OWID country ISO codes
    """

    required = {"iso_code", "country", "year", metric}
    missing = required - set(df_eda.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df_map = df_eda.copy()

    # 1) Only real countries (ISO-3)
    df_map = df_map[df_map["iso_code"].notna()]
    df_map = df_map[df_map["iso_code"].astype(str).str.len() == 3]

    # 2) Year window (NO creation of missing years)
    df_map = df_map[df_map["year"].between(year_min, year_max)]

    # 3) Only rows where metric truly exists
    df_map = df_map.dropna(subset=[metric])

    print("3D Globe Coverage Check:")
    print("Years:", df_map["year"].min(), "-", df_map["year"].max())
    print("Countries:", df_map["country"].nunique())

    fig = px.choropleth(
        df_map,
        locations="iso_code",
        color=metric,
        hover_name="country",
        animation_frame="year",
        color_continuous_scale="Viridis",
        title=(
            f"{metric} by Country (df_eda based)<br>"
            "<sup>Countries shown only where data exists</sup>"
        ),
    )

    fig.update_geos(
        projection_type="orthographic",
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="rgb(230,230,230)",
        showocean=True,
        oceancolor="rgb(200,220,255)",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=70, b=0),
    )

    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    fig.write_html(output_html)
    fig.show()

    print(f"✅ 3D globe saved to: {output_html}")


make_3d_globe_from_df_eda(
    df_eda=df_eda,
    metric="co2_per_capita",
    year_min=1990,
    year_max=2024,
    output_html="img/co2_per_capita_globe_df_eda.html",
)




