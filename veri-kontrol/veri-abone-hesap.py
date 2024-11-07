import pandas as pd

# Dosyayı oku
merged_df = pd.read_csv('veri-kontrol/birlesmis-veri-v2.csv')

# Sütun adlarınındaki boşlukları temzileme
merged_df.columns = merged_df.columns.str.strip()

# Yıl, İlçe Id ve Kullanıcı Sınıfı verileri aynı olan satırlardaki abone sayısını toplayarak veride kaç tane o bağlamda veri olduğunu hesapladık
grouped = merged_df.groupby(['Yıl', 'İlçe Id', 'Kullanıcı Sınıfı'], as_index=False)['Abone Sayı'].sum()

# İsmini değiştirdik
grouped = grouped.rename(columns={'Abone Sayı': 'Verideki Toplam Abone'})

# Verileri birleştirdik ve sütün sıralamassını ayarladık
merged_df = pd.merge(merged_df, grouped[['Yıl', 'İlçe Id', 'Kullanıcı Sınıfı', 'Verideki Toplam Abone']], 
                     on=['Yıl', 'İlçe Id', 'Kullanıcı Sınıfı'], 
                     how='left')
merged_df = merged_df[['Yıl', 'İlçe Id', 'İlçe', 'Kullanıcı Sınıfı', 'Kullanıcı Türü', 'Kullanım Sınıfı', 'Toplam Abone', 'Verideki Toplam Abone','Abone Sayı', 'Kullanım(m³)']]

# Veriyi kaydetme
merged_df.to_csv('veri-kontrol/birlesmis-veri-v3.csv', index=False)