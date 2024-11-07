import pandas as pd

# CSV dosyasını açma
df = pd.read_csv('es-veri/es-veri-sutun.csv')

print("Sütun Adları:", df.columns)

print("\nİlk 5 Satır:")
print(df.head())

# Sütun adlarında ki boşlukaları kaldırma
df.columns = df.columns.str.strip() 

# Sayısal verileri Python'ın anlayacağı hale getirmek için gereksiz virgülleri sildik
df['Count'] = df['Count'].astype(str).str.replace(',', '').astype(int)
df['Using_Count'] = df['Using_Count'].astype(str).str.replace(',', '').astype(int)
df['Amount'] = df['Amount'].astype(str).str.replace(',', '').astype(float)

# # Sütünlardaki verileri tek bir kez tekrarsız yazıyor kontrol için kullandım
# print("District'teki farklı değerler:")
# print(df['District'].unique())

# print("\nUsage_Type'teki farklı değerler:")
# print(df['Usage_Type'].unique())


# Veri çekilirken sitede farklı bir yazı tipi yada türü . Kullanıldığı için veri yanlış geldi, onu düzelttik.
df['District'] = df['District'].str.strip().replace({
    'Adalar': 'ADALAR',
    'Arnavutköy': 'ARNAVUTKÖY',
    'Ataþehir': 'ATAŞEHİR',
    'Avcýlar': 'AVCILAR',
    'Baðcýlar': 'BAĞCILAR',
    'Bahçelievler': 'BAHÇELİEVLER',
    'Bakýrköy': "BAKIRKÖY",
    'Baþakþehir': 'BAŞAKŞEHİR',
    'Bayrampaþa': 'BAYRAMPAŞA',
    'Beþiktaþ': 'BEŞİKTAŞ',
    'Beykoz': 'BEYKOZ',
    'Beylikdüzü': 'BEYLİKDÜZÜ',
    'Beyoðlu': 'BEYOĞLU',
    'Büyükçekmece': 'BÜYÜKÇEKMECE',
    'Çatalca': 'ÇATALCA',
    'Çekmeköy': 'ÇEKMEKÖY',
    'Esenler': 'ESENLER',
    'Esenyurt': 'ESENYURT',
    'Eyüpsultan': 'EYÜPSULTAN',
    'Fatih': 'FATİH',
    'Gaziosmanpaþa': 'GAZİOSMANPAŞA',
    'Güngören': 'GÜNGÖREN',
    'Kadýköy': 'KADIKÖY',
    'Kaðýthane': 'KAĞITHANE',
    'Kartal': 'KARTAL',
    'Küçükçekmece': 'KÜÇÜKÇEKMECE',
    'Maltepe': 'MALTEPE',
    'Pendik': 'PENDİK',
    'Sancaktepe': 'SANCAKTEPE',
    'Sarýyer': 'SARIYER',
    'Silivri': 'SİLİVRİ',
    'Sultanbeyli': 'SULTANBEYLİ',
    'Sultangazi': 'SULTANGAZİ',
    'Þile': 'ŞİLE',
    'Þiþli': 'ŞİŞLİ',
    'Tuzla': 'TUZLA',
    'Ümraniye': 'ÜMRANİYE',
    'Üsküdar': 'ÜSKÜDAR',
    'Zeytinburnu': 'ZEYTİNBURNU'
}, regex=False)

df['Usage_Type'] = df['Usage_Type'].str.strip().replace({
    'Yabancý Temsilcilik': 'YABANCI TEMSİLCİLİK',
    'Ticari': 'TİCARİ',
    'Ýbadethane': 'İBADETHANE',
    'Resmi Kurum': 'RESMİ KURUM',
    'Mesken': 'MESKEN',
    'Sanayi Tesisleri': 'SANAYİ TESİSLERİ',
    'Hayýr Kurumu ve Müze': 'HAYIR KURUMU VE MÜZE',
    'Diðer': 'DİĞER'
}, regex=False)

df['Year'] = df['Year'].str.strip().replace({
    '2020 (Ocak-Nisan)': '2020',
}, regex=False)

# # Son halini yazdırma kontrol için
# print("District'teki farklı değerler:")
# print(df['District'].unique())

# print("\nUsage_Type'teki farklı değerler:")
# print(df['Usage_Type'].unique())

# Düzenlenen veriyi tekrar CSV dosyasına kaydedin
df.to_csv('es-veri/es-veri-son.csv', index=False)

print("Veriler es-veri/es-veri-son.csv dosyasına kaydedildi.")
