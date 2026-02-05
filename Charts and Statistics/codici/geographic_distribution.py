import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

CSV_PATH = "global_power_plant_database.csv"
OUT_PNG = "power_plants_world_zoom.png"

POINT_SIZE = 1
POINT_ALPHA = 0.25
BORDER_LW = 0.35

# Zoom: taglio del sud (Antartide) per "ingrandire" la mappa
X_LIM = (-180, 180)
Y_LIM = (-60, 85)   # <-- modifica qui se vuoi più/meno taglio

FIGSIZE = (16, 8)


def load_powerplants(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, low_memory=False)
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude"])
    df = df[df["latitude"].between(-90, 90) & df["longitude"].between(-180, 180)]
    return df


def load_world_boundaries():
    """
    Carica confini paesi:
    - prova a usare geodatasets se disponibile
    - altrimenti usa fallback URL Natural Earth GeoJSON (110m)
    """
    # 1) prova geodatasets
    try:
        import geodatasets
        candidates = [
            k for k in geodatasets.available
            if "naturalearth" in k.lower() and ("admin_0" in k.lower() or "country" in k.lower() or "countries" in k.lower())
        ]
        if candidates:
            key = candidates[0]
            path = geodatasets.get_path(key)
            world = gpd.read_file(path)
            return world, f"geodatasets:{key}"
    except Exception:
        pass

    # 2) fallback URL (leggero e sufficiente)
    url = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson"
    world = gpd.read_file(url)
    return world, "fallback:naturalearth 110m geojson"


def pick_iso3_column(world: gpd.GeoDataFrame) -> str:
    candidates = ["iso_a3", "ISO_A3", "ADM0_A3", "adm0_a3", "SOV_A3", "sov_a3"]
    for c in candidates:
        if c in world.columns:
            return c
    raise ValueError(
        f"Non trovo una colonna ISO3 tra {candidates}. Colonne disponibili: {list(world.columns)}"
    )


def main():
    # 1) Dati centrali
    df = load_powerplants(CSV_PATH)
    print("Numero punti con coordinate valide:", len(df))

    iso3_in_dataset = set(df["country"].dropna().unique())
    print("Numero paesi (ISO3) nel dataset:", len(iso3_in_dataset))

    # 2) Confini
    world, source = load_world_boundaries()
    print("Confini caricati da:", source)

    iso_col = pick_iso3_column(world)
    print("Colonna ISO3 usata nei confini:", iso_col)

    # 3) Filtro confini ai soli paesi presenti nel dataset
    world_sel = world[world[iso_col].isin(iso3_in_dataset)].copy()
    world_sel = world_sel[world_sel[iso_col].astype(str) != "-99"]  # pulizia comune
    print("Numero poligoni selezionati:", len(world_sel))

    # 4) Plot
    fig, ax = plt.subplots(figsize=FIGSIZE)

    # Punti centrali (sotto)
    ax.scatter(
        df["longitude"], df["latitude"],
        s=POINT_SIZE, c="red", alpha=POINT_ALPHA,
        linewidths=0, zorder=1
    )

    # Confini (sopra)
    world_sel.boundary.plot(
        ax=ax, color="black", linewidth=0.2, zorder=2
    )

    # Zoom "più grande": taglia sud
    ax.set_xlim(*X_LIM)
    ax.set_ylim(*Y_LIM)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Geographic Distribution of Power Plants")

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=250)
    plt.show()



if __name__ == "__main__":
    main()
