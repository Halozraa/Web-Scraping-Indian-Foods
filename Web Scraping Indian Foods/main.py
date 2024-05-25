import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Daftar URL yang ingin di-scrap
main_url = 'https://www.pureindianfoods.com'
urls = [
    'https://www.pureindianfoods.com/collections/all',
    'https://www.pureindianfoods.com/collections/all?page=2',
    'https://www.pureindianfoods.com/collections/all?page=3',
    'https://www.pureindianfoods.com/collections/all?page=4',
    'https://www.pureindianfoods.com/collections/all?page=5',
    'https://www.pureindianfoods.com/collections/all?page=6',
    'https://www.pureindianfoods.com/collections/all?page=7',
    'https://www.pureindianfoods.com/collections/all?page=8',
    'https://www.pureindianfoods.com/collections/all?page=9',
    'https://www.pureindianfoods.com/collections/all?page=10',
]

def scrapy(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')

    # Semua tabel
    collet_main = soup.find('div', class_='collection por')

    tabel_product = []

    # Tabel utama
    tabel1 = collet_main.find_all('li', class_='grid__item') # Seleksi tabel, ini akan diulang menggunakan for

    for collet_second in tabel1:
        # Nama produk
        name_product = collet_second.find('a').text.strip()

        # Made in
        made_in = collet_second.find('div', class_='caption light card__vendor').text.strip()

        # Rating utama dan total terjual utama
        rating = collet_second.find('div', class_='loox-rating')

        # Ambil rating
        ratings = rating['data-rating'] if rating and rating.has_attr('data-rating') else None

        # Total terjual
        sell_product = rating['data-raters'] if rating and rating.has_attr('data-raters') else None

        # Harga produk
        price_product = collet_second.find('span', class_='price-item price-item--regular').text.strip()

        
        #link product
        links = collet_second.find_all('a')
        for link in links:
            href = link.get('href')
            link_done = main_url+href

        #tabel data save
        tabel_product.append({
            'Name Product': name_product,
            'Made In': made_in,
            'Rating Product': ratings,
            'Terjual': sell_product,
            'Harga': price_product,
            'Link': link_done
        })

    # Buat DataFrame dari daftar
    df = pd.DataFrame(tabel_product)
    return df

# Loop melalui URL dan scrap setiap halaman
all_data = []
for url in urls:
    print(f"Scraping Data {url}")
    df = scrapy(url)
    if df is not None:
        all_data.append(df)
    else:
        print(f"No data found at {url}")

# Gabungkan semua DataFrame menjadi satu (opsional)
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    print(combined_df)
else:
    print("No data scraped")

#output simpan data 
output_save_to = 'file'
file_save = os.path.join(output_save_to,'Scraping_Web.csv')

# Pastikan folder tujuan ada, jika tidak ada buat folder tersebut
os.makedirs(output_save_to, exist_ok=True)


# Simpan data ke file CSV
if not combined_df.empty:
    combined_df.to_csv('Scraping_Web.csv', index=False)
else:
    print("data tidak bisa disave")

# Jika ada data tersimpan dalam DataFrame, konversi file CSV ke Excel
if not combined_df.empty:
    excel_file = os.path.join(output_save_to, 'scraping_results.xlsx')
    combined_df.to_excel(excel_file, index=False)
    print(f"CSV file converted to Excel: {excel_file}")