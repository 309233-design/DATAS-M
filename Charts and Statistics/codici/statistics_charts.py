import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

df = pd.read_csv("global_power_plant_database.csv", low_memory=False)

for c in ["capacity_mw", "latitude", "longitude"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# STATISTICHE PER PAESE & PER FUEL
by_country = (df.groupby("country_long", dropna=True)
                .agg(plants=("gppd_idnr","count"),
                     capacity_mw=("capacity_mw","sum"))
                .sort_values("capacity_mw", ascending=False))

by_fuel = (df.groupby("primary_fuel", dropna=True)
             .agg(plants=("gppd_idnr","count"),
                  capacity_mw=("capacity_mw","sum"),
                  capacity_mean_mw=("capacity_mw","mean"))
             .sort_values("capacity_mw", ascending=False))

# ====== TOTALE GLOBALE (per percentuale) ======
total_capacity = by_country["capacity_mw"].sum(skipna=True)
total_plants = by_country["plants"].sum()

# helper format percento sugli assi
percent_fmt = mtick.PercentFormatter(xmax=100, decimals=0)

# HORIZONTAL BAR TOP 20 PAESI PER CAPACITÀ (in % globale)
top = by_country.head(20).iloc[::-1]
top_pct = 100 * top["capacity_mw"] / total_capacity

plt.figure()
plt.barh(top.index, top_pct)
plt.xlabel("Total Capacity (%)")
plt.gca().xaxis.set_major_formatter(percent_fmt)
plt.ylabel("Country")
plt.title("Top 20 Countries by Total Installed Capacity")
plt.tight_layout()
plt.show()

# HORIZONTAL BAR TOP 20 PAESI PER IMPIANTI (in % globale)
top = by_country.sort_values("plants", ascending=False).head(20).iloc[::-1]
top_pct = 100 * top["plants"] / total_plants

plt.figure()
plt.barh(top.index, top_pct)
plt.xlabel("Number of Plants (%)")
plt.gca().xaxis.set_major_formatter(percent_fmt)
plt.ylabel("Country")
plt.title("Top 20 Countries by Number of Plants")
plt.tight_layout()
plt.show()

# IMPIANTI VS CAPACITÀ TOTALE (entrambi in % globale)
tmp = by_country.reset_index()
tmp["plants_pct"] = 100 * tmp["plants"] / total_plants
tmp["capacity_pct"] = 100 * tmp["capacity_mw"] / total_capacity

plt.figure()
plt.scatter(tmp["plants_pct"], tmp["capacity_pct"])
plt.xlabel("Number of Plants (%)")
plt.ylabel("Total Capacity (%)")
plt.gca().xaxis.set_major_formatter(percent_fmt)
plt.gca().yaxis.set_major_formatter(percent_fmt)
plt.title("Countries: Plants VS Total Capacity")
plt.tight_layout()
plt.show()

# BARH PER FUEL: CAPACITÀ TOTALE (in % globale)
top = by_fuel.head(15).iloc[::-1]
top_pct = 100 * top["capacity_mw"] / total_capacity

plt.figure()
plt.barh(top.index, top_pct)
plt.xlabel("Total Capacity (%)")
plt.gca().xaxis.set_major_formatter(percent_fmt)
plt.ylabel("Primary Fuel")
plt.title("Top Fuel Types by Total Installed Capacity")
plt.tight_layout()
plt.show()

# BARH PER FUEL: IMPIANTI (in % globale)
top = by_fuel.sort_values("plants", ascending=False).head(15).iloc[::-1]
top_pct = 100 * top["plants"] / total_plants

plt.figure()
plt.barh(top.index, top_pct)
plt.xlabel("Number of Plants (%)")
plt.gca().xaxis.set_major_formatter(percent_fmt)
plt.ylabel("Primary Fuel")
plt.title("Top Fuel Types by Number of Plants")
plt.tight_layout()
plt.show()

# DISTRIBUZIONE CAPACITY_MW PER FUEL
# (Qui ha più senso lasciarla in MW perché è una distribuzione di taglie.)
top_fuels = df["primary_fuel"].value_counts().head(10).index.tolist()
data = [df.loc[df["primary_fuel"]==f, "capacity_mw"].dropna().values for f in top_fuels]

plt.figure(figsize=(10,5))
plt.boxplot(data, labels=top_fuels, showfliers=False)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Capacity (MW)")
plt.title("Capacity Distribution by Fuel (Top 10 Fuels)")
plt.tight_layout()
plt.show()
