from core.scraper import ContentScraper

# Inisialisasi scraper
scraper = ContentScraper()

# Jalankan scraping
hasil = scraper.scrape_url("https://www.detik.com/terpopuler")

# Tampilkan hasil
if hasil:
    print("Judul:", hasil['title'])
    print("\nKonten:", hasil['content'][:500] + "...")  # Tampilkan 500 karakter pertama
else:
    print("Gagal melakukan scraping")