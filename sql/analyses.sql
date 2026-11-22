
-- 1. Nombre total de lignes
SELECT COUNT(*) AS total_lignes
FROM finance.transactions;

-- 2. Chiffre d'affaires brut des ventes positives
SELECT ROUND(SUM(revenue)::numeric, 2) AS ca_brut
FROM finance.transactions
WHERE is_sale = TRUE;

-- 3. Nombre de commandes de vente
SELECT COUNT(DISTINCT invoice_no) AS commandes
FROM finance.transactions
WHERE is_sale = TRUE;

-- 4. Évolution mensuelle du chiffre d'affaires
SELECT
    invoice_month,
    ROUND(SUM(revenue)::numeric, 2) AS ca
FROM finance.transactions
WHERE is_sale = TRUE
GROUP BY invoice_month
ORDER BY invoice_month;

-- 5. Top 10 des pays
SELECT
    country,
    ROUND(SUM(revenue)::numeric, 2) AS ca
FROM finance.transactions
WHERE is_sale = TRUE
GROUP BY country
ORDER BY ca DESC
LIMIT 10;

-- 6. Top 10 des produits
SELECT
    stock_code,
    description,
    ROUND(SUM(revenue)::numeric, 2) AS ca
FROM finance.transactions
WHERE is_sale = TRUE
GROUP BY stock_code, description
ORDER BY ca DESC
LIMIT 10;

-- 7. Panier moyen par facture
WITH orders AS (
    SELECT
        invoice_no,
        SUM(revenue) AS order_total
    FROM finance.transactions
    WHERE is_sale = TRUE
    GROUP BY invoice_no
)
SELECT ROUND(AVG(order_total)::numeric, 2)
       AS panier_moyen
FROM orders;

-- 8. Factures d'annulation
SELECT COUNT(DISTINCT invoice_no) AS annulations
FROM finance.transactions
WHERE is_cancellation = TRUE;

-- 9. Nombre de clients identifiés
SELECT COUNT(DISTINCT customer_id) AS clients
FROM finance.transactions
WHERE is_sale = TRUE
AND customer_id IS NOT NULL;

-- 10. Contrôle qualité
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS clients_manquants,
    COUNT(*) FILTER (
        WHERE unit_price <= 0
    ) AS prix_non_positifs
FROM finance.transactions;
