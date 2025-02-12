import pandas as pd
import numpy as np
import random
import scipy.stats as stats
from datetime import datetime, timedelta

# Function to generate random dates
def generate_dates(start_date, end_date, n):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [start + timedelta(days=random.randint(0, (end - start).days)) for _ in range(n)]

# Function to determine season based on month and region
def get_season(month, region):
    northern_hemisphere = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring", 6: "Summer", 7: "Summer", 8: "Summer", 9: "Autumn", 10: "Autumn", 11: "Autumn"}
    southern_hemisphere = {6: "Winter", 7: "Winter", 8: "Winter", 9: "Spring", 10: "Spring", 11: "Spring", 12: "Summer", 1: "Summer", 2: "Summer", 3: "Autumn", 4: "Autumn", 5: "Autumn"}
    
    if region in ["North America", "Europe", "Asia"]:
        return northern_hemisphere.get(month, "Unknown")
    else:
        return southern_hemisphere.get(month, "Unknown")

# Function to get GDP per capita for each region
def get_gdp_per_capita(region):
    gdp_per_capita = {
        "North America": np.random.randint(50000, 70000),
        "Europe": np.random.randint(40000, 60000),
        "Asia": np.random.randint(10000, 30000),
        "South America": np.random.randint(5000, 20000),
        "Africa": np.random.randint(1000, 10000),
        "Australia": np.random.randint(45000, 65000)
    }
    return gdp_per_capita.get(region, 20000)

# Function to compute affected families
def get_families_affected(gdp_per_capita, severity):
    base = np.random.randint(100, 1000)
    severity_factor = {"Minor": 1, "Moderate": 2, "Severe": 3, "Catastrophic": 5}
    affected = base * severity_factor[severity] * (1 / (gdp_per_capita / 10000))
    return int(affected + np.random.uniform(-affected * 0.1, affected * 0.1))

# Function to compute displaced families
def get_families_displaced(families_affected, severity):
    severity_ratio = {"Minor": 0.1, "Moderate": 0.3, "Severe": 0.5, "Catastrophic": 0.5}
    displaced = families_affected * severity_ratio[severity]
    displaced = min(displaced, families_affected * 0.5)  # Ensuring displaced families are at most 50% of affected families
    return int(displaced + np.random.uniform(-displaced * 0.1, displaced * 0.1))

# Function to compute international aid
def get_international_aid(gdp_per_capita, families_affected):
    base_aid = families_affected * 1000
    aid = base_aid * np.exp(-gdp_per_capita / 50000)
    return int(aid + np.random.uniform(-aid * 0.1, aid * 0.1))

# Function to determine the country that provided the most aid
def get_donor_country():
    donor_countries = ["USA", "Canada", "Germany", "France", "UK", "Australia"]
    return random.choice(donor_countries)

# Function to determine the donation amount
def get_donation_amount(aid):
    return int(aid * np.random.uniform(0.05, 0.10))  # Ensuring donation is between 5% to 10% of total aid

# Function to generate dataset
def generate_disaster_data(n, region_countries):
    np.random.seed(42)
    regions = np.random.choice(list(region_countries.keys()), n)
    countries = [random.choice(region_countries[region]) for region in regions]
    dates = generate_dates("2000-01-01", "2025-01-01", n)
    gdp_per_capitas = [get_gdp_per_capita(region) for region in regions]
    disaster_severities = np.random.choice(["Minor", "Moderate", "Severe", "Catastrophic"], n, p=[0.4, 0.3, 0.2, 0.1])
    families_affected = [get_families_affected(gdp, severity) for gdp, severity in zip(gdp_per_capitas, disaster_severities)]
    families_displaced = [get_families_displaced(affected, severity) for affected, severity in zip(families_affected, disaster_severities)]
    international_aid = [get_international_aid(gdp, affected) for gdp, affected in zip(gdp_per_capitas, families_affected)]
    donor_countries = [get_donor_country() if aid > 0 else "None" for aid in international_aid]
    donation_amounts = [get_donation_amount(aid) if aid > 0 else 0 for aid in international_aid]
    
    data = {
        "S.no": np.arange(1, n + 1),
        "Date": dates,
        "Season": [get_season(date.month, region) for date, region in zip(dates, regions)],
        "Region": regions,
        "Country": countries,
        "Disaster Severity": disaster_severities,
        "GDP per Capita": gdp_per_capitas,
        "Families Affected": families_affected,
        "Families Displaced": families_displaced,
        "International Aid": international_aid,
        "Donor Country": donor_countries,
        "Donation Amount": donation_amounts
    }
    return pd.DataFrame(data)

region_countries = {"North America": ["USA", "Canada", "Mexico"], "South America": ["Brazil", "Argentina", "Chile"], "Europe": ["Germany", "France", "UK"], "Africa": ["South Africa", "Nigeria", "Kenya"], "Asia": ["India", "China", "Japan"], "Australia": ["Australia", "New Zealand"]}
df = generate_disaster_data(10000, region_countries)
df.to_csv("output/natural_disasters_dataset.csv", index=False)
print("Dataset Summary:")
print(df.describe())
