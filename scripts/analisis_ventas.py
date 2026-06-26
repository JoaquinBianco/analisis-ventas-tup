


import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RUTA_DATOS = BASE_DIR / "datos" / "ventas.csv"
DIR_RESULTADOS = BASE_DIR / "resultados"


DIR_RESULTADOS.mkdir(exist_ok=True)

def pesos(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")



df = pd.read_csv(RUTA_DATOS, parse_dates=["fecha"])
df["importe"] = df["cantidad"] * df["precio_unitario"]



ventas_totales = df["importe"].sum()


unidades_por_producto = df.groupby("producto")["cantidad"].sum().sort_values(ascending=False)
producto_top_unidades = unidades_por_producto.idxmax()


importe_por_producto = df.groupby("producto")["importe"].sum().sort_values(ascending=False)
producto_top_importe = importe_por_producto.idxmax()


ventas_por_mes = df.groupby(df["fecha"].dt.to_period("M"))["importe"].sum()


etiquetas_mes = ventas_por_mes.index.astype(str)

plt.figure(figsize=(9, 5))
plt.plot(etiquetas_mes, ventas_por_mes.values, marker="o", linewidth=2, color="#1f6feb")
plt.title("Evolución mensual de las ventas — Pequeño comercio (2025)")
plt.xlabel("Mes")
plt.ylabel("Ventas ($)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()  # evita que los textos se corten al guardar
ruta_grafico_mes = DIR_RESULTADOS / "grafico_ventas_por_mes.png"
plt.savefig(ruta_grafico_mes, dpi=120)
plt.close()



fact_asc = importe_por_producto.sort_values()
plt.figure(figsize=(9, 5))
plt.barh(fact_asc.index, fact_asc.values, color="#2da44e")
plt.title("Facturación por producto — 2025")
plt.xlabel("Facturación ($)")
plt.ylabel("Producto")
plt.grid(True, axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
ruta_grafico_prod = DIR_RESULTADOS / "grafico_facturacion_por_producto.png"
plt.savefig(ruta_grafico_prod, dpi=120)
plt.close()


ruta_resumen = DIR_RESULTADOS / "resumen_indicadores.txt"
with open(ruta_resumen, "w", encoding="utf-8") as f:
    f.write("RESUMEN DE INDICADORES DE VENTAS\n")
    f.write("================================\n\n")
    f.write(f"Periodo analizado: {df['fecha'].min().date()} a {df['fecha'].max().date()}\n")
    f.write(f"Cantidad de operaciones: {len(df)}\n\n")
    f.write(f"Ventas totales: {pesos(ventas_totales)}\n")
    f.write(f"Producto mas vendido (unidades): {producto_top_unidades} "
            f"({unidades_por_producto.max()} unidades)\n")
    f.write(f"Producto que mas facturo: {producto_top_importe} "
            f"({pesos(importe_por_producto.max())})\n\n")
    f.write("Ventas por mes:\n")
    for mes, total in ventas_por_mes.items():
        f.write(f"  {mes}: {pesos(total)}\n")


ventas_por_mes.rename("ventas").to_csv(DIR_RESULTADOS / "ventas_por_mes.csv")
importe_por_producto.rename("facturacion").to_csv(DIR_RESULTADOS / "facturacion_por_producto.csv")



print("Analisis finalizado correctamente.")
print(f"- Ventas totales: {pesos(ventas_totales)}")
print(f"- Producto mas vendido (unidades): {producto_top_unidades} ({unidades_por_producto.max()} u.)")
print(f"- Producto que mas facturo: {producto_top_importe} ({pesos(importe_por_producto.max())})")
print(f"- Graficos guardados en: {ruta_grafico_mes.relative_to(BASE_DIR)} y "
      f"{ruta_grafico_prod.relative_to(BASE_DIR)}")
print(f"- Resumen guardado en: {ruta_resumen.relative_to(BASE_DIR)}")
