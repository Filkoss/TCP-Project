import urllib.request  # Použití správného vestavěného modulu

# URL cílové stránky
url = "http://vlada.cz"

# Otevření URL a načtení obsahu
with urllib.request.urlopen(url) as response:
    html_content = response.read().decode("utf-8")

# Výpis HTML kódu stránky
print(html_content)
