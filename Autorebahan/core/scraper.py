import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class ContentScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }
    
    def clean_text(self, text):
        """Membersihkan teks dari karakter tidak perlu"""
        text = re.sub(r'\s+', ' ', text)  # Hapus spasi berlebih
        text = re.sub(r'\[.*?\]', '', text)  # Hapus konten dalam []
        return text.strip()

    def scrape_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            domain = urlparse(url).netloc

            # Detik.com
            if 'detik.com' in domain:
                return self._scrape_detik(soup)
            
            # WordPress
            elif 'wordpress' in domain:
                return self._scrape_wordpress(soup)
            
            # Blogspot
            elif 'blogspot.com' in domain:
                return self._scrape_blogspot(soup)
            
            # Umum
            else:
                return self._scrape_general(soup)
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gagal scraping: {str(e)}',
                'url': url
            }

    def _scrape_detik(self, soup):
        title = soup.find('h1', {'class': 'detail__title'})
        content = soup.find('div', {'class': 'detail__body-text'})
        
        return {
            'status': 'success',
            'title': self.clean_text(title.text) if title else 'Judul Tidak Ditemukan',
            'content': '\n'.join([self.clean_text(p.text) for p in content.find_all('p')] if content else [])
        }

    def _scrape_wordpress(self, soup):
        title = soup.find('h1', {'class': 'entry-title'})
        content = soup.find('div', {'class': 'entry-content'})
        
        return {
            'status': 'success',
            'title': self.clean_text(title.text) if title else '',
            'content': '\n'.join([self.clean_text(p.text) for p in content.find_all('p')] if content else [])
        }

    def _scrape_blogspot(self, soup):
        title = soup.find('h1', {'class': 'post-title'})
        content = soup.find('div', {'class': 'post-body'})
        
        return {
            'status': 'success',
            'title': self.clean_text(title.text) if title else '',
            'content': '\n'.join([self.clean_text(p.text) for p in content.find_all('p')] if content else [])
        }

    def _scrape_general(self, soup):
        title = soup.find('title')
        body = soup.find('body')
        paragraphs = body.find_all(['p', 'div']) if body else []
        
        return {
            'status': 'success',
            'title': self.clean_text(title.text) if title else '',
            'content': '\n'.join([self.clean_text(p.text) for p in paragraphs])
        }