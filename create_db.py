import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Initialize local SQLite connection
conn = sqlite3.connect('retail_sandbox.db')

# 2. Generate 5,000 synthetic transactions
np.random.seed(42)
categories = ['Fruits and Vegetables', 'Dairy', 'Auto Care', 'Home Improvement']

data = {
    'transaction_id': range(1001, 6001),
    'date': [datetime(2026, 3, 1).date() + timedelta(days=np.random.randint(0, 30)) for _ in range(5000)],
    'category': np.random.choice(categories, 5000, p=[0.4, 0.3, 0.15, 0.15]),
    'units_sold': np.random.randint(1, 15, 5000),
    'unit_price': np.random.uniform(20.0, 450.0, 5000).round(2)
}

df = pd.DataFrame(data)
df['gmv'] = df['units_sold'] * df['unit_price'] # Gross Merchandise Value

# 3. Load into SQLite
df.to_sql('daily_sales', conn, index=False, if_exists='replace')
print("✅ retail_sandbox.db successfully generated with 5,000 rows.")
conn.close()