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

# Country-to-country relations matrix (realistic diplomatic ties)
relations_matrix = {
    "USA": {"Canada": 1.5, "UK": 1.4, "Germany": 1.3, "India": 1.2, "China": 0.7},
    "UK": {"USA": 1.4, "France": 1.3, "India": 1.1, "Germany": 1.4},
    "Germany": {"France": 1.3, "UK": 1.4, "USA": 1.3},
    "France": {"Germany": 1.3, "UK": 1.3, "Canada": 1.2},
    "China": {"Pakistan": 1.5, "Russia": 1.4, "India": 0.6, "USA": 0.7},
    "India": {"USA": 1.2, "UK": 1.1, "China": 0.6},
    "Australia": {"New Zealand": 1.5, "USA": 1.3, "UK": 1.2}
}

# Function to compute international relations score between countries
def get_relation_score(donor, recipient):
    return np.exp(-relations_matrix.get(donor, {}).get(recipient, 1.0))  # Exponential negative impact

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

# Function to compute population density
def get_population_density(region):
    population_density = {
        "North America": np.random.randint(50, 500),
        "Europe": np.random.randint(100, 1000),
        "Asia": np.random.randint(300, 1500),
        "South America": np.random.randint(50, 600),
        "Africa": np.random.randint(20, 500),
        "Australia": np.random.randint(10, 300)
    }
    return population_density.get(region, 200)

# Function to compute economic damage based on GDP and population density
def get_economic_damage(region, base_damage):
    gdp_factor = get_gdp_per_capita(region) / 10000
    pop_density_factor = get_population_density(region) / 100
    return int(base_damage * gdp_factor * pop_density_factor)

# Function to compute international relief received
def get_international_relief(region, country, gdp_per_capita, disaster_severity):
    base_relief = np.random.randint(5, 15)
    severity_factor = {"Minor": 1, "Moderate": 2, "Severe": 3, "Catastrophic": 5}
    donor = random.choice(list(relations_matrix.keys()))
    relation_score = get_relation_score(donor, country)
    relief = base_relief * (1 / (gdp_per_capita / 10000)) * severity_factor[disaster_severity] * relation_score
    return round(relief, 2)

# Function to generate dataset
def generate_disaster_data(n, region_countries):
    np.random.seed(42)
    regions = np.random.choice(list(region_countries.keys()), n)
    countries = [random.choice(region_countries[region]) for region in regions]
    dates = generate_dates("2000-01-01", "2025-01-01", n)
    gdp_per_capitas = [get_gdp_per_capita(region) for region in regions]
    population_densities = [get_population_density(region) for region in regions]
    base_economic_damages = np.random.gamma(shape=2, scale=500, size=n).astype(int)
    economic_damages = [get_economic_damage(region, damage) for region, damage in zip(regions, base_economic_damages)]
    disaster_severities = np.random.choice(["Minor", "Moderate", "Severe", "Catastrophic"], n, p=[0.4, 0.3, 0.2, 0.1])
    international_reliefs = [get_international_relief(region, country, gdp, severity) for region, country, gdp, severity in zip(regions, countries, gdp_per_capitas, disaster_severities)]
    
    data = {
        "Date": dates,
        "Region": regions,
        "Country": countries,
        "GDP Per Capita ($)": gdp_per_capitas,
        "Population Density (people per sq. km)": population_densities,
        "Economic Damage (Million $)": economic_damages,
        "Disaster Severity": disaster_severities,
        "International Relief Received ($ Million)": international_reliefs
    }
    return pd.DataFrame(data)

region_countries = {"North America": ["USA", "Canada", "Mexico"], "South America": ["Brazil", "Argentina", "Chile"], "Europe": ["Germany", "France", "UK"], "Africa": ["South Africa", "Nigeria", "Kenya"], "Asia": ["India", "China", "Japan"], "Australia": ["Australia", "New Zealand"]}
df = generate_disaster_data(10000, region_countries)
df.to_csv("natural_disasters_dataset.csv", index=False)
print("Dataset Summary:")
print(df.describe())
