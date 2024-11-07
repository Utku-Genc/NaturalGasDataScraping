from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

# Kullanıcıdan veri sayısını al
try:
    dataCount = int(input("Lütfen veri sayısını girin: "))
except ValueError:
    print("Lütfen geçerli bir sayı girin.")



chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--incognito") 
driver = webdriver.Chrome(options=chromeOptions)

# Sayfayı açma işlemi "https://data.ibb.gov.tr/dataset/istanbul-ilceleri-dogalgaz-kullanim-sinifi-kullanici-sayisi-tuketim-miktari/resource/86bc29a5-751a-4e83-a9de-0a103da94483" bu link çalışmadı sitedeki iframe linkini kullanarak yapınca çalışıyor.
driver.get("https://data.ibb.gov.tr/dataset/istanbul-ilceleri-dogalgaz-kullanim-sinifi-kullanici-sayisi-tuketim-miktari/resource/86bc29a5-751a-4e83-a9de-0a103da94483/view/90892f7e-286e-444b-a350-050479de2be4")
driver.maximize_window()

# Sayfanın tamamen yüklenmesini bekleme bunu anlamak için veri giriş kısmının var olup olmadığını kontrol ediyoruz
element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="to"]'))
)
# Eğer tüm veriyi istiyorsak bunu yorum yapıyoruz ve altta ki kodları yorumdan normale çeviriyoruz bunuda yorum yapıyoruz

# Veri sayısını alma
# dataCount = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/span').text
# dataCount = int(dataCount.strip())

# Veri sayısını veri giriş kısmına yazıp gönderme kısmı
element = driver.find_element(By.XPATH, '//*[@id="to"]')
driver.execute_script("arguments[0].value = '';", element) # null yapma
element.click()
element.send_keys(dataCount)
print(dataCount)
element.send_keys(Keys.ENTER)

# Buraya kadar

time.sleep(5)

# Veri isteği gönderildikten sonra sayfanın yüklenmesini bekleme kısmı. Yükleniyor yazısını içeren div kaybolana kadar bekliyoruz
try:
    # Div'in yok olmasını bekleme
    WebDriverWait(driver, 300).until(
        EC.invisibility_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div"))
    )
except Exception as e:
    print(f"Hata: {e}")

# Kaydırma işleminin değişkenleri 
scroll_position = 0
max_scroll = (dataCount - 23) * 25  
scroll_increment = 25 
i = 1

# Yazdırılan verileri tutmak için bir set oluştur
printed_data = set()

# Kaydırma işelmi sayfa içinde değil div içinde olacağı için div'e ait xpath
scrollable_div = driver.find_element(By.XPATH, '/html/body/div/div/div[4]/div[1]/div[5]')

while scroll_position < max_scroll:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[1];", scrollable_div, scroll_increment)
    time.sleep(0.2)  # Her kaydırmadan sonra bekle yoksa çok hızlı olduğu için data içeren div'i bulamıyoruz

    # data_element'i her kaydırmadan sonra yeniden bul
    data_element = driver.find_element(By.CSS_SELECTOR, 'div.ui-widget-content') 

    # Verinin tekrar yazdırılmasını engellemek için veriyi data_text ile kaydediyoruz.  Eğer veri set'in içinde yoksa ekleyip kaydediyoruz
    data_text = data_element.text.replace("\n", " | ")
    if data_text not in printed_data:
        print("{}. Veri: \t{}".format(i, data_text))
        printed_data.add(data_text)
        i += 1

    scroll_position += scroll_increment

# Sayfa yapısından dolayı son 25-26 veri yukarda ki kodla çekilemiyor. Bundan dolayı en son verileri aşağıdaki kodla çekiyoruz eğer var olan bir veri ise set'e eklemiyor yoksa set'e ekliyor
data_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ui-widget-content')

print("\nSon kalan veriler:\n")
for element in data_elements:
    data_text = element.text.replace("\n", " | ")
    
    if data_text not in printed_data:
        print("{}. Veri: \t{}".format(i, data_text))
        printed_data.add(data_text)
        i += 1

# Verileri çekme ilk deneme bu sayfa dinamik olduğu için ilk sayfa yüklendiğinde sadece 47 veriyi çekiyor yukardaki koda döndüm
# data_elements = driver.find_elements(By.CSS_SELECTOR, 'div.ui-widget-content')
# for index, data in enumerate(data_elements, 1):
#     print("{}: {}".format(index, data.text.replace("\n", " | ")))

print("\nEn son veriler: Set içinden yazdırıldığı için karışık")
for j, data in enumerate(printed_data, 1):
    print("{}. Veri: {}".format(j, data))

#Data_list oluşturuyoruz sonra set içine verileri aralarında çizgi olacak şekilde kaydedeip yazdırdığımız için onların temizlemesini yapıyoruz ve id içeren sütünü tanımlıyoruz
data_list = []
for data in printed_data:
    parts = data.split(' | ')
    if len(parts) == 7:
        real_id = int(parts[0]) 
        row = [real_id] + parts[1:] 
        data_list.append(row)

# ID'ye göre sıralama. x[0] sütünü ID
data_list.sort(key=lambda x: x[0])  

# CSV dosyasına kaydetme
with open('veriler.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Year', 'District', 'User Type', 'Usage Type', 'Count', 'Amount'])
    # Sıralı verileri yazdırma
    for row in data_list:
        writer.writerow(row)

print("Veriler veriler.csv dosyasına kaydedildi.")

time.sleep(180)
driver.quit()