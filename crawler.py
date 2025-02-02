import urllib.request
from bs4 import BeautifulSoup
import time

# Definice hlavní stránky
base_url = "http://vlada.cz"

def fetch_html(url):
    """Načte HTML obsah stránky a vrátí ho jako BeautifulSoup objekt."""
    try:
        with urllib.request.urlopen(url) as response:
            return BeautifulSoup(response.read().decode("utf-8"), "html.parser")
    except Exception as e:
        print(f"Chyba při načítání {url}: {e}")
        return None

# 1️⃣ Stažení hlavní stránky
soup = fetch_html(base_url)

if soup:
    # 2️⃣ Výpis titulku hlavní stránky
    title = soup.title.string.strip() if soup.title else "Nenalezeno"
    print(f"🏠 Titulek hlavní stránky: {title}")

    # 3️⃣ Seznam odkazů na hlavní stránce
    links = set()  # Použijeme set() pro odstranění duplicit
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/"):  # Relativní odkaz => přidáme doménu
            href = base_url + href
        links.add(href)

    print(f"🔗 Počet odkazů na hlavní stránce: {len(links)}")

    # 4️⃣ Procházení každého odkazu z hlavní stránky (2. úroveň)
    for link in list(links)[:10]:  # Omezíme na prvních 10 odkazů (můžete změnit)
        time.sleep(1)  # Přidáme pauzu, abychom web nespadl pod DoS útokem
        soup_subpage = fetch_html(link)
        if soup_subpage:
            sub_title = soup_subpage.title.string.strip() if soup_subpage.title else "Nenalezeno"
            sub_links = soup_subpage.find_all("a", href=True)
            print(f"\n🌍 Navštívený odkaz: {link}")
            print(f"   🏷 Titulek: {sub_title}")
            print(f"   🔗 Počet odkazů na stránce: {len(sub_links)}")
