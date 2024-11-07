import pandas as pd

# Verileri değişkene atama
es_veri_df = pd.read_csv('es-veri/es-veri-son.csv')
ana_veri_df = pd.read_csv('ana-veri/ana-veri-son.csv')

es_veri_df['Usage_Type'] = es_veri_df['Usage_Type'].str.strip()
ana_veri_df['Kullanıcı Sınıfı'] = ana_veri_df['Kullanıcı Sınıfı'].str.strip()

# Farklı olan verileri bulma
farkli_veriler = set(es_veri_df['Usage_Type']).symmetric_difference(set(ana_veri_df['Kullanıcı Sınıfı']))

# Farklı verileri yazdırma
print("Farklı veriler:")
print(farkli_veriler)
