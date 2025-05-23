#!/usr/bin/env python3
import pandas as pd
import argparse

def main():
    p = argparse.ArgumentParser(
        description="Extrae filas de severidad Medium de un informe HTML a CSV"
    )
    p.add_argument('--input',  required=True, help='Informe HTML generado')
    p.add_argument('--output', required=True, help='CSV de salida')
    args = p.parse_args()

    # Lee la primera tabla del HTML
    tables = pd.read_html(args.input)
    if not tables:
        print("No se encontró ninguna tabla en", args.input)
        return

    df = tables[0]
    if 'Severidad' not in df.columns:
        print("No existe la columna 'Severidad' en la tabla")
        return

    # Filtra sólo Medium
    df_medium = df[df['Severidad'] == 'Medium']
    df_medium.to_csv(args.output, index=False)
    print(f"Guardado {len(df_medium)} filas en {args.output}")

if __name__ == '__main__':
    main()
