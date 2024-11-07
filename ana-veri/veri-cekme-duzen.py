import pandas as pd

# Veri Dosyasını belirttik
df = pd.read_csv('ana-veri/veriler.csv', sep=';')

# Sütun adlarındaki boşlukları temizledik
df.columns = df.columns.str.strip()
df['Kullanıcı Sınıfı'] = df['Kullanıcı Sınıfı'].str.strip()
df['Kullanım Sınıfı'] = df['Kullanım Sınıfı'].str.strip()

# Sayı hatalıydı python'ın anlayacağı hale getirdik
df['Düzeltilmiş Tüketim (m3)'] = df['Düzeltilmiş Tüketim (m3)'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)
df['Tüketim Yapan Gaz Kullanıcı Sayısı (Sayaç-Adet)'] = df['Tüketim Yapan Gaz Kullanıcı Sayısı (Sayaç-Adet)'].astype(int)

# Kullanıcı Sınıfı sütününda olan fakat kullanmayacağımız veriye sahip satırları sildik
df = df[df['Kullanıcı Sınıfı'] != 'OSB']
df = df[df['Kullanıcı Sınıfı'] != 'SERBEST BÖLGE SATIŞLARI']
df = df[df['Kullanıcı Sınıfı'] != '?']
df = df[df['Kullanıcı Sınıfı'] != "CNG SATICISI(ÖTV'SİZ"]
df = df[df['Kullanıcı Sınıfı'] != 'SAĞLIK KURUMLARI (ÖZEL)']
df = df[df['Kullanıcı Sınıfı'] != 'ÖZEL EĞİTİM KURUMLARI']


# Kullanım Türü sütunu ekleme ve doldurma fonksiyonu Kullanıcı sınıfı sütünunda ki veriye göre Kullanım türündeki veriyi ekliyor
def kullanım_türü(row):
    if row['Kullanıcı Sınıfı'] == 'MESKEN':
        return 'EV'
    elif row['Kullanıcı Sınıfı'] == 'TİCARİ':
        return 'DÜKKAN'
    elif row['Kullanıcı Sınıfı'] == 'TİCARİ (ÜRETİM)':
        return 'FABRİKA (ÜRETİM)'
    elif row['Kullanıcı Sınıfı'] == 'RESMİ EĞİTİM KURUMLALARI':
        return 'EĞİTİM KURUMU'
    elif row['Kullanıcı Sınıfı'] == 'RESMİ KURUM':
        return 'RESMİ KURUM'
    elif row['Kullanıcı Sınıfı'] == 'HAYIR KURUMU VE MÜZE':
        return 'KÜLTÜR KURUMU'  
    elif row['Kullanıcı Sınıfı'] == 'SAĞLIK KURUMLARI (RESMİ)':
        return 'SAĞLIK KURUMU'
    elif row['Kullanıcı Sınıfı'] == 'YABANCI TEMSİLCİLİK':
        return 'DİPLOMATİK TEMSİLCİLİK'
    elif row['Kullanıcı Sınıfı'] == 'İBADETHANE':
        return 'DİNİ TESİS' 
    elif row['Kullanıcı Sınıfı'] == 'ELEKTRİK ÜRETİM TESİSLERİ':
        return 'ELEKTRİK ÜRETİM TESİSİ'
    elif row['Kullanıcı Sınıfı'] == 'SANAYİ TESİSLERİ':
        return 'SANAYİ TESİSİ'
    else:
        return 'BİLİNMEYEN'

df['Kullanıcı Türü'] = df.apply(kullanım_türü, axis=1)

# Kullanıcı sınıfında olan verileri tek bir kez tekrarsız yazıyor
print(df['Kullanıcı Sınıfı'].unique())


#Diğer Veri ile kullanabilmek için bazı verileri yeniden adlandırdık
df['Kullanıcı Sınıfı'] = df['Kullanıcı Sınıfı'].str.strip().replace({
    'TİCARİ (ÜRETİM)': 'TİCARİ',
    'RESMİ EĞİTİM KURUMLALARI': 'RESMİ KURUM',
    'SAĞLIK KURUMLARI (RESMİ)': 'RESMİ KURUM',
    'ELEKTRİK ÜRETİM TESİSLERİ': 'SANAYİ TESİSLERİ'

}, regex=False)

# Sütun adlarını değiştirme çok uzun kalıyordu veriyi okumayı rahatlatmak için kısalttık
df = df.rename(columns={
    'Tüketim Yapan Gaz Kullanıcı Sayısı (Sayaç-Adet)': 'Abone Sayı',
    'Düzeltilmiş Tüketim (m3)': 'Kullanım(m³)'
})

# Sütun sırasını değiştirme
df = df[['Yıl', 'İlçe', 'Kullanıcı Sınıfı', 'Kullanıcı Türü', 'Kullanım Sınıfı', 'Abone Sayı', 'Kullanım(m³)']]

# Düzenlenmiş veriyi kaydetme
df.to_csv('ana-veri/ana-veri-son.csv', index=False)

print("Veri başarıyla düzenlendi ve kaydedildi.")
