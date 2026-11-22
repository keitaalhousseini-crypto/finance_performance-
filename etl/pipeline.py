
from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

SOURCE = ROOT / "data" / "raw" / "online_retail_II.xlsx"

RENAME = {
    "Invoice": "invoice_no",
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "UnitPrice": "unit_price",
    "Customer ID": "customer_id",
    "CustomerID": "customer_id",
    "Country": "country",
}


def extract():
    if not SOURCE.is_file():
        raise FileNotFoundError(
            f"Fichier absent : {SOURCE}\n"
            "Vérifie le téléchargement avec : "
            "ls -lh data/raw"
        )

    workbook = pd.ExcelFile(SOURCE, engine="openpyxl")
    frames = []

    for sheet in workbook.sheet_names:
        print(f"Lecture de : {sheet}")
        frame = pd.read_excel(
            workbook,
            sheet_name=sheet,
            dtype={
                "Invoice": str,
                "InvoiceNo": str,
                "StockCode": str,
            },
        )
        frame = frame.rename(columns=RENAME)
        frame["source_sheet"] = sheet
        frames.append(frame)

    return pd.concat(frames, ignore_index=True)


def transform(df):
    df = df.copy()

    required = [
        "invoice_no",
        "stock_code",
        "quantity",
        "invoice_date",
        "unit_price",
        "country",
    ]

    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    for column in ["description", "customer_id"]:
        if column not in df.columns:
            df[column] = None

    df["invoice_no"] = (
        df["invoice_no"].astype("string").str.strip()
    )
    df["stock_code"] = (
        df["stock_code"].astype("string").str.strip()
    )
    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )

    for column in ["quantity", "unit_price"]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.replace(r"\.0$", "", regex=True)
    )

    df["country"] = (
        df["country"].astype("string").str.strip()
    )

    df = df.dropna(subset=required)

    # Retirer les doublons exacts entre les feuilles.
    # Les répétitions à l'intérieur d'une feuille
    # sont conservées faute d'identifiant de ligne unique.
    business_columns = [
        "invoice_no", "stock_code", "description",
        "quantity", "invoice_date", "unit_price",
        "customer_id", "country",
    ]

    sheet_order = list(df["source_sheet"].unique())
    if len(sheet_order) > 1:
        first = df[df["source_sheet"] == sheet_order[0]]
        others = df[df["source_sheet"] != sheet_order[0]]

        # Numéro d'occurrence pour conserver les
        # répétitions légitimes dans chaque feuille.
        first = first.copy()
        others = others.copy()

        first["_occ"] = first.groupby(
            business_columns, dropna=False
        ).cumcount()

        others["_occ"] = others.groupby(
            business_columns, dropna=False
        ).cumcount()

        keys = business_columns + ["_occ"]
        first_keys = pd.MultiIndex.from_frame(first[keys])
        other_keys = pd.MultiIndex.from_frame(others[keys])

        others = others.loc[~other_keys.isin(first_keys)]
        df = pd.concat([first, others], ignore_index=True)
        df = df.drop(columns="_occ")

    df["is_cancellation"] = (
        df["invoice_no"].str.upper().str.startswith("C")
        | df["quantity"].lt(0)
    ).fillna(False).astype(bool)

    df["is_sale"] = (
        ~df["is_cancellation"]
        & df["quantity"].gt(0)
        & df["unit_price"].gt(0)
    ).fillna(False).astype(bool)

    df["revenue"] = (
        df["quantity"] * df["unit_price"]
    ).where(df["is_sale"], 0.0)

    df["invoice_month"] = (
        df["invoice_date"].dt.strftime("%Y-%m")
    )

    df["customer_id"] = df["customer_id"].astype(object)
    df = df.astype(object).where(pd.notna(df), None)

    return df


def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="127.0.0.1",
        port=int(os.getenv("POSTGRES_PORT", "55432")),
        database=os.environ["POSTGRES_DB"],
    )
    return create_engine(url, pool_pre_ping=True)


def load(df):
    engine = get_engine()

    try:
        with engine.begin() as conn:
            conn.execute(text(
                "CREATE SCHEMA IF NOT EXISTS finance"
            ))

            conn.execute(text(
                "DROP TABLE IF EXISTS "
                "finance.transactions_staging"
            ))

        print("Chargement dans la table staging...")

        df.to_sql(
            "transactions_staging",
            con=engine,
            schema="finance",
            if_exists="replace",
            index=False,
            chunksize=2000,
        )

        # Échange transactionnel : en cas d'échec,
        # l'ancienne table reste disponible.
        with engine.begin() as conn:
            conn.execute(text(
                "DROP TABLE IF EXISTS "
                "finance.transactions_previous"
            ))
            conn.execute(text(
                "ALTER TABLE IF EXISTS "
                "finance.transactions "
                "RENAME TO transactions_previous"
            ))
            conn.execute(text(
                "ALTER TABLE finance.transactions_staging "
                "RENAME TO transactions"
            ))
            conn.execute(text(
                "CREATE INDEX IF NOT EXISTS "
                "idx_finance_invoice_date "
                "ON finance.transactions(invoice_date)"
            ))
            conn.execute(text(
                "DROP TABLE IF EXISTS "
                "finance.transactions_previous"
            ))

    finally:
        engine.dispose()


def main():
    print("1. EXTRACTION")
    raw = extract()
    print("Lignes sources :", len(raw))

    print("2. TRANSFORMATION")
    clean = transform(raw)
    print("Lignes après nettoyage :", len(clean))
    print("Ventes positives :", clean["is_sale"].sum())
    print("Annulations :", clean["is_cancellation"].sum())

    print("3. CHARGEMENT")
    load(clean)

    print("Pipeline ETL terminé.")


if __name__ == "__main__":
    main()
