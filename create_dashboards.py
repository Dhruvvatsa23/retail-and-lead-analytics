"""
Create Interactive Business Dashboards
=======================================
This script generates highly interactive HTML dashboards with:
- Real-time filtering across all charts
- Cross-filtering (click one chart to filter others)
- Dynamic KPI updates
- Insight discovery highlights
- Engaging tooltips and animations
- Data context and storytelling

Author: Birva
Date: 2024
"""

import pandas as pd
import json
import os
from datetime import datetime

# ============================================================================
# RETAIL INVENTORY DASHBOARD - FULLY INTERACTIVE
# ============================================================================

def create_retail_dashboard(df):
    """Create an interactive retail dashboard with filters and insights."""
    print("Creating Interactive Retail Dashboard...")

    # Prepare data for JavaScript
    data_json = df.to_json(orient='records')

    # Pre-calculate some aggregations for initial load
    total_revenue = df['total_revenue'].sum()
    total_transactions = len(df)
    unique_products = df['product_name'].nunique()

    # Get unique values for filters
    categories = sorted(df['category'].unique().tolist())
    stores = sorted(df['store'].unique().tolist())
    months = sorted(df['month'].unique().tolist())
    products = sorted(df['product_name'].unique().tolist())

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Analytics Dashboard | Interactive Business Intelligence</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            background: #f0f2f5;
            color: #1a1a2e;
            line-height: 1.6;
        }}

        /* Navigation */
        .nav {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}

        .nav a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: color 0.2s;
        }}

        .nav a:hover {{
            color: white;
        }}

        .nav h1 {{
            color: white;
            font-size: 20px;
            font-weight: 600;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}

        /* Context Banner */
        .context-banner {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
        }}

        .context-banner::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
        }}

        .context-banner h2 {{
            font-size: 22px;
            margin-bottom: 10px;
            position: relative;
        }}

        .context-banner p {{
            font-size: 14px;
            opacity: 0.95;
            max-width: 700px;
            position: relative;
        }}

        .context-banner .data-period {{
            position: absolute;
            top: 25px;
            right: 30px;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
        }}

        /* Filter Panel */
        .filter-panel {{
            background: white;
            padding: 20px 25px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: flex-end;
        }}

        .filter-group {{
            flex: 1;
            min-width: 180px;
        }}

        .filter-group label {{
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .filter-group select {{
            width: 100%;
            padding: 10px 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}

        .filter-group select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .filter-group select:hover {{
            border-color: #667eea;
        }}

        .btn-reset {{
            padding: 10px 20px;
            background: #f0f2f5;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .btn-reset:hover {{
            background: #e74c3c;
            border-color: #e74c3c;
            color: white;
        }}

        .active-filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #eee;
        }}

        .filter-tag {{
            background: #667eea;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .filter-tag .remove {{
            cursor: pointer;
            opacity: 0.8;
        }}

        .filter-tag .remove:hover {{
            opacity: 1;
        }}

        /* KPI Cards */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .kpi-card {{
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}

        .kpi-card .icon {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}

        .kpi-card.revenue .icon {{ background: rgba(102, 126, 234, 0.1); }}
        .kpi-card.transactions .icon {{ background: rgba(46, 204, 113, 0.1); }}
        .kpi-card.products .icon {{ background: rgba(243, 156, 18, 0.1); }}
        .kpi-card.avg .icon {{ background: rgba(155, 89, 182, 0.1); }}

        .kpi-card .label {{
            font-size: 13px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .kpi-card .value {{
            font-size: 32px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 8px;
        }}

        .kpi-card .trend {{
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .kpi-card .trend.up {{ color: #27ae60; }}
        .kpi-card .trend.down {{ color: #e74c3c; }}
        .kpi-card .trend.neutral {{ color: #888; }}

        /* Insight Cards */
        .insights-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .insight-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .insight-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}

        .insight-card.positive {{ border-color: #27ae60; }}
        .insight-card.warning {{ border-color: #f39c12; }}
        .insight-card.negative {{ border-color: #e74c3c; }}
        .insight-card.info {{ border-color: #3498db; }}

        .insight-card .insight-icon {{
            font-size: 24px;
            margin-bottom: 10px;
        }}

        .insight-card h4 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }}

        .insight-card .insight-value {{
            font-size: 20px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 5px;
        }}

        .insight-card p {{
            font-size: 13px;
            color: #888;
        }}

        /* Chart Sections */
        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 25px;
            margin-bottom: 25px;
        }}

        .chart-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .chart-card.full-width {{
            grid-column: 1 / -1;
        }}

        .chart-card h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .chart-card .chart-subtitle {{
            font-size: 13px;
            color: #888;
            margin-bottom: 20px;
        }}

        .chart-card .chart-help {{
            font-size: 12px;
            color: #667eea;
            cursor: help;
        }}

        /* Data Table */
        .data-table-container {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 25px;
            overflow: hidden;
        }}

        .data-table-container h3 {{
            font-size: 16px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .table-search {{
            padding: 8px 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 13px;
            width: 250px;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th {{
            background: #f8f9fa;
            padding: 14px 16px;
            text-align: left;
            font-size: 12px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e0e0e0;
            cursor: pointer;
            transition: background 0.2s;
            white-space: nowrap;
        }}

        .data-table th:hover {{
            background: #e8e9ea;
        }}

        .data-table th.sorted-asc::after {{ content: ' ↑'; }}
        .data-table th.sorted-desc::after {{ content: ' ↓'; }}

        .data-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }}

        .data-table tr:hover {{
            background: #f8f9fa;
        }}

        .data-table tr.clickable {{
            cursor: pointer;
        }}

        .stock-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}

        .stock-badge.critical {{ background: #fde8e8; color: #c0392b; }}
        .stock-badge.low {{ background: #fef3e2; color: #d68910; }}
        .stock-badge.ok {{ background: #e8f6ef; color: #27ae60; }}

        .trend-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 500;
        }}

        .trend-badge.hot {{ background: #fde8e8; color: #c0392b; }}
        .trend-badge.growing {{ background: #e8f6ef; color: #27ae60; }}
        .trend-badge.stable {{ background: #e8f0fe; color: #2980b9; }}
        .trend-badge.declining {{ background: #f5f5f5; color: #888; }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            color: #888;
            font-size: 13px;
        }}

        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}

        /* Loading State */
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            color: #888;
        }}

        .loading::after {{
            content: '';
            width: 30px;
            height: 30px;
            border: 3px solid #e0e0e0;
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-left: 10px;
        }}

        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}

        /* Tooltip Enhancement */
        .custom-tooltip {{
            position: fixed;
            background: #1a1a2e;
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 13px;
            pointer-events: none;
            z-index: 1000;
            max-width: 300px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            opacity: 0;
            transition: opacity 0.2s;
        }}

        .custom-tooltip.visible {{
            opacity: 1;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .nav {{ padding: 12px 20px; }}
            .nav h1 {{ font-size: 16px; }}
            .context-banner {{ padding: 20px; }}
            .context-banner .data-period {{ position: static; margin-top: 15px; display: inline-block; }}
            .filter-panel {{ padding: 15px; }}
            .filter-group {{ min-width: 100%; }}
            .kpi-card .value {{ font-size: 26px; }}
            .chart-row {{ grid-template-columns: 1fr; }}
            .chart-card {{ padding: 16px; }}
        }}

        /* Animation for value changes */
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}

        .value-updated {{
            animation: pulse 0.3s ease;
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <a href="index.html">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back to Portfolio
        </a>
        <h1>Retail Analytics Dashboard</h1>
        <div style="width: 120px;"></div>
    </nav>

    <div class="container">
        <!-- Context Banner -->
        <div class="context-banner">
            <span class="data-period" id="dataPeriod">Loading...</span>
            <h2>Multi-Store Retail Performance Analysis</h2>
            <p>This view summarizes daily transactions across five stores and five product categories. It’s designed to reveal
            seasonal spikes, store strengths, and product lifecycle trends without overcomplicating the logic.</p>
            <p><strong>How to use:</strong> Apply filters below or click any chart element to cross‑filter the entire dashboard.</p>
        </div>

        <!-- Filter Panel -->
        <div class="filter-panel">
            <div class="filter-group">
                <label>Category</label>
                <select id="filterCategory">
                    <option value="all">All Categories</option>
                    {' '.join([f'<option value="{cat}">{cat}</option>' for cat in categories])}
                </select>
            </div>
            <div class="filter-group">
                <label>Store</label>
                <select id="filterStore">
                    <option value="all">All Stores</option>
                    {' '.join([f'<option value="{store}">{store}</option>' for store in stores])}
                </select>
            </div>
            <div class="filter-group">
                <label>Month</label>
                <select id="filterMonth">
                    <option value="all">All Months</option>
                    {' '.join([f'<option value="{month}">{month}</option>' for month in months])}
                </select>
            </div>
            <div class="filter-group">
                <label>Product Trend</label>
                <select id="filterTrend">
                    <option value="all">All Trends</option>
                    <option value="hot">Hot Products</option>
                    <option value="growing">Growing</option>
                    <option value="stable">Stable</option>
                    <option value="declining">Declining</option>
                </select>
            </div>
            <button class="btn-reset" onclick="resetFilters()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                    <path d="M3 3v5h5"/>
                </svg>
                Reset
            </button>
        </div>
        <div class="active-filters" id="activeFilters"></div>

        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card revenue">
                <div class="icon">💰</div>
                <div class="label">Total Revenue</div>
                <div class="value" id="kpiRevenue">$0</div>
                <div class="trend neutral" id="kpiRevenueTrend">Loading...</div>
            </div>
            <div class="kpi-card transactions">
                <div class="icon">🛒</div>
                <div class="label">Transactions</div>
                <div class="value" id="kpiTransactions">0</div>
                <div class="trend neutral" id="kpiTransactionsTrend">Loading...</div>
            </div>
            <div class="kpi-card products">
                <div class="icon">📦</div>
                <div class="label">Products Sold</div>
                <div class="value" id="kpiProducts">0</div>
                <div class="trend neutral" id="kpiProductsTrend">Loading...</div>
            </div>
            <div class="kpi-card avg">
                <div class="icon">📊</div>
                <div class="label">Avg Transaction</div>
                <div class="value" id="kpiAvg">$0</div>
                <div class="trend neutral" id="kpiAvgTrend">Loading...</div>
            </div>
        </div>

        <!-- Dynamic Insights -->
        <div class="insights-row" id="insightsRow">
            <!-- Populated by JavaScript -->
        </div>

        <!-- Charts Row 1 -->
        <div class="chart-row">
            <div class="chart-card full-width">
                <h3>
                    Revenue Trend Over Time
                    <span class="chart-help" title="Click on data points to filter by month">ℹ️ Interactive</span>
                </h3>
                <div class="chart-subtitle">Daily revenue with trend line - click any point to explore that period</div>
                <div id="trendChart" style="height: 300px;"></div>
            </div>
        </div>

        <!-- Charts Row 2 -->
        <div class="chart-row">
            <div class="chart-card">
                <h3>Revenue by Category</h3>
                <div class="chart-subtitle">Click a segment to filter dashboard by category</div>
                <div id="categoryChart" style="height: 320px;"></div>
            </div>
            <div class="chart-card">
                <h3>Store Performance</h3>
                <div class="chart-subtitle">Revenue comparison across locations - click to filter</div>
                <div id="storeChart" style="height: 320px;"></div>
            </div>
        </div>

        <!-- Charts Row 3 -->
        <div class="chart-row">
            <div class="chart-card">
                <h3>Top 10 Products</h3>
                <div class="chart-subtitle">Best sellers by revenue - click to see product details</div>
                <div id="productsChart" style="height: 350px;"></div>
            </div>
            <div class="chart-card">
                <h3>Sales by Day of Week</h3>
                <div class="chart-subtitle">Understand weekly patterns to optimize staffing</div>
                <div id="dowChart" style="height: 350px;"></div>
            </div>
        </div>

        <!-- Product Performance Table -->
        <div class="data-table-container">
            <h3>
                Product Performance Details
                <input type="text" class="table-search" placeholder="Search products..." id="tableSearch" oninput="filterTable()">
            </h3>
            <div style="overflow-x: auto;">
                <table class="data-table" id="productTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Product</th>
                            <th onclick="sortTable(1)">Category</th>
                            <th onclick="sortTable(2)">Revenue</th>
                            <th onclick="sortTable(3)">Units Sold</th>
                            <th onclick="sortTable(4)">Avg Price</th>
                            <th onclick="sortTable(5)">Stock Level</th>
                            <th onclick="sortTable(6)">Trend</th>
                        </tr>
                    </thead>
                    <tbody id="productTableBody">
                        <!-- Populated by JavaScript -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>Interactive Business Analytics Dashboard | Built with Plotly.js</p>
            <p style="margin-top: 8px;"><a href="index.html">Back to Portfolio</a> | Data refreshed in real-time based on filters</p>
        </div>
    </div>

    <script>
        // ================================================================
        // DATA AND STATE
        // ================================================================
        const rawData = {data_json};
        let filteredData = [...rawData];
        let currentFilters = {{
            category: 'all',
            store: 'all',
            month: 'all',
            trend: 'all'
        }};

        const colors = {{
            primary: '#667eea',
            secondary: '#764ba2',
            success: '#27ae60',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#3498db',
            chart: ['#667eea', '#27ae60', '#f39c12', '#e74c3c', '#9b59b6', '#3498db', '#1abc9c', '#e67e22']
        }};

        // ================================================================
        // INITIALIZATION
        // ================================================================
        document.addEventListener('DOMContentLoaded', function() {{
            // Set data period
            const dates = rawData.map(d => d.date).sort();
            document.getElementById('dataPeriod').textContent =
                `${{dates[0]}} to ${{dates[dates.length-1]}}`;

            // Add filter event listeners
            document.getElementById('filterCategory').addEventListener('change', applyFilters);
            document.getElementById('filterStore').addEventListener('change', applyFilters);
            document.getElementById('filterMonth').addEventListener('change', applyFilters);
            document.getElementById('filterTrend').addEventListener('change', applyFilters);

            // Initial render
            updateDashboard();
        }});

        // ================================================================
        // FILTER FUNCTIONS
        // ================================================================
        function applyFilters() {{
            currentFilters.category = document.getElementById('filterCategory').value;
            currentFilters.store = document.getElementById('filterStore').value;
            currentFilters.month = document.getElementById('filterMonth').value;
            currentFilters.trend = document.getElementById('filterTrend').value;

            filteredData = rawData.filter(d => {{
                if (currentFilters.category !== 'all' && d.category !== currentFilters.category) return false;
                if (currentFilters.store !== 'all' && d.store !== currentFilters.store) return false;
                if (currentFilters.month !== 'all' && d.month !== currentFilters.month) return false;
                if (currentFilters.trend !== 'all' && d.product_trend !== currentFilters.trend) return false;
                return true;
            }});

            updateDashboard();
        }}

        function resetFilters() {{
            document.getElementById('filterCategory').value = 'all';
            document.getElementById('filterStore').value = 'all';
            document.getElementById('filterMonth').value = 'all';
            document.getElementById('filterTrend').value = 'all';
            currentFilters = {{ category: 'all', store: 'all', month: 'all', trend: 'all' }};
            filteredData = [...rawData];
            updateDashboard();
        }}

        function setFilter(type, value) {{
            document.getElementById('filter' + type.charAt(0).toUpperCase() + type.slice(1)).value = value;
            applyFilters();
        }}

        // ================================================================
        // UPDATE DASHBOARD
        // ================================================================
        function updateDashboard() {{
            updateActiveFilters();
            updateKPIs();
            updateInsights();
            updateTrendChart();
            updateCategoryChart();
            updateStoreChart();
            updateProductsChart();
            updateDOWChart();
            updateProductTable();
        }}

        function updateActiveFilters() {{
            const filters = [
                {{ key: 'category', label: 'Category' }},
                {{ key: 'store', label: 'Store' }},
                {{ key: 'month', label: 'Month' }},
                {{ key: 'trend', label: 'Trend' }}
            ];
            const tags = filters
                .filter(f => currentFilters[f.key] !== 'all')
                .map(f => `
                    <span class="filter-tag">
                        ${{f.label}}: ${{currentFilters[f.key]}}
                        <span class="remove" onclick="clearFilter('${{f.key}}')">×</span>
                    </span>
                `);
            document.getElementById('activeFilters').innerHTML = tags.join('');
        }}

        function clearFilter(key) {{
            const id = 'filter' + key.charAt(0).toUpperCase() + key.slice(1);
            document.getElementById(id).value = 'all';
            applyFilters();
        }}

        // ================================================================
        // KPI UPDATES
        // ================================================================
        function updateKPIs() {{
            const revenue = filteredData.reduce((sum, d) => sum + d.total_revenue, 0);
            const transactions = filteredData.length;
            const products = [...new Set(filteredData.map(d => d.product_name))].length;
            const avgTransaction = transactions > 0 ? revenue / transactions : 0;

            // Animate value changes
            animateValue('kpiRevenue', '$' + formatNumber(revenue));
            animateValue('kpiTransactions', formatNumber(transactions));
            animateValue('kpiProducts', products.toString());
            animateValue('kpiAvg', '$' + avgTransaction.toFixed(2));

            // Calculate trends (compare to full data)
            const fullRevenue = rawData.reduce((sum, d) => sum + d.total_revenue, 0);
            const revenuePercent = ((revenue / fullRevenue) * 100).toFixed(1);

            document.getElementById('kpiRevenueTrend').innerHTML =
                currentFilters.category !== 'all' || currentFilters.store !== 'all' || currentFilters.month !== 'all' || currentFilters.trend !== 'all'
                    ? `<span class="neutral">${{revenuePercent}}% of total revenue</span>`
                    : `<span class="up">↑ Full dataset</span>`;

            document.getElementById('kpiTransactionsTrend').innerHTML =
                `${{((transactions / rawData.length) * 100).toFixed(1)}}% of all transactions`;

            document.getElementById('kpiProductsTrend').innerHTML =
                `${{products}} of ${{[...new Set(rawData.map(d => d.product_name))].length}} products`;

            document.getElementById('kpiAvgTrend').innerHTML =
                avgTransaction > (fullRevenue / rawData.length)
                    ? '<span class="up">↑ Above average</span>'
                    : '<span class="down">↓ Below average</span>';
        }}

        function animateValue(elementId, newValue) {{
            const el = document.getElementById(elementId);
            if (el.textContent !== newValue) {{
                el.textContent = newValue;
                el.classList.add('value-updated');
                setTimeout(() => el.classList.remove('value-updated'), 300);
            }}
        }}

        // ================================================================
        // INSIGHTS
        // ================================================================
        function updateInsights() {{
            const insights = [];

            // Top store insight
            const storeRevenue = {{}};
            filteredData.forEach(d => {{
                storeRevenue[d.store] = (storeRevenue[d.store] || 0) + d.total_revenue;
            }});
            const topStore = Object.entries(storeRevenue).sort((a, b) => b[1] - a[1])[0];
            const worstStore = Object.entries(storeRevenue).sort((a, b) => a[1] - b[1])[0];

            if (topStore) {{
                insights.push({{
                    type: 'positive',
                    icon: '🏆',
                    title: 'Top Performing Store',
                    value: topStore[0],
                    detail: `${{formatNumber(topStore[1])}} in revenue`,
                    action: () => setFilter('store', topStore[0])
                }});
            }}

            // Struggling store
            if (worstStore && worstStore[0] === 'Outlet Store') {{
                insights.push({{
                    type: 'warning',
                    icon: '⚠️',
                    title: 'Needs Attention',
                    value: worstStore[0],
                    detail: 'Lowest revenue - investigate causes',
                    action: () => setFilter('store', worstStore[0])
                }});
            }}

            // Hot products
            const hotProducts = filteredData.filter(d => d.product_trend === 'hot');
            if (hotProducts.length > 0) {{
                const hotRevenue = hotProducts.reduce((sum, d) => sum + d.total_revenue, 0);
                insights.push({{
                    type: 'positive',
                    icon: '🔥',
                    title: 'Hot Products Revenue',
                    value: '$' + formatNumber(hotRevenue),
                    detail: `${{[...new Set(hotProducts.map(d => d.product_name))].length}} trending products`,
                    action: () => setFilter('trend', 'hot')
                }});
            }}

            // Low stock alert
            const latestStock = {{}};
            filteredData.sort((a, b) => a.date.localeCompare(b.date)).forEach(d => {{
                latestStock[d.product_name] = d.stock_level;
            }});
            const lowStockItems = Object.entries(latestStock).filter(([_, stock]) => stock < 50);
            if (lowStockItems.length > 0) {{
                insights.push({{
                    type: 'negative',
                    icon: '📦',
                    title: 'Low Stock Alert',
                    value: lowStockItems.length + ' products',
                    detail: 'Items need restocking soon',
                    action: null
                }});
            }}

            // Render insights
            const container = document.getElementById('insightsRow');
            container.innerHTML = insights.map(insight => `
                <div class="insight-card ${{insight.type}}" ${{insight.action ? 'onclick="' + insight.action.toString().slice(6) + '"' : ''}} style="${{insight.action ? 'cursor: pointer;' : ''}}">
                    <div class="insight-icon">${{insight.icon}}</div>
                    <h4>${{insight.title}}</h4>
                    <div class="insight-value">${{insight.value}}</div>
                    <p>${{insight.detail}}</p>
                </div>
            `).join('');
        }}

        // ================================================================
        // CHARTS
        // ================================================================
        function updateTrendChart() {{
            const dailyRevenue = {{}};
            filteredData.forEach(d => {{
                dailyRevenue[d.date] = (dailyRevenue[d.date] || 0) + d.total_revenue;
            }});

            const dates = Object.keys(dailyRevenue).sort();
            const revenues = dates.map(d => dailyRevenue[d]);

            // Calculate 7-day moving average
            const movingAvg = revenues.map((_, i, arr) => {{
                const start = Math.max(0, i - 6);
                const slice = arr.slice(start, i + 1);
                return slice.reduce((a, b) => a + b, 0) / slice.length;
            }});

            const traces = [
                {{
                    x: dates,
                    y: revenues,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Daily Revenue',
                    fill: 'tozeroy',
                    fillcolor: 'rgba(102, 126, 234, 0.1)',
                    line: {{ color: colors.primary, width: 2 }},
                    hovertemplate: '<b>%{{x}}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>'
                }},
                {{
                    x: dates,
                    y: movingAvg,
                    type: 'scatter',
                    mode: 'lines',
                    name: '7-Day Average',
                    line: {{ color: colors.danger, width: 2, dash: 'dot' }},
                    hovertemplate: '<b>%{{x}}</b><br>7-Day Avg: $%{{y:,.0f}}<extra></extra>'
                }}
            ];

            const layout = {{
                margin: {{ t: 20, r: 30, b: 50, l: 70 }},
                xaxis: {{ gridcolor: '#f0f0f0', tickangle: -45 }},
                yaxis: {{ gridcolor: '#f0f0f0', tickprefix: '$', tickformat: ',.0f' }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white',
                showlegend: true,
                legend: {{ x: 0, y: 1.1, orientation: 'h' }},
                hovermode: 'x unified'
            }};

            Plotly.newPlot('trendChart', traces, layout, {{ responsive: true }});

            // Add click handler
            document.getElementById('trendChart').on('plotly_click', function(data) {{
                const clickedDate = data.points[0].x;
                const month = clickedDate.substring(0, 7);
                setFilter('month', month);
            }});
        }}

        function updateCategoryChart() {{
            const categoryRevenue = {{}};
            filteredData.forEach(d => {{
                categoryRevenue[d.category] = (categoryRevenue[d.category] || 0) + d.total_revenue;
            }});

            const sorted = Object.entries(categoryRevenue).sort((a, b) => b[1] - a[1]);

            const trace = {{
                labels: sorted.map(d => d[0]),
                values: sorted.map(d => d[1]),
                type: 'pie',
                hole: 0.45,
                marker: {{ colors: colors.chart }},
                textinfo: 'label+percent',
                textposition: 'outside',
                hovertemplate: '<b>%{{label}}</b><br>Revenue: $%{{value:,.0f}}<br>%{{percent}}<extra></extra>'
            }};

            const layout = {{
                margin: {{ t: 20, r: 20, b: 20, l: 20 }},
                paper_bgcolor: 'white',
                showlegend: false,
                annotations: [{{
                    text: '$' + formatNumber(sorted.reduce((sum, d) => sum + d[1], 0)),
                    x: 0.5, y: 0.5,
                    font: {{ size: 18, weight: 'bold' }},
                    showarrow: false
                }}]
            }};

            Plotly.newPlot('categoryChart', [trace], layout, {{ responsive: true }});

            // Add click handler
            document.getElementById('categoryChart').on('plotly_click', function(data) {{
                const category = data.points[0].label;
                setFilter('category', category);
            }});
        }}

        function updateStoreChart() {{
            const storeRevenue = {{}};
            filteredData.forEach(d => {{
                storeRevenue[d.store] = (storeRevenue[d.store] || 0) + d.total_revenue;
            }});

            const sorted = Object.entries(storeRevenue).sort((a, b) => b[1] - a[1]);

            const trace = {{
                x: sorted.map(d => d[0]),
                y: sorted.map(d => d[1]),
                type: 'bar',
                marker: {{
                    color: sorted.map((d, i) => {{
                        if (d[0] === 'Outlet Store') return colors.warning;
                        if (i === 0) return colors.success;
                        return colors.primary;
                    }}),
                    line: {{ color: 'white', width: 1 }}
                }},
                hovertemplate: '<b>%{{x}}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>'
            }};

            const layout = {{
                margin: {{ t: 20, r: 20, b: 100, l: 70 }},
                xaxis: {{ tickangle: -45 }},
                yaxis: {{ gridcolor: '#f0f0f0', tickprefix: '$', tickformat: ',.0f' }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white'
            }};

            Plotly.newPlot('storeChart', [trace], layout, {{ responsive: true }});

            // Add click handler
            document.getElementById('storeChart').on('plotly_click', function(data) {{
                const store = data.points[0].x;
                setFilter('store', store);
            }});
        }}

        function updateProductsChart() {{
            const productRevenue = {{}};
            filteredData.forEach(d => {{
                productRevenue[d.product_name] = (productRevenue[d.product_name] || 0) + d.total_revenue;
            }});

            const sorted = Object.entries(productRevenue)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);

            const trace = {{
                y: sorted.map(d => d[0]).reverse(),
                x: sorted.map(d => d[1]).reverse(),
                type: 'bar',
                orientation: 'h',
                marker: {{
                    color: colors.primary,
                    line: {{ color: 'white', width: 1 }}
                }},
                hovertemplate: '<b>%{{y}}</b><br>Revenue: $%{{x:,.0f}}<extra></extra>'
            }};

            const layout = {{
                margin: {{ t: 20, r: 30, b: 50, l: 180 }},
                xaxis: {{ gridcolor: '#f0f0f0', tickprefix: '$', tickformat: ',.0f' }},
                yaxis: {{ }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white'
            }};

            Plotly.newPlot('productsChart', [trace], layout, {{ responsive: true }});
        }}

        function updateDOWChart() {{
            const dowRevenue = {{}};
            const dowOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            dowOrder.forEach(d => dowRevenue[d] = 0);
            filteredData.forEach(d => {{
                dowRevenue[d.day_of_week] = (dowRevenue[d.day_of_week] || 0) + d.total_revenue;
            }});

            const trace = {{
                x: dowOrder,
                y: dowOrder.map(d => dowRevenue[d]),
                type: 'bar',
                marker: {{
                    color: dowOrder.map(d =>
                        d === 'Saturday' || d === 'Sunday' ? colors.success : colors.primary
                    ),
                    line: {{ color: 'white', width: 1 }}
                }},
                hovertemplate: '<b>%{{x}}</b><br>Revenue: $%{{y:,.0f}}<extra></extra>'
            }};

            const layout = {{
                margin: {{ t: 20, r: 20, b: 50, l: 70 }},
                xaxis: {{ }},
                yaxis: {{ gridcolor: '#f0f0f0', tickprefix: '$', tickformat: ',.0f' }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white'
            }};

            Plotly.newPlot('dowChart', [trace], layout, {{ responsive: true }});
        }}

        // ================================================================
        // TABLE FUNCTIONS
        // ================================================================
        function updateProductTable() {{
            const productStats = {{}};

            filteredData.forEach(d => {{
                if (!productStats[d.product_name]) {{
                    productStats[d.product_name] = {{
                        name: d.product_name,
                        category: d.category,
                        revenue: 0,
                        units: 0,
                        priceSum: 0,
                        priceCount: 0,
                        stock: d.stock_level,
                        trend: d.product_trend
                    }};
                }}
                productStats[d.product_name].revenue += d.total_revenue;
                productStats[d.product_name].units += d.quantity;
                productStats[d.product_name].priceSum += d.unit_price;
                productStats[d.product_name].priceCount++;
                productStats[d.product_name].stock = d.stock_level; // Latest stock
            }});

            const sorted = Object.values(productStats).sort((a, b) => b.revenue - a.revenue);

            const tbody = document.getElementById('productTableBody');
            tbody.innerHTML = sorted.map(p => `
                <tr class="clickable" onclick="setFilter('category', '${{p.category}}')">
                    <td><strong>${{p.name}}</strong></td>
                    <td>${{p.category}}</td>
                    <td>$${{formatNumber(p.revenue)}}</td>
                    <td>${{formatNumber(p.units)}}</td>
                    <td>$${{(p.priceSum / p.priceCount).toFixed(2)}}</td>
                    <td><span class="stock-badge ${{p.stock < 30 ? 'critical' : p.stock < 80 ? 'low' : 'ok'}}">${{p.stock}} units</span></td>
                    <td><span class="trend-badge ${{p.trend}}">${{p.trend}}</span></td>
                </tr>
            `).join('');
        }}

        function filterTable() {{
            const search = document.getElementById('tableSearch').value.toLowerCase();
            const rows = document.querySelectorAll('#productTableBody tr');
            rows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(search) ? '' : 'none';
            }});
        }}

        let sortColumn = -1;
        let sortAsc = true;

        function sortTable(columnIndex) {{
            const tbody = document.getElementById('productTableBody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            // Toggle direction if same column
            if (sortColumn === columnIndex) {{
                sortAsc = !sortAsc;
            }} else {{
                sortColumn = columnIndex;
                sortAsc = true;
            }}

            // Update header styling
            document.querySelectorAll('.data-table th').forEach((th, i) => {{
                th.classList.remove('sorted-asc', 'sorted-desc');
                if (i === columnIndex) {{
                    th.classList.add(sortAsc ? 'sorted-asc' : 'sorted-desc');
                }}
            }});

            rows.sort((a, b) => {{
                let aVal = a.cells[columnIndex].textContent;
                let bVal = b.cells[columnIndex].textContent;

                // Handle numeric values
                if (columnIndex === 2 || columnIndex === 4) {{ // Revenue, Avg Price
                    aVal = parseFloat(aVal.replace(/[$,]/g, ''));
                    bVal = parseFloat(bVal.replace(/[$,]/g, ''));
                }} else if (columnIndex === 3 || columnIndex === 5) {{ // Units, Stock
                    aVal = parseInt(aVal.replace(/[, units]/g, ''));
                    bVal = parseInt(bVal.replace(/[, units]/g, ''));
                }}

                if (aVal < bVal) return sortAsc ? -1 : 1;
                if (aVal > bVal) return sortAsc ? 1 : -1;
                return 0;
            }});

            rows.forEach(row => tbody.appendChild(row));
        }}

        // ================================================================
        // UTILITY FUNCTIONS
        // ================================================================
        function formatNumber(num) {{
            if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toFixed(0);
        }}
    </script>
</body>
</html>'''

    return html_content


# ============================================================================
# LEAD CONVERSION DASHBOARD - FULLY INTERACTIVE
# ============================================================================

def create_lead_dashboard(df):
    """Create an interactive lead conversion dashboard."""
    print("Creating Interactive Lead Conversion Dashboard...")

    # Prepare data
    data_json = df.to_json(orient='records')

    # Get unique values
    sources = sorted(df['source'].unique().tolist())
    stages = ['Lead', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    reps = sorted(df['sales_rep'].unique().tolist())
    industries = sorted(df['industry'].unique().tolist())
    months = sorted(df['lead_month'].unique().tolist())

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lead Conversion Dashboard | Marketing Analytics</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            background: #f0f2f5;
            color: #1a1a2e;
            line-height: 1.6;
        }}

        .nav {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}

        .nav a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            transition: color 0.2s;
        }}

        .nav a:hover {{ color: white; }}

        .nav h1 {{
            color: white;
            font-size: 20px;
            font-weight: 600;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
        }}

        .context-banner {{
            background: linear-gradient(135deg, #27ae60 0%, #1abc9c 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 16px;
            margin-bottom: 25px;
            position: relative;
        }}

        .context-banner h2 {{
            font-size: 22px;
            margin-bottom: 10px;
        }}

        .context-banner p {{
            font-size: 14px;
            opacity: 0.95;
            max-width: 700px;
        }}

        .context-banner .data-period {{
            position: absolute;
            top: 25px;
            right: 30px;
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
        }}

        .filter-panel {{
            background: white;
            padding: 20px 25px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: flex-end;
        }}

        .filter-group {{
            flex: 1;
            min-width: 160px;
        }}

        .filter-group label {{
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .filter-group select {{
            width: 100%;
            padding: 10px 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: border-color 0.2s;
        }}

        .filter-group select:focus {{
            outline: none;
            border-color: #27ae60;
        }}

        .btn-reset {{
            padding: 10px 20px;
            background: #f0f2f5;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btn-reset:hover {{
            background: #e74c3c;
            border-color: #e74c3c;
            color: white;
        }}

        .active-filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}

        .filter-tag {{
            background: #27ae60;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .filter-tag .remove {{
            cursor: pointer;
            opacity: 0.85;
        }}

        .filter-tag .remove:hover {{
            opacity: 1;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .kpi-card {{
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            position: relative;
            transition: transform 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-3px);
        }}

        .kpi-card .icon {{
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 28px;
        }}

        .kpi-card .label {{
            font-size: 12px;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .kpi-card .value {{
            font-size: 28px;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 5px;
        }}

        .kpi-card .trend {{
            font-size: 13px;
        }}

        .kpi-card .trend.up {{ color: #27ae60; }}
        .kpi-card .trend.down {{ color: #e74c3c; }}

        .insights-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }}

        .insight-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .insight-card:hover {{
            transform: translateX(5px);
        }}

        .insight-card.positive {{ border-color: #27ae60; }}
        .insight-card.warning {{ border-color: #f39c12; }}
        .insight-card.negative {{ border-color: #e74c3c; }}
        .insight-card.info {{ border-color: #3498db; }}

        .insight-card h4 {{
            font-size: 13px;
            color: #666;
            margin-bottom: 5px;
        }}

        .insight-card .insight-value {{
            font-size: 18px;
            font-weight: 700;
            color: #1a1a2e;
        }}

        .insight-card p {{
            font-size: 12px;
            color: #888;
            margin-top: 5px;
        }}

        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 25px;
        }}

        .chart-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .chart-card.full-width {{
            grid-column: 1 / -1;
        }}

        .chart-card h3 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .chart-card .chart-subtitle {{
            font-size: 13px;
            color: #888;
            margin-bottom: 20px;
        }}

        .data-table-container {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 25px;
        }}

        .data-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .data-table th {{
            background: #f8f9fa;
            padding: 14px 16px;
            text-align: left;
            font-size: 12px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            border-bottom: 2px solid #e0e0e0;
            cursor: pointer;
        }}

        .data-table th:hover {{ background: #e8e9ea; }}

        .data-table td {{
            padding: 14px 16px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }}

        .data-table tr:hover {{ background: #f8f9fa; }}

        .stage-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 500;
        }}

        .stage-badge.lead {{ background: #e8f0fe; color: #2980b9; }}
        .stage-badge.contacted {{ background: #fef3e2; color: #d68910; }}
        .stage-badge.qualified {{ background: #e8f6ef; color: #27ae60; }}
        .stage-badge.proposal {{ background: #f5eef8; color: #8e44ad; }}
        .stage-badge.negotiation {{ background: #fdebd0; color: #e67e22; }}
        .stage-badge.won {{ background: #d4efdf; color: #1e8449; }}
        .stage-badge.lost {{ background: #fadbd8; color: #c0392b; }}

        .footer {{
            text-align: center;
            padding: 30px;
            color: #888;
            font-size: 13px;
        }}

        .footer a {{
            color: #27ae60;
            text-decoration: none;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}

        .value-updated {{
            animation: pulse 0.3s ease;
        }}

        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .filter-group {{ min-width: 100%; }}
            .chart-row {{ grid-template-columns: 1fr; }}
            .context-banner .data-period {{ position: static; margin-top: 15px; display: inline-block; }}
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <a href="index.html">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back to Portfolio
        </a>
        <h1>Lead Conversion Dashboard</h1>
        <div style="width: 120px;"></div>
    </nav>

    <div class="container">
        <div class="context-banner">
            <span class="data-period" id="dataPeriod">Loading...</span>
            <h2>Marketing Funnel & Sales Performance</h2>
            <p>This dashboard summarizes lead flow, pipeline value, and conversion outcomes across sources,
            industries, and reps. It’s built to surface the quality‑vs‑volume tradeoff in a clear, explainable way.</p>
            <p><strong>How to use:</strong> Use the filters or click chart elements to cross‑filter the view.</p>
        </div>

        <div class="filter-panel">
            <div class="filter-group">
                <label>Lead Source</label>
                <select id="filterSource">
                    <option value="all">All Sources</option>
                    {' '.join([f'<option value="{s}">{s}</option>' for s in sources])}
                </select>
            </div>
            <div class="filter-group">
                <label>Stage</label>
                <select id="filterStage">
                    <option value="all">All Stages</option>
                    {' '.join([f'<option value="{s}">{s}</option>' for s in stages])}
                </select>
            </div>
            <div class="filter-group">
                <label>Sales Rep</label>
                <select id="filterRep">
                    <option value="all">All Reps</option>
                    {' '.join([f'<option value="{r}">{r}</option>' for r in reps])}
                </select>
            </div>
            <div class="filter-group">
                <label>Industry</label>
                <select id="filterIndustry">
                    <option value="all">All Industries</option>
                    {' '.join([f'<option value="{i}">{i}</option>' for i in industries])}
                </select>
            </div>
            <div class="filter-group">
                <label>Month</label>
                <select id="filterMonth">
                    <option value="all">All Months</option>
                    {' '.join([f'<option value="{m}">{m}</option>' for m in months])}
                </select>
            </div>
            <button class="btn-reset" onclick="resetFilters()">Reset Filters</button>
        </div>
        <div class="active-filters" id="activeFilters"></div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <span class="icon">👥</span>
                <div class="label">Total Leads</div>
                <div class="value" id="kpiLeads">0</div>
                <div class="trend" id="kpiLeadsTrend">Loading...</div>
            </div>
            <div class="kpi-card">
                <span class="icon">💰</span>
                <div class="label">Pipeline Value</div>
                <div class="value" id="kpiPipeline">$0</div>
                <div class="trend" id="kpiPipelineTrend">Loading...</div>
            </div>
            <div class="kpi-card">
                <span class="icon">📈</span>
                <div class="label">Conversion Rate</div>
                <div class="value" id="kpiConversion">0%</div>
                <div class="trend" id="kpiConversionTrend">Loading...</div>
            </div>
            <div class="kpi-card">
                <span class="icon">🏆</span>
                <div class="label">Closed Won Value</div>
                <div class="value" id="kpiWon">$0</div>
                <div class="trend" id="kpiWonTrend">Loading...</div>
            </div>
            <div class="kpi-card">
                <span class="icon">⏱️</span>
                <div class="label">Avg Days in Pipeline</div>
                <div class="value" id="kpiDays">0</div>
                <div class="trend" id="kpiDaysTrend">Loading...</div>
            </div>
            <div class="kpi-card">
                <span class="icon">💵</span>
                <div class="label">Avg Deal Size</div>
                <div class="value" id="kpiDealSize">$0</div>
                <div class="trend" id="kpiDealSizeTrend">Loading...</div>
            </div>
        </div>

        <div class="insights-row" id="insightsRow"></div>

        <div class="chart-row">
            <div class="chart-card full-width">
                <h3>Sales Funnel</h3>
                <div class="chart-subtitle">Click any stage to filter - watch how numbers change as leads progress</div>
                <div id="funnelChart" style="height: 350px;"></div>
            </div>
        </div>

        <div class="chart-row">
            <div class="chart-card">
                <h3>Lead Source Performance</h3>
                <div class="chart-subtitle">Compare volume vs quality - click to filter by source</div>
                <div id="sourceChart" style="height: 320px;"></div>
            </div>
            <div class="chart-card">
                <h3>Conversion Rate by Source</h3>
                <div class="chart-subtitle">Which channels convert best?</div>
                <div id="conversionChart" style="height: 320px;"></div>
            </div>
        </div>

        <div class="chart-row">
            <div class="chart-card">
                <h3>Sales Rep Performance</h3>
                <div class="chart-subtitle">Pipeline value by rep - identify top performers</div>
                <div id="repChart" style="height: 320px;"></div>
            </div>
            <div class="chart-card">
                <h3>Lead Trend Over Time</h3>
                <div class="chart-subtitle">New leads and pipeline value by month</div>
                <div id="trendChart" style="height: 320px;"></div>
            </div>
        </div>

        <div class="data-table-container">
            <h3 style="margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
                Lead Details
                <input type="text" placeholder="Search leads..." id="tableSearch" oninput="filterTable()"
                       style="padding: 8px 14px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 13px; width: 250px;">
            </h3>
            <div style="overflow-x: auto;">
                <table class="data-table" id="leadTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">Company</th>
                            <th onclick="sortTable(1)">Contact</th>
                            <th onclick="sortTable(2)">Source</th>
                            <th onclick="sortTable(3)">Stage</th>
                            <th onclick="sortTable(4)">Deal Value</th>
                            <th onclick="sortTable(5)">Expected Value</th>
                            <th onclick="sortTable(6)">Sales Rep</th>
                            <th onclick="sortTable(7)">Days in Pipeline</th>
                        </tr>
                    </thead>
                    <tbody id="leadTableBody"></tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Interactive Marketing Analytics Dashboard | Built with Plotly.js</p>
            <p style="margin-top: 8px;"><a href="index.html">Back to Portfolio</a></p>
        </div>
    </div>

    <script>
        const rawData = {data_json};
        let filteredData = [...rawData];
        let currentFilters = {{
            source: 'all',
            stage: 'all',
            rep: 'all',
            industry: 'all',
            month: 'all'
        }};

        const colors = {{
            primary: '#27ae60',
            secondary: '#1abc9c',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#3498db',
            chart: ['#3498db', '#27ae60', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#e67e22']
        }};

        const stageOrder = ['Lead', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'];
        const stageColors = ['#3498db', '#f39c12', '#27ae60', '#9b59b6', '#e67e22', '#1abc9c', '#e74c3c'];

        document.addEventListener('DOMContentLoaded', function() {{
            const dates = rawData.map(d => d.lead_date).sort();
            document.getElementById('dataPeriod').textContent =
                `${{dates[0]}} to ${{dates[dates.length-1]}}`;

            ['Source', 'Stage', 'Rep', 'Industry', 'Month'].forEach(filter => {{
                document.getElementById('filter' + filter).addEventListener('change', applyFilters);
            }});

            updateDashboard();
        }});

        function applyFilters() {{
            currentFilters.source = document.getElementById('filterSource').value;
            currentFilters.stage = document.getElementById('filterStage').value;
            currentFilters.rep = document.getElementById('filterRep').value;
            currentFilters.industry = document.getElementById('filterIndustry').value;
            currentFilters.month = document.getElementById('filterMonth').value;

            filteredData = rawData.filter(d => {{
                if (currentFilters.source !== 'all' && d.source !== currentFilters.source) return false;
                if (currentFilters.stage !== 'all' && d.stage !== currentFilters.stage) return false;
                if (currentFilters.rep !== 'all' && d.sales_rep !== currentFilters.rep) return false;
                if (currentFilters.industry !== 'all' && d.industry !== currentFilters.industry) return false;
                if (currentFilters.month !== 'all' && d.lead_month !== currentFilters.month) return false;
                return true;
            }});

            updateDashboard();
        }}

        function resetFilters() {{
            ['Source', 'Stage', 'Rep', 'Industry', 'Month'].forEach(f => {{
                document.getElementById('filter' + f).value = 'all';
            }});
            currentFilters = {{ source: 'all', stage: 'all', rep: 'all', industry: 'all', month: 'all' }};
            filteredData = [...rawData];
            updateDashboard();
        }}

        function setFilter(type, value) {{
            const filterMap = {{ source: 'Source', stage: 'Stage', sales_rep: 'Rep', industry: 'Industry' }};
            document.getElementById('filter' + filterMap[type]).value = value;
            applyFilters();
        }}

        function updateDashboard() {{
            updateActiveFilters();
            updateKPIs();
            updateInsights();
            updateFunnelChart();
            updateSourceChart();
            updateConversionChart();
            updateRepChart();
            updateTrendChart();
            updateLeadTable();
        }}

        function updateActiveFilters() {{
            const filters = [
                {{ key: 'source', label: 'Source' }},
                {{ key: 'stage', label: 'Stage' }},
                {{ key: 'rep', label: 'Rep' }},
                {{ key: 'industry', label: 'Industry' }},
                {{ key: 'month', label: 'Month' }}
            ];
            const tags = filters
                .filter(f => currentFilters[f.key] !== 'all')
                .map(f => `
                    <span class="filter-tag">
                        ${{f.label}}: ${{currentFilters[f.key]}}
                        <span class="remove" onclick="clearFilter('${{f.key}}')">×</span>
                    </span>
                `);
            document.getElementById('activeFilters').innerHTML = tags.join('');
        }}

        function clearFilter(key) {{
            const map = {{ source: 'Source', stage: 'Stage', rep: 'Rep', industry: 'Industry', month: 'Month' }};
            const id = 'filter' + map[key];
            document.getElementById(id).value = 'all';
            applyFilters();
        }}

        function updateKPIs() {{
            const totalLeads = filteredData.length;
            const pipeline = filteredData.reduce((sum, d) => sum + d.deal_value, 0);
            const closed = filteredData.filter(d => d.stage === 'Closed Won' || d.stage === 'Closed Lost');
            const won = filteredData.filter(d => d.stage === 'Closed Won');
            const conversionRate = closed.length > 0 ? (won.length / closed.length * 100) : 0;
            const wonValue = won.reduce((sum, d) => sum + d.deal_value, 0);
            const avgDays = filteredData.reduce((sum, d) => sum + d.days_in_pipeline, 0) / Math.max(totalLeads, 1);
            const avgDealSize = pipeline / Math.max(totalLeads, 1);

            animateValue('kpiLeads', formatNumber(totalLeads));
            animateValue('kpiPipeline', '$' + formatNumber(pipeline));
            animateValue('kpiConversion', conversionRate.toFixed(1) + '%');
            animateValue('kpiWon', '$' + formatNumber(wonValue));
            animateValue('kpiDays', avgDays.toFixed(0));
            animateValue('kpiDealSize', '$' + formatNumber(avgDealSize));

            document.getElementById('kpiLeadsTrend').innerHTML =
                `${{((totalLeads / rawData.length) * 100).toFixed(1)}}% of all leads`;
            document.getElementById('kpiConversionTrend').innerHTML =
                conversionRate > 20 ? '<span class="up">↑ Above target</span>' : '<span class="down">↓ Below target</span>';
        }}

        function animateValue(id, value) {{
            const el = document.getElementById(id);
            if (el.textContent !== value) {{
                el.textContent = value;
                el.classList.add('value-updated');
                setTimeout(() => el.classList.remove('value-updated'), 300);
            }}
        }}

        function updateInsights() {{
            const insights = [];

            // Best source
            const sourceConv = {{}};
            const sourceData = {{}};
            filteredData.forEach(d => {{
                if (!sourceData[d.source]) sourceData[d.source] = {{ total: 0, won: 0, closed: 0 }};
                sourceData[d.source].total++;
                if (d.stage === 'Closed Won') {{ sourceData[d.source].won++; sourceData[d.source].closed++; }}
                if (d.stage === 'Closed Lost') sourceData[d.source].closed++;
            }});

            Object.entries(sourceData).forEach(([source, data]) => {{
                if (data.closed > 0) sourceConv[source] = (data.won / data.closed * 100);
            }});

            const bestSource = Object.entries(sourceConv).sort((a, b) => b[1] - a[1])[0];
            if (bestSource) {{
                insights.push({{
                    type: 'positive',
                    title: 'Best Converting Source',
                    value: bestSource[0],
                    detail: `${{bestSource[1].toFixed(1)}}% conversion rate`,
                    action: `setFilter('source', '${{bestSource[0]}}')`
                }});
            }}

            // Top rep
            const repWon = {{}};
            filteredData.filter(d => d.stage === 'Closed Won').forEach(d => {{
                repWon[d.sales_rep] = (repWon[d.sales_rep] || 0) + d.deal_value;
            }});
            const topRep = Object.entries(repWon).sort((a, b) => b[1] - a[1])[0];
            if (topRep) {{
                insights.push({{
                    type: 'positive',
                    title: 'Top Performer',
                    value: topRep[0].split(' ')[0],
                    detail: `$${{formatNumber(topRep[1])}} closed`,
                    action: `setFilter('sales_rep', '${{topRep[0]}}')`
                }});
            }}

            // Stale leads warning
            const staleLeads = filteredData.filter(d =>
                d.days_in_pipeline > 60 && !['Closed Won', 'Closed Lost'].includes(d.stage)
            );
            if (staleLeads.length > 0) {{
                insights.push({{
                    type: 'warning',
                    title: 'Stale Leads',
                    value: staleLeads.length + ' leads',
                    detail: 'Over 60 days without closing',
                    action: null
                }});
            }}

            // Expected value
            const expectedValue = filteredData.reduce((sum, d) => sum + d.expected_value, 0);
            insights.push({{
                type: 'info',
                title: 'Expected Pipeline Value',
                value: '$' + formatNumber(expectedValue),
                detail: 'Weighted by stage probability',
                action: null
            }});

            document.getElementById('insightsRow').innerHTML = insights.map(i => `
                <div class="insight-card ${{i.type}}" ${{i.action ? `onclick="${{i.action}}"` : ''}} style="${{i.action ? 'cursor:pointer;' : ''}}">
                    <h4>${{i.title}}</h4>
                    <div class="insight-value">${{i.value}}</div>
                    <p>${{i.detail}}</p>
                </div>
            `).join('');
        }}

        function updateFunnelChart() {{
            const stageCounts = {{}};
            stageOrder.forEach(s => stageCounts[s] = 0);
            filteredData.forEach(d => stageCounts[d.stage]++);

            const trace = {{
                type: 'funnel',
                y: stageOrder,
                x: stageOrder.map(s => stageCounts[s]),
                textposition: 'inside',
                textinfo: 'value+percent initial',
                marker: {{ color: stageColors }},
                connector: {{ line: {{ color: '#f0f0f0', width: 2 }} }},
                hovertemplate: '<b>%{{y}}</b><br>Leads: %{{x}}<br>%{{percentInitial}} of total<extra></extra>'
            }};

            Plotly.newPlot('funnelChart', [trace], {{
                margin: {{ t: 20, r: 100, b: 20, l: 150 }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white'
            }}, {{ responsive: true }});

            document.getElementById('funnelChart').on('plotly_click', function(data) {{
                setFilter('stage', data.points[0].y);
            }});
        }}

        function updateSourceChart() {{
            const sourceData = {{}};
            filteredData.forEach(d => {{
                sourceData[d.source] = (sourceData[d.source] || 0) + d.deal_value;
            }});

            const sorted = Object.entries(sourceData).sort((a, b) => b[1] - a[1]);

            Plotly.newPlot('sourceChart', [{{
                labels: sorted.map(d => d[0]),
                values: sorted.map(d => d[1]),
                type: 'pie',
                hole: 0.4,
                marker: {{ colors: colors.chart }},
                textinfo: 'label+percent',
                hovertemplate: '<b>%{{label}}</b><br>Pipeline: $%{{value:,.0f}}<extra></extra>'
            }}], {{
                margin: {{ t: 20, r: 20, b: 20, l: 20 }},
                paper_bgcolor: 'white',
                showlegend: false
            }}, {{ responsive: true }});

            document.getElementById('sourceChart').on('plotly_click', function(data) {{
                setFilter('source', data.points[0].label);
            }});
        }}

        function updateConversionChart() {{
            const sourceConv = {{}};
            const sourceData = {{}};

            filteredData.forEach(d => {{
                if (!sourceData[d.source]) sourceData[d.source] = {{ won: 0, closed: 0 }};
                if (d.stage === 'Closed Won') {{ sourceData[d.source].won++; sourceData[d.source].closed++; }}
                if (d.stage === 'Closed Lost') sourceData[d.source].closed++;
            }});

            Object.entries(sourceData).forEach(([source, data]) => {{
                sourceConv[source] = data.closed > 0 ? (data.won / data.closed * 100) : 0;
            }});

            const sorted = Object.entries(sourceConv).sort((a, b) => b[1] - a[1]);

            Plotly.newPlot('conversionChart', [{{
                y: sorted.map(d => d[0]).reverse(),
                x: sorted.map(d => d[1]).reverse(),
                type: 'bar',
                orientation: 'h',
                marker: {{
                    color: sorted.map(d => d[1] > 30 ? colors.primary : d[1] > 15 ? colors.warning : colors.danger).reverse()
                }},
                text: sorted.map(d => d[1].toFixed(1) + '%').reverse(),
                textposition: 'outside',
                hovertemplate: '<b>%{{y}}</b><br>Conversion: %{{x:.1f}}%<extra></extra>'
            }}], {{
                margin: {{ t: 20, r: 60, b: 40, l: 120 }},
                xaxis: {{ title: 'Conversion Rate %', range: [0, Math.max(...sorted.map(d => d[1])) * 1.3] }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white'
            }}, {{ responsive: true }});
        }}

        function updateRepChart() {{
            const repData = {{}};
            filteredData.forEach(d => {{
                if (!repData[d.sales_rep]) repData[d.sales_rep] = {{ pipeline: 0, won: 0 }};
                repData[d.sales_rep].pipeline += d.deal_value;
                if (d.stage === 'Closed Won') repData[d.sales_rep].won += d.deal_value;
            }});

            const sorted = Object.entries(repData).sort((a, b) => b[1].pipeline - a[1].pipeline);

            Plotly.newPlot('repChart', [
                {{
                    x: sorted.map(d => d[0]),
                    y: sorted.map(d => d[1].pipeline),
                    name: 'Pipeline',
                    type: 'bar',
                    marker: {{ color: colors.info }},
                    hovertemplate: '<b>%{{x}}</b><br>Pipeline: $%{{y:,.0f}}<extra></extra>'
                }},
                {{
                    x: sorted.map(d => d[0]),
                    y: sorted.map(d => d[1].won),
                    name: 'Won',
                    type: 'bar',
                    marker: {{ color: colors.primary }},
                    hovertemplate: '<b>%{{x}}</b><br>Won: $%{{y:,.0f}}<extra></extra>'
                }}
            ], {{
                margin: {{ t: 20, r: 20, b: 100, l: 70 }},
                barmode: 'group',
                xaxis: {{ tickangle: -45 }},
                yaxis: {{ tickprefix: '$', tickformat: ',.0f' }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white',
                legend: {{ x: 0, y: 1.1, orientation: 'h' }}
            }}, {{ responsive: true }});

            document.getElementById('repChart').on('plotly_click', function(data) {{
                setFilter('sales_rep', data.points[0].x);
            }});
        }}

        function updateTrendChart() {{
            const monthData = {{}};
            filteredData.forEach(d => {{
                if (!monthData[d.lead_month]) monthData[d.lead_month] = {{ leads: 0, pipeline: 0 }};
                monthData[d.lead_month].leads++;
                monthData[d.lead_month].pipeline += d.deal_value;
            }});

            const months = Object.keys(monthData).sort();

            Plotly.newPlot('trendChart', [
                {{
                    x: months,
                    y: months.map(m => monthData[m].leads),
                    name: 'New Leads',
                    type: 'bar',
                    marker: {{ color: colors.info }},
                    yaxis: 'y'
                }},
                {{
                    x: months,
                    y: months.map(m => monthData[m].pipeline),
                    name: 'Pipeline Value',
                    type: 'scatter',
                    mode: 'lines+markers',
                    line: {{ color: colors.primary, width: 3 }},
                    yaxis: 'y2'
                }}
            ], {{
                margin: {{ t: 20, r: 70, b: 50, l: 60 }},
                yaxis: {{ title: 'Leads' }},
                yaxis2: {{ title: 'Pipeline ($)', overlaying: 'y', side: 'right', tickprefix: '$', tickformat: ',.0f' }},
                paper_bgcolor: 'white',
                plot_bgcolor: 'white',
                legend: {{ x: 0, y: 1.15, orientation: 'h' }},
                hovermode: 'x unified'
            }}, {{ responsive: true }});
        }}

        function updateLeadTable() {{
            const sorted = [...filteredData].sort((a, b) => b.deal_value - a.deal_value).slice(0, 50);

            document.getElementById('leadTableBody').innerHTML = sorted.map(lead => {{
                const stageClass = lead.stage.toLowerCase().replace(' ', '');
                return `
                    <tr onclick="setFilter('source', '${{lead.source}}')" style="cursor: pointer;">
                        <td><strong>${{lead.company}}</strong></td>
                        <td>${{lead.full_name}}</td>
                        <td>${{lead.source}}</td>
                        <td><span class="stage-badge ${{stageClass}}">${{lead.stage}}</span></td>
                        <td>$${{formatNumber(lead.deal_value)}}</td>
                        <td>$${{formatNumber(lead.expected_value)}}</td>
                        <td>${{lead.sales_rep}}</td>
                        <td>${{lead.days_in_pipeline}} days</td>
                    </tr>
                `;
            }}).join('');
        }}

        function filterTable() {{
            const search = document.getElementById('tableSearch').value.toLowerCase();
            document.querySelectorAll('#leadTableBody tr').forEach(row => {{
                row.style.display = row.textContent.toLowerCase().includes(search) ? '' : 'none';
            }});
        }}

        let sortCol = -1, sortAsc = true;
        function sortTable(col) {{
            if (sortCol === col) sortAsc = !sortAsc;
            else {{ sortCol = col; sortAsc = true; }}

            const rows = Array.from(document.querySelectorAll('#leadTableBody tr'));
            rows.sort((a, b) => {{
                let aVal = a.cells[col].textContent;
                let bVal = b.cells[col].textContent;
                if ([4, 5].includes(col)) {{
                    aVal = parseFloat(aVal.replace(/[$,K]/g, '')) || 0;
                    bVal = parseFloat(bVal.replace(/[$,K]/g, '')) || 0;
                }}
                if (col === 7) {{
                    aVal = parseInt(aVal); bVal = parseInt(bVal);
                }}
                return sortAsc ? (aVal > bVal ? 1 : -1) : (aVal < bVal ? 1 : -1);
            }});
            rows.forEach(r => document.getElementById('leadTableBody').appendChild(r));
        }}

        function formatNumber(num) {{
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(0) + 'K';
            return Math.round(num).toLocaleString();
        }}
    </script>
</body>
</html>'''

    return html_content


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*60)
    print("CREATING INTERACTIVE DASHBOARDS")
    print("="*60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    dashboards_dir = os.path.join(script_dir, 'dashboards')
    os.makedirs(dashboards_dir, exist_ok=True)

    # Load data
    retail_path = os.path.join(data_dir, 'retail_sales_cleaned.csv')
    leads_path = os.path.join(data_dir, 'marketing_leads_cleaned.csv')

    if not os.path.exists(retail_path) or not os.path.exists(leads_path):
        print("ERROR: Data files not found. Run 'python generate_data.py' first.")
        return

    retail_df = pd.read_csv(retail_path)
    leads_df = pd.read_csv(leads_path)

    print(f"Loaded {len(retail_df):,} retail transactions")
    print(f"Loaded {len(leads_df):,} marketing leads")

    # Create dashboards
    retail_html = create_retail_dashboard(retail_df)
    lead_html = create_lead_dashboard(leads_df)

    # Save
    with open(os.path.join(dashboards_dir, 'retail-inventory.html'), 'w', encoding='utf-8') as f:
        f.write(retail_html)
    print(f"\nSaved: dashboards/retail-inventory.html")

    with open(os.path.join(dashboards_dir, 'lead-conversion.html'), 'w', encoding='utf-8') as f:
        f.write(lead_html)
    print(f"Saved: dashboards/lead-conversion.html")

    print("\n" + "="*60)
    print("INTERACTIVE DASHBOARDS CREATED!")
    print("="*60)
    print("\nFeatures:")
    print("- Real-time filtering with instant updates")
    print("- Click any chart element to filter the dashboard")
    print("- Dynamic KPIs that update based on filters")
    print("- Smart insights that highlight important findings")
    print("- Sortable, searchable data tables")
    print("- Engaging tooltips and hover effects")
    print("\nOpen index.html in your browser to explore!")

if __name__ == "__main__":
    main()
