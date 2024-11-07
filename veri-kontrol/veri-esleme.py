import pandas as pd

# Dosyaları oku
ana_veri_df = pd.read_csv('ana-veri/ana-veri-son.csv')
es_veri_df = pd.read_csv('es-veri/es-veri-son.csv')

# Sütun adlarını temizle (boşlukları kaldır)
ana_veri_df.columns = ana_veri_df.columns.str.strip()
es_veri_df.columns = es_veri_df.columns.str.strip()

# Veri tiplerini kontrol et ve aynı tipe dönüştür
# Yıl ve Year sütunlarının tiplerini karşılaştır
print("Yıl veri tipi:", ana_veri_df['Yıl'].dtype)
print("Year veri tipi:", es_veri_df['Year'].dtype)

# Eğer veri tipleri farklıysa, onları aynı tipe dönüştür
ana_veri_df['Yıl'] = ana_veri_df['Yıl'].astype(str)
es_veri_df['Year'] = es_veri_df['Year'].astype(str)

# İlçe ve District sütunlarındaki boşlukları temizle
ana_veri_df['İlçe'] = ana_veri_df['İlçe'].str.strip()
es_veri_df['District'] = es_veri_df['District'].str.strip()

# Kullanıcı Sınıfı ve Usage_Type sütunlarındaki boşlukları temizle
ana_veri_df['Kullanıcı Sınıfı'] = ana_veri_df['Kullanıcı Sınıfı'].str.strip()
es_veri_df['Usage_Type'] = es_veri_df['Usage_Type'].str.strip()

# İlçe ve District sütunlarını büyük harfe çevir
ana_veri_df['İlçe'] = ana_veri_df['İlçe'].str.upper()
es_veri_df['District'] = es_veri_df['District'].str.upper()

# Kullanıcı Sınıfı ve Usage_Type sütunlarını büyük harfe çevir
ana_veri_df['Kullanıcı Sınıfı'] = ana_veri_df['Kullanıcı Sınıfı'].str.upper()
es_veri_df['Usage_Type'] = es_veri_df['Usage_Type'].str.upper()

# Boş değerleri kontrol et
print("Ana veri eksik değerler:\n", ana_veri_df.isnull().sum())
print("Es veri eksik değerler:\n", es_veri_df.isnull().sum())

# İlçe eşleşmesi yaparak sadece 'District_Id' verisini ekle
merged_df = pd.merge(
    ana_veri_df, 
    es_veri_df[['District', 'District_Id']],  # sadece İlçe ve District_Id alınır
    left_on='İlçe',  # sadece İlçe'ye göre eşleşme yapılır
    right_on='District', 
    how='left'
)

# Diğer eşleşmeleri 'Yıl' ve 'Kullanıcı Sınıfı' sütunlarına göre yap
merged_df = pd.merge(
    merged_df, 
    es_veri_df[['Year', 'District', 'Usage_Type', 'Count']],  # diğer veriler
    left_on=['Yıl', 'İlçe', 'Kullanıcı Sınıfı'], 
    right_on=['Year', 'District', 'Usage_Type'], 
    how='left'
)

# 'Count' sütununu integer türüne dönüştür
merged_df['Count'] = merged_df['Count'].astype('Int64')

# Sütun adlarını yeniden düzenle
merged_df = merged_df.rename(columns={
    'Count': 'Toplam Abone',
    'District_Id': 'İlçe Id'
})

# Gereksiz sütunları kaldır

# Yeni sıralanmış DataFrame
merged_df = merged_df[['Yıl', 'İlçe Id', 'İlçe', 'Kullanıcı Sınıfı', 'Kullanıcı Türü', 'Kullanım Sınıfı', 'Toplam Abone', 'Abone Sayı', 'Kullanım(m³)']]
# Birleştirilmiş veride tekrarlanan satırları kaldır
merged_df = merged_df.drop_duplicates()


# Sonuçları yeni bir dosyaya kaydet
merged_df.to_csv('veri-kontrol/birlesmis-veri-v2.csv', index=False)

# Sonuçları kontrol et
print(merged_df.head())
