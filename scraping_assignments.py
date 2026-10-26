"""
Web scraping assignments.  Run:  python scraping_assignments.py [a1 a1b a2 a3 a4 a5]
Needs internet access:  pip install requests beautifulsoup4 lxml pandas
"""
import re
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (student-assignment scraper)"}


def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


# ---------------------------------------------------------------------------
# Lab 2 Assignment 1: Worldometers countries (+ cleaning, stats, histogram)
# ---------------------------------------------------------------------------
def a1_worldometers():
    url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/"
    soup = get_soup(url)
    rows = []
    # the page lists countries as links/rows; adapt selector after Inspect Element
    tables = soup.find_all("table")
    if tables:
        df = pd.read_html(str(tables[0]))[0]
    else:
        for a in soup.select("a[href*='/world-population/'], a[href*='/geography/']"):
            name = a.get_text(strip=True)
            if name:
                rows.append({"Country": name, "Link": a.get("href")})
        df = pd.DataFrame(rows)
    print(df.head(10)); print(df.shape); df.info()

    # Population: use worldometers population table (separate page) and merge
    pop = pd.read_html("https://www.worldometers.info/world-population/population-by-country/")[0]
    pop = pop.rename(columns={"Country (or dependency)": "Country", "Population (2025)": "Population"})
    pop = pop[["Country", pop.columns[pop.columns.str.startswith("Population")][0]]]
    pop.columns = ["Country", "Population"]
    df = pop.copy()

    print("Duplicates:", df.duplicated().sum()); df = df.drop_duplicates()
    print("Missing:\n", df.isna().sum())
    df["Population"] = pd.to_numeric(df["Population"].astype(str).str.replace(",", ""), errors="coerce")
    df["Population"] = df["Population"].fillna(df["Population"].median())
    df.to_csv("countries.csv", index=False)

    p = df["Population"]
    print("Mean", p.mean(), "Median", p.median(), "Mode", p.mode()[0], "Var", p.var(), "Std", p.std(),
          "Min", p.min(), "Max", p.max(), "Q1/Q2/Q3", p.quantile([.25, .5, .75]).tolist(),
          "IQR", p.quantile(.75) - p.quantile(.25))
    print(p.describe())
    plt.figure(figsize=(8, 4)); sns.histplot(p, bins=40, kde=True); plt.title("Country population")
    plt.savefig("countries_hist.png", dpi=110)


# ---------------------------------------------------------------------------
# Text-based scraping: books.toscrape.com (first page)
# ---------------------------------------------------------------------------
def a1_books():
    soup = get_soup("https://books.toscrape.com/")
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    data = []
    for art in soup.select("article.product_pod"):
        data.append({
            "Book Title": art.select_one("h3 a")["title"],
            "Price": art.select_one("p.price_color").get_text(strip=True),
            "Availability": art.select_one("p.instock").get_text(strip=True),
            "Rating": rating_map[art.select_one("p.star-rating")["class"][1]],
        })
    df = pd.DataFrame(data)
    df["Price_num"] = df["Price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    df.drop(columns="Price_num").to_csv("books.csv", index=False)
    print(df.head())
    print("In stock:", df["Availability"].str.contains("In stock").sum())
    print("Most expensive:\n", df.loc[df["Price_num"].idxmax(), ["Book Title", "Price"]])
    print("5-star books:\n", df[df["Rating"] == 5]["Book Title"].tolist())


# ---------------------------------------------------------------------------
# Assignment 2: scrapethissite countries
# ---------------------------------------------------------------------------
def a2_countries():
    soup = get_soup("https://www.scrapethissite.com/pages/simple/")
    rows = []
    for c in soup.select("div.country"):
        rows.append({
            "Country": c.select_one("h3.country-name").get_text(strip=True),
            "Capital": c.select_one("span.country-capital").get_text(strip=True),
            "Population": int(c.select_one("span.country-population").get_text(strip=True)),
            "Area": float(c.select_one("span.country-area").get_text(strip=True)),
        })
    df = pd.DataFrame(rows); df.to_csv("countries.csv", index=False)
    print(df.head())
    print("Max population:", df.loc[df.Population.idxmax(), "Country"])
    print("Min area:", df.loc[df.Area.idxmin(), "Country"])
    print("Average population:", df.Population.mean())
    print("Top 10 populated:\n", df.nlargest(10, "Population")[["Country", "Population"]])


# ---------------------------------------------------------------------------
# Assignment 3: hockey teams (paginated HTML table)
# ---------------------------------------------------------------------------
def a3_hockey():
    base = "https://www.scrapethissite.com/pages/forms/?page_num={}"
    frames = []
    page = 1
    while True:
        soup = get_soup(base.format(page))
        rows = soup.select("tr.team")
        if not rows:
            break
        for r in rows:
            g = lambda cls: r.select_one(f"td.{cls}").get_text(strip=True)
            frames.append({"Team Name": g("name"), "Year": int(g("year")), "Wins": int(g("wins")),
                           "Losses": int(g("losses")), "Win Percentage": float(g("pct"))})
        page += 1
        time.sleep(0.5)
    df = pd.DataFrame(frames); df.to_csv("hockey.csv", index=False)
    print(df.head(), df.shape)


# ---------------------------------------------------------------------------
# Assignment 5: NIT Raipur CSE faculty directory
# ---------------------------------------------------------------------------
def a5_faculty():
    url = "https://www.nitrr.ac.in/aboutcse.php"
    soup = get_soup(url)
    print("Title:", soup.title.get_text(strip=True))
    tables = soup.find_all("table")
    print("Tables found:", len(tables))
    if tables:
        # choose the table with a faculty-like header
        for t in tables:
            df = pd.read_html(str(t))[0]
            if any(re.search("name|designation|email", str(c), re.I) for c in df.columns):
                df.to_csv("faculty.csv", index=False); print(df.head()); return
        pd.read_html(str(tables[0]))[0].to_csv("faculty.csv", index=False)
    else:
        # fallback: collect text blocks that look like names with titles and emails
        text = soup.get_text("\n", strip=True)
        emails = sorted(set(re.findall(r"[\w.\-]+@[\w.\-]+\.\w+", text)))
        names = re.findall(r"(?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.)\s*[A-Z][\w.\s]{2,40}", text)
        pd.DataFrame({"Name": pd.Series(names), "Email": pd.Series(emails)}).to_csv("faculty.csv", index=False)
    print("Saved faculty.csv (inspect the page HTML and tighten the selectors if columns look off)")


ALL = dict(a1=a1_worldometers, a1b=a1_books, a2=a2_countries, a3=a3_hockey, a5=a5_faculty)

if __name__ == "__main__":
    for k in (sys.argv[1:] or ALL):
        ALL[k]()
