
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)

PRODUCTOS = {
    "Cafe": 800,
    "Te": 600,
    "Medialuna": 450,
    "Sandwich": 2500,
    "Gaseosa": 1200,
    "Agua": 900,
    "Alfajor": 700,
    "Jugo": 1100,
}


PESOS = [30, 10, 28, 12, 18, 14, 22, 9]

INICIO = date(2025, 1, 1)
FIN = date(2025, 6, 30)


BASE_DIR = Path(__file__).resolve().parent.parent
DIR_DATOS = BASE_DIR / "datos"
DIR_DATOS.mkdir(exist_ok=True)
RUTA_SALIDA = DIR_DATOS / "ventas.csv"


def generar():
    
    filas = []
    id_venta = 1
    dia = INICIO
    while dia <= FIN:
        # Entre 2 y 6 operaciones por dia.
        for _ in range(random.randint(2, 6)):
            producto = random.choices(list(PRODUCTOS), weights=PESOS, k=1)[0]
            cantidad = random.randint(1, 5)
            precio = PRODUCTOS[producto]
            filas.append([id_venta, dia.isoformat(), producto, cantidad, precio])
            id_venta += 1
        dia += timedelta(days=1)
    return filas


def main():
    filas = generar()
    with open(RUTA_SALIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["id", "fecha", "producto", "cantidad", "precio_unitario"])
        escritor.writerows(filas)
    print(f"Dataset generado: {len(filas)} filas en {RUTA_SALIDA.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
