import csv
import random
from datetime import datetime, timedelta

categories = ["Électronique", "Vêtements", "Alimentation", "Maison", "Sport", "Beauté", "Livres", "Jouets"]
pays = ["France", "Maroc", "USA", "Allemagne", "Canada", "Espagne", "Italie", "Japon", "Brésil", "UK"]
produits = {
    "Électronique": ["Laptop", "Smartphone", "Tablette", "Casque", "Montre connectée"],
    "Vêtements": ["T-shirt", "Jean", "Veste", "Robe", "Chaussures"],
    "Alimentation": ["Café", "Chocolat", "Huile olive", "Pâtes", "Riz"],
    "Maison": ["Lampe", "Coussin", "Tapis", "Cadre", "Vase"],
    "Sport": ["Ballon", "Raquette", "Haltère", "Tapis yoga", "Corde"],
    "Beauté": ["Parfum", "Crème", "Shampoing", "Rouge lèvres", "Sérum"],
    "Livres": ["Roman", "BD", "Manuel", "Dictionnaire", "Biographie"],
    "Jouets": ["Puzzle", "Lego", "Poupée", "Voiture RC", "Peluche"]
}
modes_paiement = ["Carte", "PayPal", "Virement", "Cash"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

with open("data/sales.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id", "date", "category", "product",
        "quantity", "unit_price", "total",
        "country", "payment_method", "customer_id"
    ])

    for i in range(1, 100001):  # 100 000 lignes
        cat = random.choice(categories)
        product = random.choice(produits[cat])
        qty = random.randint(1, 10)
        price = round(random.uniform(5, 500), 2)
        total = round(qty * price, 2)
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        country = random.choice(pays)
        payment = random.choice(modes_paiement)
        customer_id = f"CUST{random.randint(1, 5000):05d}"

        writer.writerow([
            f"ORD{i:06d}",
            date.strftime("%Y-%m-%d"),
            cat, product, qty, price, total,
            country, payment, customer_id
        ])

print("100 000 lignes générées dans data/sales.csv")