# -*- coding: utf-8 -*-
"""crawling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y8V6xmGooPAyqwYJpkAkt2PhnCHjURS-
"""

import requests
from bs4 import BeautifulSoup
from csv import writer
import time

# Fungsi untuk mengambil semua tautan dari halaman
def crawl(url, visited, max_links):
    if url not in visited and len(visited) < max_links:
        visited.add(url)  # Tandai URL sebagai telah dikunjungi
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                html = BeautifulSoup(res.content, 'html.parser')

                # Mencari semua tautan artikel dalam halaman dan mencari di berbagai elemen dan kelas
                article_selectors = ['article', 'h2', 'h3']  # Menambahkan lebih banyak elemen
                articles = []
                for selector in article_selectors:
                    articles.extend(html.find_all(selector))

                for article in articles:
                    link_tag = article.find('a', href=True)
                    if link_tag:
                        href = link_tag['href']
                        # Memastikan tautan adalah URL lengkap
                        if href.startswith('/'):
                            href = "https://www.cnnindonesia.com" + href  # Mengubah menjadi URL lengkap
                        if href.startswith('http') and href not in visited:
                            # Mengambil judul artikel
                            title = link_tag.get_text(strip=True)  # Mengambil teks judul dengan strip

                            # Menulis ke CSV
                            csv_writer.writerow([title, href])
                            print(f"Menemukan tautan: {title} - {href}")

                            time.sleep(0.5)  # Mengurangi waktu jeda untuk efisiensi
                            crawl(href, visited, max_links)  # Rekursi untuk mengunjungi tautan yang ditemukan
                            if len(visited) >= max_links:
                                break  # Hentikan jika sudah mencapai batas
            else:
                print(f"Error: {res.status_code} saat mengakses {url}")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

# Fungsi untuk mengambil data tambahan dari API (jika perlu)
def get_additional_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Mengembalikan data JSON dari API
        else:
            print(f"Error: {response.status_code} saat mengakses API {api_url}")
            return None
    except Exception as e:
        print(f"Terjadi kesalahan saat mengakses API: {e}")
        return None

# Daftar URL awal untuk crawling
start_urls = [
    "https://www.cnnindonesia.com/teknologi"  # URL yang diinginkan
]

# Menyimpan data ke file CSV
max_links_to_visit = 50  # Jumlah maksimum tautan yang akan dikunjungi
with open('daftar_crawling_cnn.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["Judul", "Link"])

    visited = set()  # Set untuk menyimpan URL yang sudah dikunjungi

    for url in start_urls:
        crawl(url, visited, max_links_to_visit)

print("Crawling selesai. Lihat 'daftar_crawling_cnn.csv' untuk hasilnya.")