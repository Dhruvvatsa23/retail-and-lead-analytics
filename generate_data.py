"""
Generate Realistic Business Data with Meaningful Patterns
==========================================================
This script generates synthetic data that tells a COHERENT BUSINESS STORY.

Key Design Principles:
1. Data has realistic seasonal patterns (holiday spikes, summer slowdowns)
2. Stores have distinct personalities (top performer, struggling store, etc.)
3. Products have lifecycle patterns (new launches, declining items)
4. Numbers RELATE to each other (high sales = low stock, good source = high conversion)
5. There are "discoveries" to be made in the data

Business Story for Retail:
- It's a 6-month view of a multi-category retailer
- Holiday season (Nov-Dec) shows clear spike
- Store E is underperforming and needs attention
- Electronics is the star category, Beauty is growing fast
- Some products are running critically low on stock

Business Story for Leads:
- Marketing team is testing different channels
- Referrals convert best but are limited volume
- Google Ads brings volume but lower quality
- One sales rep (Eva) is exceptional, one (David) needs coaching
- Trade shows bring high-value leads in bursts

Author: Birva
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import json

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

END_DATE = datetime(2024, 12, 31)  # End at year-end for clear seasonality
START_DATE = END_DATE - timedelta(days=180)  # 6 months back

# Store profiles - each has distinct characteristics
STORE_PROFILES = {
    'Downtown Flagship': {'multiplier': 1.4, 'trend': 'growing', 'specialty': 'Electronics'},
    'Mall Central': {'multiplier': 1.2, 'trend': 'stable', 'specialty': 'Clothing'},
    'Suburban Plaza': {'multiplier': 1.0, 'trend': 'stable', 'specialty': 'Home & Kitchen'},
    'Airport Express': {'multiplier': 0.9, 'trend': 'growing', 'specialty': 'Beauty'},
    'Outlet Store': {'multiplier': 0.6, 'trend': 'declining', 'specialty': None}  # Struggling store
}

# Category data with realistic pricing and seasonality
CATEGORIES = {
    'Electronics': {
        'products': [
            {'name': 'Wireless Earbuds Pro', 'base_price': 149, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Smart Watch Series X', 'base_price': 299, 'popularity': 'high', 'trend': 'growing'},
            {'name': '4K Webcam', 'base_price': 89, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Portable Charger 20K', 'base_price': 45, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Bluetooth Speaker Mini', 'base_price': 79, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'USB-C Hub Pro', 'base_price': 65, 'popularity': 'medium', 'trend': 'growing'},
            {'name': 'Noise Canceling Headphones', 'base_price': 249, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Tablet Stand Adjustable', 'base_price': 35, 'popularity': 'low', 'trend': 'declining'},
            {'name': 'Wireless Mouse Ergonomic', 'base_price': 55, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'LED Desk Lamp Smart', 'base_price': 75, 'popularity': 'medium', 'trend': 'growing'}
        ],
        'seasonal_peak': [11, 12],  # Nov-Dec holiday spike
        'base_demand': 1.3
    },
    'Clothing': {
        'products': [
            {'name': 'Premium Cotton T-Shirt', 'base_price': 35, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Slim Fit Jeans', 'base_price': 75, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Winter Jacket Insulated', 'base_price': 189, 'popularity': 'medium', 'trend': 'seasonal'},
            {'name': 'Running Sneakers Pro', 'base_price': 129, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Casual Hoodie', 'base_price': 65, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Formal Dress Shirt', 'base_price': 55, 'popularity': 'medium', 'trend': 'declining'},
            {'name': 'Athletic Shorts', 'base_price': 40, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Wool Sweater Classic', 'base_price': 95, 'popularity': 'medium', 'trend': 'seasonal'},
            {'name': 'Canvas Sneakers', 'base_price': 55, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Baseball Cap Logo', 'base_price': 28, 'popularity': 'low', 'trend': 'stable'}
        ],
        'seasonal_peak': [10, 11, 12],  # Fall/Winter
        'base_demand': 1.0
    },
    'Home & Kitchen': {
        'products': [
            {'name': 'Air Fryer Digital 5L', 'base_price': 119, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Coffee Maker Programmable', 'base_price': 89, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Knife Set Professional', 'base_price': 149, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Non-Stick Pan Set', 'base_price': 79, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Blender High-Speed', 'base_price': 99, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Instant Pot Multi-Use', 'base_price': 129, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Toaster 4-Slice', 'base_price': 55, 'popularity': 'low', 'trend': 'declining'},
            {'name': 'Food Storage Set', 'base_price': 45, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Electric Kettle', 'base_price': 40, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Kitchen Scale Digital', 'base_price': 25, 'popularity': 'low', 'trend': 'stable'}
        ],
        'seasonal_peak': [11, 12],  # Holiday gifting
        'base_demand': 0.9
    },
    'Beauty': {
        'products': [
            {'name': 'Vitamin C Serum', 'base_price': 45, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Hair Dryer Professional', 'base_price': 129, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Moisturizer Daily SPF', 'base_price': 38, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Perfume Signature 50ml', 'base_price': 85, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Makeup Brush Set', 'base_price': 55, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Face Mask Hydrating', 'base_price': 28, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Curling Iron Ceramic', 'base_price': 75, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Nail Polish Set', 'base_price': 32, 'popularity': 'low', 'trend': 'stable'},
            {'name': 'Electric Shaver', 'base_price': 89, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Lip Balm Collection', 'base_price': 18, 'popularity': 'medium', 'trend': 'stable'}
        ],
        'seasonal_peak': [11, 12, 2],  # Holidays + Valentine's
        'base_demand': 1.1
    },
    'Sports': {
        'products': [
            {'name': 'Yoga Mat Premium', 'base_price': 45, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Dumbbell Set Adjustable', 'base_price': 199, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Fitness Tracker Band', 'base_price': 79, 'popularity': 'high', 'trend': 'growing'},
            {'name': 'Resistance Bands Set', 'base_price': 28, 'popularity': 'high', 'trend': 'hot'},
            {'name': 'Water Bottle Insulated', 'base_price': 32, 'popularity': 'high', 'trend': 'stable'},
            {'name': 'Jump Rope Speed', 'base_price': 18, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Foam Roller', 'base_price': 35, 'popularity': 'medium', 'trend': 'growing'},
            {'name': 'Gym Bag Duffle', 'base_price': 55, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Protein Shaker Bottle', 'base_price': 15, 'popularity': 'medium', 'trend': 'stable'},
            {'name': 'Exercise Ball 65cm', 'base_price': 28, 'popularity': 'low', 'trend': 'declining'}
        ],
        'seasonal_peak': [1, 9],  # New Year resolutions + Back to routine
        'base_demand': 0.8
    }
}

# Lead source profiles - each has distinct conversion characteristics
LEAD_SOURCES = {
    'Google Ads': {'volume': 'high', 'quality': 0.15, 'avg_deal': 25000, 'cost_per_lead': 150},
    'Facebook Ads': {'volume': 'high', 'quality': 0.12, 'avg_deal': 18000, 'cost_per_lead': 80},
    'LinkedIn': {'volume': 'medium', 'quality': 0.25, 'avg_deal': 45000, 'cost_per_lead': 200},
    'Referral': {'volume': 'low', 'quality': 0.45, 'avg_deal': 55000, 'cost_per_lead': 50},
    'Organic Search': {'volume': 'medium', 'quality': 0.20, 'avg_deal': 30000, 'cost_per_lead': 0},
    'Email Campaign': {'volume': 'medium', 'quality': 0.18, 'avg_deal': 22000, 'cost_per_lead': 25},
    'Trade Show': {'volume': 'low', 'quality': 0.35, 'avg_deal': 75000, 'cost_per_lead': 500},
    'Cold Outreach': {'volume': 'medium', 'quality': 0.08, 'avg_deal': 15000, 'cost_per_lead': 100}
}

# Sales rep profiles
SALES_REPS = {
    'Eva Martinez': {'skill': 1.3, 'specialty': 'Enterprise', 'close_rate_bonus': 0.15},
    'James Wilson': {'skill': 1.1, 'specialty': 'Mid-Market', 'close_rate_bonus': 0.05},
    'Sarah Chen': {'skill': 1.0, 'specialty': 'SMB', 'close_rate_bonus': 0.0},
    'Michael Brown': {'skill': 0.95, 'specialty': 'Mid-Market', 'close_rate_bonus': -0.03},
    'David Kim': {'skill': 0.75, 'specialty': 'SMB', 'close_rate_bonus': -0.10}  # Needs coaching
}

# ============================================================================
# RETAIL DATA GENERATION
# ============================================================================

def get_seasonal_multiplier(date, category_data):
    """Calculate seasonal demand multiplier based on month."""
    month = date.month
    peak_months = category_data.get('seasonal_peak', [])

    if month in peak_months:
        return 1.5 + random.uniform(0, 0.3)
    elif month in [7, 8]:  # Summer slump for most retail
        return 0.7 + random.uniform(0, 0.1)
    else:
        return 1.0 + random.uniform(-0.1, 0.1)

def get_trend_multiplier(product, days_from_start):
    """Calculate trend multiplier based on product lifecycle."""
    trend = product.get('trend', 'stable')
    progress = days_from_start / 180  # 0 to 1 over 6 months

    if trend == 'hot':
        return 1.2 + (progress * 0.4)  # Growing fast
    elif trend == 'growing':
        return 1.0 + (progress * 0.2)
    elif trend == 'declining':
        return 1.0 - (progress * 0.3)
    elif trend == 'seasonal':
        return 1.0  # Handled by seasonal multiplier
    else:
        return 1.0 + random.uniform(-0.05, 0.05)

def get_popularity_base(product):
    """Get base transaction frequency based on popularity."""
    popularity = product.get('popularity', 'medium')
    if popularity == 'high':
        return 3
    elif popularity == 'medium':
        return 2
    else:
        return 1

def generate_retail_data():
    """Generate retail sales data with realistic patterns."""
    print("\n" + "="*60)
    print("GENERATING RETAIL SALES DATA WITH BUSINESS PATTERNS")
    print("="*60)

    transactions = []
    product_stock = {}  # Track stock levels

    # Initialize stock levels
    for category, cat_data in CATEGORIES.items():
        for product in cat_data['products']:
            # Hot/popular products start with more stock
            base_stock = 500 if product['popularity'] == 'high' else 300 if product['popularity'] == 'medium' else 200
            product_stock[product['name']] = base_stock

    # Generate transactions day by day
    current_date = START_DATE
    transaction_id = 1

    while current_date <= END_DATE:
        days_from_start = (current_date - START_DATE).days
        is_weekend = current_date.weekday() >= 5

        for category, cat_data in CATEGORIES.items():
            seasonal_mult = get_seasonal_multiplier(current_date, cat_data)

            for product in cat_data['products']:
                # Calculate how many transactions for this product today
                base_transactions = get_popularity_base(product)
                trend_mult = get_trend_multiplier(product, days_from_start)

                # Weekend boost
                weekend_mult = 1.3 if is_weekend else 1.0

                # Calculate expected transactions
                expected = base_transactions * seasonal_mult * trend_mult * weekend_mult * cat_data['base_demand']
                num_transactions = np.random.poisson(expected)

                for _ in range(num_transactions):
                    # Pick a store (weighted by profile)
                    store_weights = []
                    stores = list(STORE_PROFILES.keys())
                    for store, profile in STORE_PROFILES.items():
                        weight = profile['multiplier']
                        # Boost if this is store's specialty
                        if profile['specialty'] == category:
                            weight *= 1.3
                        store_weights.append(weight)

                    store = random.choices(stores, weights=store_weights)[0]
                    store_profile = STORE_PROFILES[store]

                    # Quantity (usually 1-2, occasionally more)
                    quantity = random.choices([1, 2, 3, 4, 5], weights=[60, 25, 10, 3, 2])[0]

                    # Price with small variations
                    base_price = product['base_price']
                    # Outlet store has discounts
                    if store == 'Outlet Store':
                        price = base_price * random.uniform(0.7, 0.85)
                    else:
                        price = base_price * random.uniform(0.95, 1.05)

                    # Update stock
                    product_stock[product['name']] = max(0, product_stock[product['name']] - quantity)

                    transactions.append({
                        'transaction_id': f'TXN{transaction_id:06d}',
                        'date': current_date.strftime('%Y-%m-%d'),
                        'product_name': product['name'],
                        'category': category,
                        'unit_price': round(price, 2),
                        'quantity': quantity,
                        'total_revenue': round(price * quantity, 2),
                        'store': store,
                        'stock_level': product_stock[product['name']],
                        'day_of_week': current_date.strftime('%A'),
                        'month': current_date.strftime('%Y-%m'),
                        'is_weekend': is_weekend,
                        'product_trend': product['trend']
                    })
                    transaction_id += 1

        # Restock simulation (every week, partial restock)
        if current_date.weekday() == 0:  # Monday
            for product_name in product_stock:
                # Restock based on how low stock is
                if product_stock[product_name] < 100:
                    product_stock[product_name] += random.randint(50, 150)
                elif product_stock[product_name] < 200:
                    product_stock[product_name] += random.randint(30, 80)

        current_date += timedelta(days=1)

    df = pd.DataFrame(transactions)

    print(f"Generated {len(df):,} transactions")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total revenue: ${df['total_revenue'].sum():,.2f}")

    return df

# ============================================================================
# LEAD DATA GENERATION
# ============================================================================

def generate_lead_data():
    """Generate marketing lead data with realistic conversion patterns."""
    print("\n" + "="*60)
    print("GENERATING MARKETING LEAD DATA WITH FUNNEL LOGIC")
    print("="*60)

    leads = []
    lead_id = 1

    # Company names for realism
    companies = [
        'Acme Corp', 'TechStart Inc', 'Global Solutions', 'InnovateCo', 'DataDrive LLC',
        'CloudFirst', 'Quantum Systems', 'NexGen Industries', 'PrimeLogic', 'VelocityTech',
        'Summit Partners', 'Horizon Group', 'Atlas Enterprises', 'Forge Digital', 'Spark Ventures',
        'ClearPath Analytics', 'BlueWave Solutions', 'RedRock Systems', 'GreenField Tech', 'SilverLine Corp',
        'Northern Dynamics', 'Pacific Digital', 'Central Hub Inc', 'Eastern Networks', 'Western Systems'
    ]

    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
                   'William', 'Elizabeth', 'David', 'Susan', 'Richard', 'Jessica', 'Joseph', 'Sarah',
                   'Thomas', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty']

    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White']

    industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Services']

    current_date = START_DATE

    while current_date <= END_DATE:
        # Generate leads for each source
        for source, profile in LEAD_SOURCES.items():
            # Determine how many leads today
            if profile['volume'] == 'high':
                base_leads = 3
            elif profile['volume'] == 'medium':
                base_leads = 2
            else:
                base_leads = 1

            # Trade shows happen in bursts (simulate 2 trade shows in 6 months)
            if source == 'Trade Show':
                # Trade shows in months 2 and 5
                if current_date.month in [8, 11] and current_date.day <= 5:
                    num_leads = random.randint(8, 15)
                else:
                    num_leads = 0
            else:
                num_leads = np.random.poisson(base_leads)

            for _ in range(num_leads):
                # Generate lead details
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                company = random.choice(companies) + f" {random.choice(['Inc', 'LLC', 'Corp', 'Group'])}"
                industry = random.choice(industries)

                # Deal value based on source profile with variation
                base_deal = profile['avg_deal']
                deal_value = int(base_deal * random.uniform(0.5, 2.0))

                # Assign sales rep (weighted by skill for higher value deals)
                if deal_value > 50000:
                    rep_weights = [p['skill'] * 1.5 if p['specialty'] == 'Enterprise' else p['skill']
                                   for p in SALES_REPS.values()]
                elif deal_value > 25000:
                    rep_weights = [p['skill'] * 1.3 if p['specialty'] == 'Mid-Market' else p['skill']
                                   for p in SALES_REPS.values()]
                else:
                    rep_weights = [p['skill'] for p in SALES_REPS.values()]

                sales_rep = random.choices(list(SALES_REPS.keys()), weights=rep_weights)[0]
                rep_profile = SALES_REPS[sales_rep]

                # Calculate conversion probability
                base_quality = profile['quality']
                rep_bonus = rep_profile['close_rate_bonus']
                conversion_prob = min(0.8, max(0.05, base_quality + rep_bonus))

                # Determine stage based on time elapsed and probability
                days_since_created = (END_DATE - current_date).days

                # Leads progress through stages over time
                if days_since_created < 7:
                    stage = 'Lead'
                elif days_since_created < 14:
                    stage = random.choices(['Lead', 'Contacted'], weights=[30, 70])[0]
                elif days_since_created < 30:
                    if random.random() < conversion_prob:
                        stage = random.choices(['Contacted', 'Qualified', 'Proposal'], weights=[20, 50, 30])[0]
                    else:
                        stage = random.choices(['Lead', 'Contacted'], weights=[40, 60])[0]
                elif days_since_created < 60:
                    if random.random() < conversion_prob:
                        stage = random.choices(['Qualified', 'Proposal', 'Negotiation'], weights=[30, 40, 30])[0]
                    else:
                        stage = random.choices(['Lead', 'Contacted', 'Qualified'], weights=[30, 40, 30])[0]
                else:
                    # Older leads - should be resolved
                    if random.random() < conversion_prob:
                        stage = random.choices(['Proposal', 'Negotiation', 'Closed Won'], weights=[20, 30, 50])[0]
                    else:
                        stage = random.choices(['Qualified', 'Closed Lost'], weights=[30, 70])[0]

                # Stage probabilities
                stage_probs = {
                    'Lead': 0.10, 'Contacted': 0.20, 'Qualified': 0.40,
                    'Proposal': 0.60, 'Negotiation': 0.75, 'Closed Won': 1.0, 'Closed Lost': 0.0
                }

                # Calculate dates
                lead_date = current_date
                contact_date = lead_date + timedelta(days=random.randint(1, 5))

                # Days to convert (if closed)
                if stage in ['Closed Won', 'Closed Lost']:
                    days_to_close = random.randint(30, 90)
                    close_date = lead_date + timedelta(days=days_to_close)
                else:
                    days_to_close = None
                    close_date = None

                leads.append({
                    'lead_id': f'LEAD{lead_id:05d}',
                    'first_name': first_name,
                    'last_name': last_name,
                    'full_name': f'{first_name} {last_name}',
                    'email': f'{first_name.lower()}.{last_name.lower()}@{company.split()[0].lower()}.com',
                    'company': company,
                    'industry': industry,
                    'lead_date': lead_date.strftime('%Y-%m-%d'),
                    'contact_date': contact_date.strftime('%Y-%m-%d'),
                    'close_date': close_date.strftime('%Y-%m-%d') if close_date else None,
                    'source': source,
                    'stage': stage,
                    'deal_value': deal_value,
                    'probability': stage_probs[stage],
                    'expected_value': int(deal_value * stage_probs[stage]),
                    'sales_rep': sales_rep,
                    'lead_month': lead_date.strftime('%Y-%m'),
                    'days_in_pipeline': days_since_created,
                    'cost_per_lead': profile['cost_per_lead']
                })
                lead_id += 1

        current_date += timedelta(days=1)

    df = pd.DataFrame(leads)

    print(f"Generated {len(df):,} leads")
    print(f"Date range: {df['lead_date'].min()} to {df['lead_date'].max()}")
    print(f"Total pipeline: ${df['deal_value'].sum():,.0f}")

    # Print source analysis
    print("\nSource Performance:")
    source_stats = df.groupby('source').agg({
        'lead_id': 'count',
        'deal_value': 'sum',
        'expected_value': 'sum'
    }).round(0)

    # Calculate conversion rates
    for source in df['source'].unique():
        source_df = df[df['source'] == source]
        closed = source_df[source_df['stage'].isin(['Closed Won', 'Closed Lost'])]
        if len(closed) > 0:
            won = len(closed[closed['stage'] == 'Closed Won'])
            rate = won / len(closed) * 100
            print(f"  {source}: {len(source_df)} leads, {rate:.1f}% conversion rate")

    return df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*60)
    print("BUSINESS ANALYTICS DATA GENERATION")
    print("="*60)
    print(f"Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print("\nThis data tells a coherent business story:")
    print("- Seasonal patterns (holiday spike in Nov-Dec)")
    print("- Store performance variations (one struggling store)")
    print("- Product lifecycle trends (hot products vs declining)")
    print("- Marketing channel effectiveness differences")
    print("- Sales rep performance variations")

    # Create data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Generate data
    retail_df = generate_retail_data()
    leads_df = generate_lead_data()

    # Save to CSV
    retail_path = os.path.join(data_dir, 'retail_sales_cleaned.csv')
    leads_path = os.path.join(data_dir, 'marketing_leads_cleaned.csv')

    retail_df.to_csv(retail_path, index=False)
    leads_df.to_csv(leads_path, index=False)

    # Also save as JSON for easy JavaScript consumption
    retail_json_path = os.path.join(data_dir, 'retail_sales.json')
    leads_json_path = os.path.join(data_dir, 'marketing_leads.json')

    retail_df.to_json(retail_json_path, orient='records', date_format='iso')
    leads_df.to_json(leads_json_path, orient='records', date_format='iso')

    print("\n" + "="*60)
    print("DATA SAVED")
    print("="*60)
    print(f"CSV: {retail_path}")
    print(f"CSV: {leads_path}")
    print(f"JSON: {retail_json_path}")
    print(f"JSON: {leads_json_path}")

    # Print key insights that users should be able to discover
    print("\n" + "="*60)
    print("KEY INSIGHTS TO DISCOVER IN THE DATA")
    print("="*60)

    print("\nRetail Insights:")
    # Best performing store
    store_revenue = retail_df.groupby('store')['total_revenue'].sum().sort_values(ascending=False)
    print(f"1. Best store: {store_revenue.index[0]} (${store_revenue.iloc[0]:,.0f})")
    print(f"   Worst store: {store_revenue.index[-1]} (${store_revenue.iloc[-1]:,.0f}) - needs attention!")

    # Best category
    cat_revenue = retail_df.groupby('category')['total_revenue'].sum().sort_values(ascending=False)
    print(f"2. Top category: {cat_revenue.index[0]} (${cat_revenue.iloc[0]:,.0f})")

    # Holiday spike
    monthly = retail_df.groupby('month')['total_revenue'].sum()
    print(f"3. Holiday spike: December revenue is highest at ${monthly.max():,.0f}")

    # Hot products
    hot_products = retail_df[retail_df['product_trend'] == 'hot'].groupby('product_name')['total_revenue'].sum()
    print(f"4. Hot products driving growth: {', '.join(hot_products.nlargest(3).index.tolist())}")

    # Low stock alerts
    latest_stock = retail_df.sort_values('date').groupby('product_name').last()
    low_stock = latest_stock[latest_stock['stock_level'] < 50].sort_values('stock_level')
    if len(low_stock) > 0:
        print(f"5. Low stock alert: {len(low_stock)} products need restocking!")

    print("\nLead Insights:")
    # Best source by conversion
    source_conv = leads_df.groupby('source').apply(
        lambda x: len(x[x['stage'] == 'Closed Won']) / max(1, len(x[x['stage'].isin(['Closed Won', 'Closed Lost'])])) * 100
    ).sort_values(ascending=False)
    print(f"1. Best converting source: {source_conv.index[0]} ({source_conv.iloc[0]:.1f}% conversion)")

    # Best sales rep
    rep_won = leads_df[leads_df['stage'] == 'Closed Won'].groupby('sales_rep')['deal_value'].sum().sort_values(ascending=False)
    print(f"2. Top performer: {rep_won.index[0]} (${rep_won.iloc[0]:,.0f} closed)")

    # Rep needing coaching
    rep_lost = leads_df[leads_df['stage'] == 'Closed Lost'].groupby('sales_rep')['deal_value'].count()
    print(f"3. Needs coaching: {rep_lost.idxmax()} (highest lost deals)")

    # Pipeline value
    pipeline = leads_df[~leads_df['stage'].isin(['Closed Won', 'Closed Lost'])]['expected_value'].sum()
    print(f"4. Active pipeline: ${pipeline:,.0f} expected value")

    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE!")
    print("="*60)
    print("\nNext: Run 'python create_dashboards.py' to generate interactive dashboards.")

if __name__ == "__main__":
    main()
