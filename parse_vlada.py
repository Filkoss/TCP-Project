import urllib.request
from bs4 import BeautifulSoup

# URL stránky
url = "http://vlada.cz"

# Stažení HTML obsahu stránky
with urllib.request.urlopen(url) as response:
    html_content = response.read().decode("utf-8")

# Parsování HTML pomocí BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# 1️⃣ Výpis titulku stránky
title = soup.title.string if soup.title else "Nenalezeno"
print(f"Titulek stránky: {title}")

# 2️⃣ Výpis nadpisů H1
h1_tags = soup.find_all("h1")
print("\nNadpisy H1:")
for h1 in h1_tags:
    print("-", h1.get_text(strip=True))

# 3️⃣ Výpis nadpisů H2
h2_tags = soup.find_all("h2")
print("\nNadpisy H2:")
for h2 in h2_tags:
    print("-", h2.get_text(strip=True))

# 4️⃣ Výpis URL adres všech odkazů
links = soup.find_all("a", href=True)
print("\nURL adresy odkazů:")
for link in links:
    print("-", link["href"])
