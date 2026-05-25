import csv
import os

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DB_DIR, exist_ok=True)

PROD_FILE = os.path.join(DB_DIR, "products.csv")
CAT_FILE = os.path.join(DB_DIR, "categories.csv")

def init_db():
    if not os.path.exists(PROD_FILE):
        with open(PROD_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Category", "Size", "Price", "SalePrice", "Stock", "SoldCount", "ImagePath"])
    if not os.path.exists(CAT_FILE):
        with open(CAT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name"])

init_db()

def load_products():
    products = []
    if os.path.exists(PROD_FILE):
        with open(PROD_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                products.append(row)
    return products

def save_products(products):
    with open(PROD_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Name", "Category", "Size", "Price", "SalePrice", "Stock", "SoldCount", "ImagePath"])
        writer.writeheader()
        writer.writerows(products)

def load_categories():
    categories = []
    if os.path.exists(CAT_FILE):
        with open(CAT_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                categories.append(row)
    return categories

def save_categories(categories):
    with open(CAT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Name"])
        writer.writeheader()
        writer.writerows(categories)