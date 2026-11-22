
import pandas as pd
from etl.pipeline import transform


def sample_data():
    return pd.DataFrame({
        "invoice_no": ["100001", "C100002", "100003"],
        "stock_code": ["A1", "A2", "A3"],
        "description": ["Produit A", "Produit B", "Produit C"],
        "quantity": [2, -1, 3],
        "invoice_date": [
            "2010-01-01",
            "2010-01-02",
            "2010-01-03",
        ],
        "unit_price": [10.0, 15.0, 0.0],
        "customer_id": ["1", "2", "3"],
        "country": ["France", "France", "Suisse"],
        "source_sheet": ["Test", "Test", "Test"],
    })


def test_ventes():
    result = transform(sample_data())
    assert result["is_sale"].tolist() == [
        True, False, False
    ]


def test_annulation():
    result = transform(sample_data())
    assert result["is_cancellation"].tolist() == [
        False, True, False
    ]


def test_revenue():
    result = transform(sample_data())
    assert result["revenue"].tolist() == [
        20.0, 0.0, 0.0
    ]


def test_nombre_lignes():
    result = transform(sample_data())
    assert len(result) == 3
