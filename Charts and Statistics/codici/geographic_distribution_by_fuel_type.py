import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.lines import Line2D
from matplotlib.colors import to_rgb, rgb_to_hsv, hsv_to_rgb

CSV_PATH = "global_power_plant_database.csv"
OUT_PNG = "power_plants_all_fuels_legend_top.png"

POINT_SIZE = 2
POINT_ALPHA = 0.25
BORDER_LW = 0.35

LEGEND_MARKER_SIZE = 9
LEGEND_NCOL = 5

X_LIM = (-180, 180)
Y_LIM = (-60, 85)

FIGSIZE = (22, 10)

LEGEND_Y = 1.10

# Margini per non tagliare la y-label
LEFT_MARGIN = 0.12
BOTTOM_MARGIN = 0.08
TOP_MARGIN = 0.78

# Boost colori
SAT_MULT = 1.35
VAL_MULT = 1.10

FUEL_COLORS = {
    "Solar": "#FFD700",          # giallo acceso
    "Wind": "#00BFFF",           # azzurro intenso
    "Hydro": "#1F77B4",          # blu
    "Gas": "#FF7F0E",            # arancione
    "Coal": "#2F2F2F",           # quasi nero
    "Oil": "#8C564B",            # marrone
    "Nuclear": "#9467BD",        # viola
    "Biomass": "#2CA02C",        # verde
    "Waste": "#BCBD22",          # oliva/giallo-verde
    "Geothermal": "#D62728",     # rosso
    "Storage": "#17BECF",        # ciano/teal
    "Cogeneration": "#E377C2",   # fucsia
    "Petcoke": "#7F7F7F",        # grigio
    "Other": "#8A2BE2",          # blu-violet
    "Wave and Tidal": "#00CC66"  # verde acqua
}


def boost_color(color, sat_mult=1.35, val_mult=1.10):
    """(Opzionale) rende un colore più acceso in HSV."""
    r, g, b = to_rgb(color)
    hsv = rgb_to_hsv([r, g, b])
    hsv[1] = min(1.0, hsv[1] * sat_mult)
    hsv[2] = min(1.0, hsv[2] * val_mult)
    r2, g2, b2 = hsv_to_rgb(hsv)
    return (r2, g2, b2)


def load_powerplants(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude", "primary_fuel"])
    df = df[df["latitude"].between(-90, 90) & df["longitude"].between(-180, 180)]
    return df


def load_world_boundaries():
    try:
        import geodatasets
        candidates = [
            k for k in geodatasets.available
            if "naturalearth" in k.lower()
            and ("admin_0" in k.lower() or "country" in k.lower() or "countries" in k.lower())
        ]
        if candidates:
            return gpd.read_file(geodatasets.get_path(candidates[0]))
    except Exception:
        pass

    url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
    return gpd.read_file(url)


def pick_iso3_column(world: gpd.GeoDataFrame) -> str:
    for c in ["iso_a3", "ISO_A3", "ADM0_A3", "adm0_a3", "SOV_A3", "sov_a3"]:
        if c in world.columns:
            return c
    raise ValueError(f"Non trovo colonna ISO3. Colonne disponibili: {list(world.columns)}")


def main():
    df = load_powerplants(CSV_PATH)
    iso3_in_dataset = set(df["country"].dropna().unique())

    world = load_world_boundaries()
    iso_col = pick_iso3_column(world)
    world_sel = world[world[iso_col].isin(iso3_in_dataset)].copy()
    world_sel = world_sel[world_sel[iso_col].astype(str) != "-99"]

    # Fuel ordinati per frequenza (come prima)
    fuel_counts = df["primary_fuel"].value_counts()
    fuels = fuel_counts.index.tolist()

    # ========= COLORI: USO PALETTE MANUALE =========
    # Se per qualche motivo appare un fuel non previsto, assegno un colore di fallback
    fallback_cycle = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF0000", "#0000FF"]
    fuel_to_color = {}
    extra_i = 0
    for f in fuels:
        if f in FUEL_COLORS:
            fuel_to_color[f] = FUEL_COLORS[f]
        else:
            fuel_to_color[f] = fallback_cycle[extra_i % len(fallback_cycle)]
            extra_i += 1
    # =============================================

    fig, ax = plt.subplots(figsize=FIGSIZE)

    # margini manuali: evita che label e ticks vengano tagliati + riduce bianco ai lati
    fig.subplots_adjust(left=0.06, right=0.995, bottom=0.11, top=0.78)

    # punti
    for fuel in fuels:
        sub = df[df["primary_fuel"] == fuel]
        ax.scatter(
            sub["longitude"], sub["latitude"],
            s=POINT_SIZE,
            alpha=POINT_ALPHA,
            linewidths=0,
            color=fuel_to_color[fuel],
            zorder=1
        )

    # confini
    world_sel.boundary.plot(ax=ax, color="black", linewidth=BORDER_LW, zorder=2)

    # zoom
    ax.set_xlim(*X_LIM)
    ax.set_ylim(*Y_LIM)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude", labelpad=16)
    ax.set_title("Geographic Distribution of Power Plants by Type")

    # legenda
    legend_handles = [
        Line2D([0], [0],
               marker='o', linestyle='None',
               markerfacecolor=fuel_to_color[f],
               markeredgecolor='black',
               markeredgewidth=0.6,
               markersize=LEGEND_MARKER_SIZE,
               label=f)
        for f in fuels
    ]

    ax.legend(
        handles=legend_handles,
        title="PRIMARY FUEL",
        loc="lower center",
        bbox_to_anchor=(0.5, LEGEND_Y),
        ncol=LEGEND_NCOL,
        frameon=True,
        columnspacing=1.2,
        handletextpad=0.4
    )

    # Salvataggio
    plt.savefig(OUT_PNG, dpi=300)
    plt.show()
    print("Salvato:", OUT_PNG)


if __name__ == "__main__":
    main()
