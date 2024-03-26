# Import library
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as by

# Open URL 
url= 'https://www.mobil123.com/mobil-dijual/toyota/indonesia'
driver = webdriver.Chrome()
driver.get(url)
data = []
for item in range(0,2):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    containers = soup.findAll('article', {'class':'listing--review'})
    # Melakukan perulangan Sejumlah banyak Container
    for container in containers:
        # Mengambil data nama dalam container
        name = container.find('a', {'class':'js-ellipsize-text'})
        # Membuat Kondisi
        if name:
            name = name.text.strip()
        else:
            # Karena terdapat beberapa elemen yang memuat nama maka dibuat kondisi lagi
            try:
                name = container.find('a',{'class':'text--clamp'}).text.strip()
            except:
                ('')

        # Mengambil data harga dalam container
        harga = container.find('div', {'class':'listing__price delta weight--bold'})
        # Membuat Kondisi
        if harga:
            harga = harga.text.strip()
        else:
            # Jika Harga Diskon
            try:
                harga = container.find('span', {'weight--semibold'}).text.strip()
            except:
                ("Tidak Tertera")

        # Mengambil data kondisi kendaran dalam container
        kondisi = container.find('span', {'class':'soft-quarter'})
        # Membuat Kondisi
        if kondisi:
            kondisi = kondisi.text.strip()
        else:
            ('')

        # Mengambil data lokasi dalam container
        lokasi = container.find_all('div', {'class':'item push-quarter--ends'})[1]
        # Membuat Kondisi
        if lokasi:
            lokasi = lokasi.text.strip()
        else:
            # print("")
            ('')

        # Mengambil data jenis transmisi dalam container
        transmisi = container.find('div', {'class':'item push-quarter--ends'})
        # Membuat Kondisi
        if transmisi:
            transmisi = transmisi.text.strip()
        else:
            ('')

        # Mengambil data jarank penggunakan dalam container
        penggunakan = container.find('div', {'class':'item push-quarter--ends soft--right push-quarter--right'})
        # Membuat Kondisi
        if penggunakan:
            penggunakan = penggunakan.text.strip()
            if penggunakan == "- KM":
                penggunakan = "0 KM"
        else:
            ('')
        # Mengisi list dengan data yang diperoleh
        data.append([
            name,
            harga,
            kondisi,
            lokasi,
            transmisi,
            penggunakan
        ])
    time.sleep(4)
    driver.find_element(by.CLASS_NAME, 'arrow--after').click()
    time.sleep(5)

df = pd.DataFrame(data, columns=['Merk Mobil', 'Harga', 'Kondisi','Lokasi', 'Trasmisi', 'Jarak Penggunakana'])
print(df)

# Menyimpan Hasil Scraping dalam Excel
writer = pd.ExcelWriter('mobil.xlsx')
df.to_excel(writer, index=False)
writer.close()
driver.quit()

