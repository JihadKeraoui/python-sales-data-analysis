import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("raw_sales_data.csv")

print(df.head())
print(df.shape)
print(df.info())

print(df.describe())
print(df.isnull().sum())
print("Doublons :", df.duplicated().sum())

# ============================================================
# 2. DATA CLEANING - NETTOYAGE DES DONNÉES
# ============================================================

# ------------------------------------------------------------
# 1. SUPPRESSION DES DOUBLONS
# ------------------------------------------------------------

# Vérifier le nombre de doublons avant suppression
print("Nombre de doublons avant nettoyage :", df.duplicated().sum())

# Supprimer les lignes dupliquées
df = df.drop_duplicates()

# Vérifier le résultat
print("Nombre de doublons après nettoyage :", df.duplicated().sum())
print("Nombre de lignes après suppression :", len(df))


# ------------------------------------------------------------
# 2. STANDARDISATION DE LA COLONNE CATEGORY
# ------------------------------------------------------------

# Certaines catégories peuvent être écrites différemment :
# "electronics", "Electronics", "ACCESSORIES", etc.

# Supprimer les espaces inutiles et mettre la première lettre
# de chaque mot en majuscule
df["Category"] = df["Category"].str.strip().str.title()

# Vérifier les catégories après standardisation
print("\nCatégories après standardisation :")
print(df["Category"].value_counts())


# ------------------------------------------------------------
# 3. TRAITEMENT DES CUSTOMER_ID MANQUANTS
# ------------------------------------------------------------

# Afficher le nombre de Customer_ID manquants
print("\nCustomer_ID manquants avant traitement :",
      df["Customer_ID"].isnull().sum())

# Nous ne créons pas de faux identifiant client.
# Pour ce projet, nous conservons les valeurs manquantes.
# Cela permet de ne pas inventer de données.


# ------------------------------------------------------------
# 4. TRAITEMENT DES PAYMENT_METHOD MANQUANTS
# ------------------------------------------------------------

# Remplacer les valeurs manquantes par "Unknown"
df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

# Vérifier le résultat
print("\nMéthodes de paiement :")
print(df["Payment_Method"].value_counts())


# ------------------------------------------------------------
# 5. TRAITEMENT DES UNIT_PRICE MANQUANTS
# ------------------------------------------------------------

# Afficher le nombre de prix manquants
print("\nUnit_Price manquants avant traitement :",
      df["Unit_Price"].isnull().sum())

# Pour remplacer un prix manquant, on utilise la médiane
# du prix correspondant au même produit.
#
# Exemple :
# Si plusieurs "Laptop" coûtent 800, 900, 1000
# et qu'un prix est manquant, on utilise la médiane
# des prix des autres Laptop.

df["Unit_Price"] = df.groupby("Product")["Unit_Price"].transform(
    lambda x: x.fillna(x.median())
)

# Vérifier le résultat
print("Unit_Price manquants après traitement :",
      df["Unit_Price"].isnull().sum())


# ------------------------------------------------------------
# 6. RECALCUL DU REVENUE
# ------------------------------------------------------------

# Le chiffre d'affaires doit être :
#
# Revenue = Quantity × Unit_Price

df["Revenue"] = df["Quantity"] * df["Unit_Price"]

# Arrondir le résultat à 2 chiffres après la virgule
df["Revenue"] = df["Revenue"].round(2)


# ------------------------------------------------------------
# 7. VÉRIFICATION FINALE DU DATASET
# ------------------------------------------------------------

print("\n========================================")
print("     DATASET APRÈS NETTOYAGE")
print("========================================")

# Nombre de lignes et de colonnes
print("\nDimensions :", df.shape)

# Vérifier les valeurs manquantes
print("\nValeurs manquantes :")
print(df.isnull().sum())

# Vérifier les doublons
print("\nNombre de doublons :", df.duplicated().sum())

# Vérifier les catégories
print("\nCatégories :")
print(df["Category"].value_counts())

# Afficher les premières lignes du dataset nettoyé
print("\nAperçu du dataset nettoyé :")
print(df.head())


# ------------------------------------------------------------
# 8. SAUVEGARDE DU DATASET NETTOYÉ
# ------------------------------------------------------------

# Sauvegarder le résultat dans un nouveau fichier CSV.
# On conserve le fichier original "raw_sales_data.csv"
# pour pouvoir montrer la différence avant/après nettoyage.

df.to_csv("clean_sales_data.csv", index=False)

print("\nDataset nettoyé sauvegardé dans : clean_sales_data.csv")

# ============================================================
# 3. DATA ANALYSIS - ANALYSE DES DONNÉES
# ============================================================


# ------------------------------------------------------------
# 1. STATISTIQUES DESCRIPTIVES
# ------------------------------------------------------------

print("\n========================================")
print("       STATISTIQUES DESCRIPTIVES")
print("========================================")

# Statistiques générales des colonnes numériques
print(df.describe())


# ------------------------------------------------------------
# 2. CHIFFRE D'AFFAIRES TOTAL
# ------------------------------------------------------------

total_revenue = df["Revenue"].sum()

print("\nChiffre d'affaires total :",
      round(total_revenue, 2), "$")


# ------------------------------------------------------------
# 3. QUANTITÉ TOTALE VENDUE
# ------------------------------------------------------------

total_quantity = df["Quantity"].sum()

print("Quantité totale vendue :",
      total_quantity)


# ------------------------------------------------------------
# 4. NOMBRE DE COMMANDES
# ------------------------------------------------------------

number_orders = df["Order_ID"].nunique()

print("Nombre de commandes :",
      number_orders)


# ------------------------------------------------------------
# 5. PANIER MOYEN
# ------------------------------------------------------------

average_order = df["Revenue"].mean()

print("Valeur moyenne d'une commande :",
      round(average_order, 2), "$")


# ------------------------------------------------------------
# 6. CHIFFRE D'AFFAIRES PAR PRODUIT
# ------------------------------------------------------------

revenue_by_product = (
    df.groupby("Product")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n========================================")
print("     CHIFFRE D'AFFAIRES PAR PRODUIT")
print("========================================")

print(revenue_by_product)


# ------------------------------------------------------------
# 7. QUANTITÉ VENDUE PAR PRODUIT
# ------------------------------------------------------------

quantity_by_product = (
    df.groupby("Product")["Quantity"]
      .sum()
      .sort_values(ascending=False)
)

print("\n========================================")
print("       QUANTITÉ PAR PRODUIT")
print("========================================")

print(quantity_by_product)


# ------------------------------------------------------------
# 8. CHIFFRE D'AFFAIRES PAR CATÉGORIE
# ------------------------------------------------------------

revenue_by_category = (
    df.groupby("Category")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n========================================")
print("     CHIFFRE D'AFFAIRES PAR CATÉGORIE")
print("========================================")

print(revenue_by_category)


# ------------------------------------------------------------
# 9. CHIFFRE D'AFFAIRES PAR RÉGION
# ------------------------------------------------------------

revenue_by_region = (
    df.groupby("Region")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\n========================================")
print("       CHIFFRE D'AFFAIRES PAR RÉGION")
print("========================================")

print(revenue_by_region)


# ------------------------------------------------------------
# 10. NOMBRE DE COMMANDES PAR RÉGION
# ------------------------------------------------------------

orders_by_region = (
    df.groupby("Region")["Order_ID"]
      .nunique()
      .sort_values(ascending=False)
)

print("\n========================================")
print("       COMMANDES PAR RÉGION")
print("========================================")

print(orders_by_region)


# ------------------------------------------------------------
# 11. MÉTHODES DE PAIEMENT
# ------------------------------------------------------------

payment_distribution = df["Payment_Method"].value_counts()

print("\n========================================")
print("       MÉTHODES DE PAIEMENT")
print("========================================")

print(payment_distribution)


# ------------------------------------------------------------
# 12. PRODUIT LE PLUS RENTABLE
# ------------------------------------------------------------

best_product = revenue_by_product.idxmax()
best_product_revenue = revenue_by_product.max()

print("\nProduit avec le chiffre d'affaires le plus élevé :")
print(best_product)
print("Revenue :", round(best_product_revenue, 2), "$")


# ------------------------------------------------------------
# 13. MEILLEURE RÉGION
# ------------------------------------------------------------

best_region = revenue_by_region.idxmax()
best_region_revenue = revenue_by_region.max()

print("\nRégion avec le chiffre d'affaires le plus élevé :")
print(best_region)
print("Revenue :", round(best_region_revenue, 2), "$")


# ------------------------------------------------------------
# 14. MEILLEURE CATÉGORIE
# ------------------------------------------------------------

best_category = revenue_by_category.idxmax()
best_category_revenue = revenue_by_category.max()

print("\nCatégorie avec le chiffre d'affaires le plus élevé :")
print(best_category)
print("Revenue :", round(best_category_revenue, 2), "$")


# ------------------------------------------------------------
# 15. RÉSUMÉ DU PROJET
# ------------------------------------------------------------

print("\n========================================")
print("           RÉSUMÉ DE L'ANALYSE")
print("========================================")

print("Nombre de commandes :", number_orders)
print("Quantité vendue :", total_quantity)
print("Chiffre d'affaires :", round(total_revenue, 2), "$")
print("Panier moyen :", round(average_order, 2), "$")
print("Meilleur produit :", best_product)
print("Meilleure catégorie :", best_category)
print("Meilleure région :", best_region)
# ============================================================
# 4. DATA VISUALIZATION - VISUALISATION PROFESSIONNELLE
# ============================================================

import matplotlib.pyplot as plt
import pandas as pd


# ------------------------------------------------------------
# FONCTION POUR FORMATER LES MONTANTS
# ------------------------------------------------------------

def format_currency(value):
    """
    Transforme un montant en format lisible :
    170797 -> $170.8K
    250344 -> $250.3K
    1500   -> $1.5K
    """
    
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    
    else:
        return f"${value:.0f}"


# ------------------------------------------------------------
# PRÉPARATION DE LA DATE
# ------------------------------------------------------------

df["Order_Date"] = pd.to_datetime(df["Order_Date"])


# ============================================================
# GRAPHIQUE 1 : REVENUE PAR PRODUIT
# ============================================================

revenue_by_product = (
    df.groupby("Product")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(11, 7))

bars = plt.bar(
    revenue_by_product.index,
    revenue_by_product.values
)

# Identifier le meilleur produit
best_product_index = revenue_by_product.values.argmax()

# Mettre en évidence le meilleur résultat
bars[best_product_index].set_alpha(0.75)

# Ajouter les valeurs au-dessus des barres
for i, value in enumerate(revenue_by_product.values):

    plt.text(
        i,
        value + revenue_by_product.max() * 0.02,
        format_currency(value),
        ha="center",
        fontweight="bold"
    )

plt.title(
    "Revenue by Product",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Product")
plt.ylabel("Revenue ($)")

plt.xticks(rotation=35, ha="right")

plt.grid(axis="y", alpha=0.25)

plt.tight_layout()

plt.savefig(
    "revenue_by_product.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# GRAPHIQUE 2 : REVENUE PAR CATÉGORIE
# ============================================================

revenue_by_category = (
    df.groupby("Category")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(9, 7))

bars = plt.bar(
    revenue_by_category.index,
    revenue_by_category.values
)

# Identifier la meilleure catégorie
best_category_index = revenue_by_category.values.argmax()

# Mise en évidence
bars[best_category_index].set_alpha(0.75)

# Ajouter les valeurs
for i, value in enumerate(revenue_by_category.values):

    plt.text(
        i,
        value + revenue_by_category.max() * 0.02,
        format_currency(value),
        ha="center",
        fontweight="bold"
    )

plt.title(
    "Revenue by Category",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Category")
plt.ylabel("Revenue ($)")

plt.grid(axis="y", alpha=0.25)

plt.tight_layout()

plt.savefig(
    "revenue_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# GRAPHIQUE 3 : REVENUE PAR RÉGION
# ============================================================

revenue_by_region = (
    df.groupby("Region")["Revenue"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(9, 7))

bars = plt.bar(
    revenue_by_region.index,
    revenue_by_region.values
)

# Identifier la meilleure région
best_region_index = revenue_by_region.values.argmax()

# Mise en évidence
bars[best_region_index].set_alpha(0.75)

# Ajouter les valeurs
for i, value in enumerate(revenue_by_region.values):

    plt.text(
        i,
        value + revenue_by_region.max() * 0.02,
        format_currency(value),
        ha="center",
        fontweight="bold"
    )

plt.title(
    "Revenue by Region",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Region")
plt.ylabel("Revenue ($)")

plt.grid(axis="y", alpha=0.25)

plt.tight_layout()

plt.savefig(
    "revenue_by_region.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# GRAPHIQUE 4 : ÉVOLUTION MENSUELLE DU REVENUE
# ============================================================

monthly_revenue = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"]
      .sum()
)

# Convertir les périodes en texte
monthly_revenue.index = monthly_revenue.index.astype(str)

plt.figure(figsize=(12, 7))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o",
    linewidth=2
)

# Identifier le meilleur mois
best_month_index = monthly_revenue.values.argmax()

best_month = monthly_revenue.index[best_month_index]
best_month_value = monthly_revenue.values[best_month_index]

# Mettre en évidence le meilleur mois
plt.scatter(
    best_month,
    best_month_value,
    s=120,
    zorder=5
)

# Ajouter les valeurs sur chaque point
for i, value in enumerate(monthly_revenue.values):

    plt.text(
        i,
        value + monthly_revenue.max() * 0.025,
        format_currency(value),
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

plt.title(
    "Monthly Revenue Trend",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Revenue ($)")

plt.xticks(rotation=45)

plt.grid(alpha=0.25)

plt.tight_layout()

plt.savefig(
    "monthly_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# RÉSUMÉ DES MEILLEURS RÉSULTATS
# ============================================================

print("\n========================================")
print("       MEILLEURS RÉSULTATS")
print("========================================")

print(
    f"Meilleur produit : {revenue_by_product.idxmax()} "
    f"({format_currency(revenue_by_product.max())})"
)

print(
    f"Meilleure catégorie : {revenue_by_category.idxmax()} "
    f"({format_currency(revenue_by_category.max())})"
)

print(
    f"Meilleure région : {revenue_by_region.idxmax()} "
    f"({format_currency(revenue_by_region.max())})"
)

print(
    f"Meilleur mois : {best_month} "
    f"({format_currency(best_month_value)})"
)

print("\n✓ Les 4 graphiques ont été sauvegardés.")

# ============================================================
# 5. DASHBOARD KPI
# ============================================================

import matplotlib.pyplot as plt


# ------------------------------------------------------------
# CALCUL DES KPI
# ------------------------------------------------------------

total_orders = df["Order_ID"].nunique()
total_revenue = df["Revenue"].sum()
total_quantity = df["Quantity"].sum()
average_order = df["Revenue"].mean()

best_product = revenue_by_product.idxmax()
best_product_revenue = revenue_by_product.max()

best_category = revenue_by_category.idxmax()
best_category_revenue = revenue_by_category.max()

best_region = revenue_by_region.idxmax()
best_region_revenue = revenue_by_region.max()

best_month = monthly_revenue.idxmax()
best_month_revenue = monthly_revenue.max()


# ------------------------------------------------------------
# CRÉATION DU DASHBOARD
# ------------------------------------------------------------

fig = plt.figure(figsize=(14, 9))

fig.suptitle(
    "SALES DATA ANALYSIS DASHBOARD",
    fontsize=22,
    fontweight="bold"
)


# ------------------------------------------------------------
# KPI 1 - COMMANDES
# ------------------------------------------------------------

fig.text(
    0.15, 0.78,
    "TOTAL ORDERS",
    ha="center",
    fontsize=12
)

fig.text(
    0.15, 0.71,
    f"{total_orders:,}",
    ha="center",
    fontsize=24,
    fontweight="bold"
)


# ------------------------------------------------------------
# KPI 2 - REVENUE
# ------------------------------------------------------------

fig.text(
    0.38, 0.78,
    "TOTAL REVENUE",
    ha="center",
    fontsize=12
)

fig.text(
    0.38, 0.71,
    format_currency(total_revenue),
    ha="center",
    fontsize=24,
    fontweight="bold"
)


# ------------------------------------------------------------
# KPI 3 - QUANTITÉ VENDUE
# ------------------------------------------------------------

fig.text(
    0.62, 0.78,
    "UNITS SOLD",
    ha="center",
    fontsize=12
)

fig.text(
    0.62, 0.71,
    f"{total_quantity:,}",
    ha="center",
    fontsize=24,
    fontweight="bold"
)


# ------------------------------------------------------------
# KPI 4 - PANIER MOYEN
# ------------------------------------------------------------

fig.text(
    0.85, 0.78,
    "AVERAGE ORDER",
    ha="center",
    fontsize=12
)

fig.text(
    0.85, 0.71,
    format_currency(average_order),
    ha="center",
    fontsize=24,
    fontweight="bold"
)


# ------------------------------------------------------------
# SECTION DES MEILLEURS RÉSULTATS
# ------------------------------------------------------------

fig.text(
    0.5, 0.60,
    "TOP PERFORMERS",
    ha="center",
    fontsize=16,
    fontweight="bold"
)


# Meilleur produit
fig.text(
    0.25, 0.51,
    "TOP PRODUCT",
    ha="center",
    fontsize=11
)

fig.text(
    0.25, 0.45,
    best_product,
    ha="center",
    fontsize=18,
    fontweight="bold"
)

fig.text(
    0.25, 0.40,
    format_currency(best_product_revenue),
    ha="center",
    fontsize=13
)


# Meilleure catégorie
fig.text(
    0.50, 0.51,
    "TOP CATEGORY",
    ha="center",
    fontsize=11
)

fig.text(
    0.50, 0.45,
    best_category,
    ha="center",
    fontsize=18,
    fontweight="bold"
)

fig.text(
    0.50, 0.40,
    format_currency(best_category_revenue),
    ha="center",
    fontsize=13
)


# Meilleure région
fig.text(
    0.75, 0.51,
    "TOP REGION",
    ha="center",
    fontsize=11
)

fig.text(
    0.75, 0.45,
    best_region,
    ha="center",
    fontsize=18,
    fontweight="bold"
)

fig.text(
    0.75, 0.40,
    format_currency(best_region_revenue),
    ha="center",
    fontsize=13
)


# ------------------------------------------------------------
# MEILLEUR MOIS
# ------------------------------------------------------------

fig.text(
    0.5, 0.29,
    "BEST SALES MONTH",
    ha="center",
    fontsize=11
)

fig.text(
    0.5, 0.23,
    best_month,
    ha="center",
    fontsize=20,
    fontweight="bold"
)

fig.text(
    0.5, 0.18,
    format_currency(best_month_revenue),
    ha="center",
    fontsize=14
)


# ------------------------------------------------------------
# SAUVEGARDE
# ------------------------------------------------------------

plt.axis("off")

plt.savefig(
    "sales_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ------------------------------------------------------------
# CONFIRMATION
# ------------------------------------------------------------

print("\n========================================")
print("       DASHBOARD CRÉÉ")
print("========================================")

print("✓ sales_dashboard.png")