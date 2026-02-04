# Business Analytics Portfolio

A professional portfolio showcasing interactive business intelligence dashboards built with Python and Plotly.

## Live Demo

[View Live Demo](https://YOUR-USERNAME.github.io/business-analytics-portfolio/)

## Project Overview

This portfolio contains two comprehensive business analytics dashboards:

### 1. Retail Inventory Dashboard
Comprehensive analysis of retail sales performance with:
- Revenue trends and KPI tracking
- Category and store performance breakdown
- Top-selling products analysis
- Day-of-week sales patterns
- Low stock alerts and inventory monitoring

### 2. Lead Conversion Dashboard
Marketing funnel analysis and lead conversion metrics featuring:
- Interactive sales funnel visualization
- Lead source performance analysis
- Pipeline value and ROI metrics
- Sales rep performance tracking
- Conversion rate analysis

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.x | Data generation and processing |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computations |
| Plotly | Interactive visualizations |
| HTML5 | Dashboard structure |
| CSS3 | Responsive styling |
| JavaScript | Chart interactivity |

## Data Cleaning Steps

### Retail Sales Data Cleaning
The data generation script (`generate_data.py`) performs the following cleaning operations:

1. **Remove Duplicates** - Eliminated exact duplicate transaction records
2. **Standardize Dates** - Converted all date formats to YYYY-MM-DD
3. **Handle Missing Product Names** - Filled with "Unknown Product"
4. **Handle Missing Categories** - Used mode imputation
5. **Fix Negative Quantities** - Converted to absolute values
6. **Cap Outlier Prices** - Limited to 99th percentile
7. **Calculate Derived Metrics** - Added total_revenue, month, day_of_week

### Marketing Lead Data Cleaning

1. **Validate Email Formats** - Removed records with invalid emails
2. **Fix Date Inconsistencies** - Ensured contact_date >= lead_date
3. **Handle Missing Sources** - Marked as "Direct"
4. **Remove Incomplete Records** - Dropped records missing critical fields
5. **Standardize Status Values** - Converted to Title Case
6. **Calculate Derived Metrics** - Added days_to_convert, expected_value

## Key Insights

### Retail Dashboard Insights
- **Revenue Distribution**: Electronics and Home & Kitchen categories drive the highest revenue
- **Store Performance**: Identified top-performing store locations
- **Sales Patterns**: Weekend days show distinct purchasing patterns
- **Inventory Alerts**: Real-time monitoring of low-stock items

### Lead Conversion Insights
- **Funnel Analysis**: Clear visualization of lead progression through stages
- **Source ROI**: Comparison of marketing channel effectiveness
- **Pipeline Value**: Weighted expected value calculations
- **Team Performance**: Individual sales rep contribution tracking

## Project Structure

```
business-analytics-portfolio/
├── data/
│   ├── retail_sales_cleaned.csv
│   └── marketing_leads_cleaned.csv
├── dashboards/
│   ├── retail-inventory.html
│   └── lead-conversion.html
├── assets/
├── index.html
├── generate_data.py
├── create_dashboards.py
└── README.md
```

## How to Run Locally

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/business-analytics-portfolio.git
   cd business-analytics-portfolio
   ```

2. **Install required Python libraries**
   ```bash
   pip install pandas numpy plotly
   ```

3. **Generate the data**
   ```bash
   python generate_data.py
   ```
   This creates cleaned CSV files in the `data/` folder.

4. **Create the dashboards**
   ```bash
   python create_dashboards.py
   ```
   This generates interactive HTML dashboards in the `dashboards/` folder.

5. **View the portfolio**
   Open `index.html` in your web browser, or use a local server:
   ```bash
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000`

## Dashboard Features

- **Interactive Charts**: Hover, zoom, and filter capabilities
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time KPIs**: Key performance indicators at a glance
- **Data Tables**: Detailed breakdowns with sorting
- **Insights Cards**: Highlighted key findings

## Color Palette

The dashboards use a professional business color scheme:

| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary | #2C3E50 | Headers, text |
| Secondary | #3498DB | Charts, accents |
| Accent | #1ABC9C | Highlights |
| Success | #27AE60 | Positive metrics |
| Warning | #F39C12 | Alerts |
| Danger | #E74C3C | Critical items |

## Customization

### Modifying Data Parameters
Edit `generate_data.py` to adjust:
- Date range (currently 6 months)
- Number of transactions (currently 2000)
- Number of leads (currently 500)
- Product categories and items
- Price ranges

### Styling Changes
Dashboard styles are embedded in the HTML files. Key CSS classes:
- `.kpi-card` - KPI card styling
- `.chart-section` - Chart container styling
- `.data-table` - Table styling
- `.insight-card` - Insight card styling

## Deployment to GitHub Pages

1. Push your code to GitHub
2. Go to repository Settings > Pages
3. Select "Deploy from a branch"
4. Choose "main" branch and "/ (root)"
5. Your site will be live at `https://YOUR-USERNAME.github.io/business-analytics-portfolio/`

## License

This project is open source and available under the MIT License.

## Author

**Birva**

---

Built with Python, Pandas & Plotly
