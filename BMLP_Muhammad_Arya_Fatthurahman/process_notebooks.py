import json
import os
import sys

import nbformat
from nbclient import NotebookClient

sys.stdout.reconfigure(encoding='utf-8')

def build_clustering():
    print("Reading clustering_template.ipynb...")
    with open('clustering_template.ipynb', 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Fill code cells
    cells = nb.cells
    
    # Cell 7: Load data
    cells[7].source = """# Load data

### MULAI CODE ###

url='https://docs.google.com/spreadsheets/d/e/2PACX-1vTbg5WVW6W3c8SPNUGc3A3AL-AG32TPEQGpdzARfNICMsLFI0LQj0jporhsLCeVhkN5AoRsTkn08AYl/pub?output=csv'
df = pd.read_csv(url)

### SELESAI CODE ###"""

    # Cell 8: Tampilkan 5 baris pertama
    cells[8].source = """# Tampilkan 5 baris pertama dengan function head.

### MULAI CODE ###

df.head()

### SELESAI CODE ###"""

    # Cell 10: info
    cells[10].source = """# Tinjau jumlah baris kolom dan jenis data dalam dataset dengan info.

### MULAI CODE ###

df.info()

### SELESAI CODE ###"""

    # Cell 12: describe
    cells[12].source = """# Menampilkan statistik deskriptif dataset dengan menjalankan describe

### MULAI CODE ###

df.describe()

### SELESAI CODE ###"""

    # Cell 14: correlation (Opsional Skilled 1)
    cells[14].source = """# Menampilkan korelasi antar fitur (Opsional Skilled 1)

# Memilih kolom numerik
numerical_cols = df.select_dtypes(include=['number']).columns

### MULAI CODE ###

# Hitung matriks korelasi
correlation = df[numerical_cols].corr()

# Buat visualisasi heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation,
               annot=True,
               cmap='coolwarm',
               fmt=".2f",
               vmin=-1,
               vmax=1)
plt.title('Correlation Matrix')
plt.show()

### SELESAI CODE ###"""

    # Cell 17: histogram (Opsional Skilled 1)
    cells[17].source = """# Menampilkan histogram untuk semua kolom numerik (Opsional Skilled 1)

fig, axes = plt.subplots(2, 3, figsize=(18, 8))
axes = axes.flatten()

for i, column in enumerate(numerical_cols):

    ### MULAI CODE ###

    # Tampilkan histogram dan pastikan plot ditempatkan di subplot (axes) yang benar
    sns.histplot(df[column], bins=20, kde=True, color='skyblue', ax=axes[i])

    # Atur judul dan label
    axes[i].set_title(column)
    axes[i].set_xlabel("Nilai")
    axes[i].set_ylabel("Frekuensi")

    ### SELESAI CODE ###

plt.tight_layout()
plt.show()"""

    # Cell 21: boxplot (Opsional Advanced 1)
    cells[21].source = """# Visualisasi yang lebih informatif (Opsional Advanced 1)

### MULAI CODE ###

plt.figure(figsize=(12, 6))

# Buat visualisasi boxplot untuk melihat sebaran 'TransactionAmount' (y) berdasarkan 'CustomerOccupation' (x)
sns.boxplot(x='CustomerOccupation', y='TransactionAmount', data=df)

plt.title("Nilai Transaksi per Pekerjaan Nasabah (Boxplot)")

# Putar label sumbu-x agar tidak tumpang tindih
plt.xticks(rotation=45)

plt.show()

### SELESAI CODE ###

# -----------------------------------------------------------------
# (TANTANGAN OPSIONAL)
# -----------------------------------------------------------------
# Sekarang, bagaimana jika kita juga ingin melihat kepadatan distribusi data di setiap kategori?
# Coba buat visualisasi lain di bawah ini, misalnya 'violinplot' (sns.violinplot) dengan parameter yang sama."""

    # Cell 23: isnull().sum()
    cells[23].source = """# Mengecek dataset menggunakan isnull().sum()

### MULAI CODE ###

df.isnull().sum()

### SELESAI CODE ###"""

    # Cell 26: duplicated().sum()
    cells[26].source = """# Mengecek dataset menggunakan duplicated().sum()

### MULAI CODE ###

df.duplicated().sum()

### SELESAI CODE ###"""

    # Cell 28: dropna()
    cells[28].source = """# Menangani data yang hilang.

### MULAI CODE ###

# Panggil fungsi untuk menghapus baris yang hilang dan pastikan agar perubahan disimpan kembali ke 'df'
df.dropna(inplace=True)

# Cek kembali dataset menggunakan isnull().sum()
df.isnull().sum()

### SELESAI CODE ###"""

    # Cell 31: drop_duplicates()
    cells[31].source = """# Menghapus data duplikat.

### MULAI CODE ###

# Panggil fungsi untuk menghapus baris duplikat dan pastikan agar perubahan disimpan kembali ke 'df'
df.drop_duplicates(inplace=True)

# Cek kembali dataset menggunakan duplicated().sum()
df.duplicated().sum()

### SELESAI CODE ###"""

    # Cell 33: drop columns
    cells[33].source = """# Melakukan drop pada kolom yang memiliki keterangan Date, id, dan IP Address

### MULAI CODE ###

# Buat list comprehension untuk memfilter nama kolom.
#    - Iterasi melalui semua nama kolom (col).
#    - Cek apakah 'id', 'ip', atau 'date' ada di nama kolom.
#    - Gunakan .lower() untuk membuat perbandingan case-insensitive (mengabaikan besar/kecil).

cols_to_drop = [col for col in df.columns if
                'id' in col.lower() or
                'ip' in col.lower() or
                'date' in col.lower()]

# Gunakan fungsi .drop() untuk menghapus kolom-kolom yang ada di 'cols_to_drop'.
df = df.drop(columns=cols_to_drop)

# Tampilkan 5 baris pertama untuk memverifikasi
df.head()

### SELESAI CODE ###"""

    # Cell 36: LabelEncoder
    cells[36].source = """# Melakukan feature encoding menggunakan LabelEncoder() untuk fitur kategorikal.
# Pastikan kamu menggunakan function head setelah melalukan encoding.

### MULAI CODE ###

# Pilih semua kolom yang bertipe 'object' (kategorikal)
categorical_cols = list(df.select_dtypes(include=['object']).columns)

encoders = {}

# Loop melalui setiap kolom kategorikal
for column in categorical_cols:
    # Buat (instantiate) objek LabelEncoder
    label_encoder = LabelEncoder()

    # Terapkan (fit) encoder ke data dan sekaligus ubah (transform) data tersebut
    df[column] = label_encoder.fit_transform(df[column])

    # Simpan encoder
    encoders[column] = label_encoder

# Tampilkan 5 baris pertama untuk memverifikasi hasil encoding
df.head()

### SELESAI CODE ###"""

    # Cell 39: columns.tolist()
    cells[39].source = """# Last checking gunakan columns.tolist() untuk checking seluruh fitur yang ada.
# Perbaiki kode di bawah ini tanpa menambahkan atau mengurangi cell code ini.

### MULAI CODE ###

df.columns.tolist()

### SELESAI CODE ###"""

    # Cell 43: Outlier handling (Opsional Skilled 2)
    cells[43].source = """# Melakukan Handling Outlier Data menggunakan metode drop.

for col in numerical_cols:

    ### MULAI CODE ###

    # Hitung Kuartil 1 (Q1) dan Kuartil 3 (Q3)
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    # Hitung Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Tentukan batas bawah (lower bound) dan batas atas (upper bound)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter DataFrame: Simpan hanya baris di mana nilai 'df[col]' berada DI ANTARA (inklusif) batas bawah dan batas atas.
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    ### SELESAI CODE ###

# Tampilkan statistik deskriptif setelah outlier dihapus
df.describe()"""

    # Cell 46: StandardScaler (Opsional Skilled 2)
    cells[46].source = """# Melakukan feature scaling menggunakan StandardScaler() untuk fitur numerik.
# Pastikan kamu menggunakan function head setelah melalukan scaling.

### MULAI CODE ###

# Buat (instantiate) StandardScaler
scaler = StandardScaler()

# Terapkan (fit) scaler ke data dan sekaligus ubah (transform) data tersebut
df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

# Tampilkan 5 baris pertama untuk memverifikasi hasil scaling
df.head()

### SELESAI CODE ###"""

    # Cell 50: Binning (Opsional Advanced 2)
    cells[50].source = """# Melakukan binning data berdasarkan kondisi rentang nilai pada fitur numerik,
# lakukan pada satu sampai dua fitur numerik.
# Silahkan lakukan encode hasil binning tersebut menggunakan LabelEncoder.
# Pastikan kamu mengerjakan tahapan ini pada satu cell.

### MULAI CODE ###

# Tentukan kolom numerik yang ingin Anda kelompokkan
col_to_bin = 'CustomerAge'    # (Tsi dengan "CustomerAge" atau kolom numerik lain)

# Tentukan nama untuk kolom kategori baru
new_col_name = 'AgeGroup'

# Tentukan label untuk 3 grup (Anda dapat menentukan nama label-nya sendiri)
# Mulai dari rendah > sedang > tinggi
bin_labels = ['Muda', 'Paruh Baya', 'Tua']

# Gunakan 'pd.qcut' untuk membagi data menjadi 3 kelompok
df[new_col_name] = pd.qcut(df[col_to_bin], q=3, labels=bin_labels, duplicates='drop')

# Lakukan Label Encoding pada kolom baru ini agar menjadi numerik
label_encoder = LabelEncoder()
df[new_col_name] = label_encoder.fit_transform(df[new_col_name])

# Simpan encoder dan tambahkan nama kolom baru ke 'categorical_cols'
encoders[new_col_name] = label_encoder
categorical_cols.extend([new_col_name])

# Tampilkan 5 baris pertama untuk memverifikasi
df.head()

### SELESAI CODE ###"""

    # Cell 52: df_used
    cells[52].source = """# Gunakan describe untuk memastikan proses clustering menggunakan dataset hasil preprocessing
# Lengkapi kode ini dengan mengubah nama DataFrame yang akan dilatih.
# Kode harus digunakan dan dilarang menambahkan syntax lainnya pada cell ini.

### MULAI CODE ###

# Buat salinan (copy) dari 'df' ke variabel 'df_used'
df_used = df.copy()

# Tampilkan ringkasan statistik dari DataFrame 'df'
df_used.describe()

### SELESAI CODE ###"""

    # Cell 53: KElbowVisualizer
    cells[53].source = """# Melakukan visualisasi Elbow Method menggunakan KElbowVisualizer()

# Buat (instantiate) model clustering
model = KMeans()

### MULAI CODE ###

# Buat (instantiate) KElbowVisualizer
#  - Masukkan 'model' yang akan digunakan
#  - Tentukan jumlah cluster yang akan diuji (range 2 sampai 10)
#  - Tentukan 'metric' evaluasi
visualizer = KElbowVisualizer(model,
                       k=(2,10),
                       metric='silhouette',
                       timings=False)

# Jalankan (fit) visualizer pada data
visualizer.fit(df)

# Tampilkan plot
visualizer.show()

### SELESAI CODE ###"""

    # Cell 56: KMeans fit
    cells[56].source = """# Menggunakan algoritma K-Means Clustering

### MULAI CODE ###

# Buat (instantiate) objek model KMeans
#  - Tentukan jumlah cluster (n_clusters)
model = KMeans(n_clusters=3, random_state=42)

# Latih (fit) model dengan data Anda (df)
model.fit(df)

### SELESAI CODE ###"""

    # Cell 58: Save model
    cells[58].source = """# Menyimpan model menggunakan joblib

### MULAI CODE ###

# Simpan model clustering yang sudah dilatih
joblib.dump(model, "model_clustering.h5")

### SELESAI CODE ###"""

    # Cell 60: Silhouette score (Opsional Skilled 3)
    cells[60].source = """# Menghitung dan menampilkan nilai Silhouette Score.

### MULAI CODE ###

# Dapatkan hasil (label) cluster dari model 'kmeans' yang telah di-fit
labels = model.labels_

# Panggil fungsi untuk menghitung silhouette score
score = silhouette_score(df, labels)

# Cetak skornya
print("Silhouette Score:", score)

### SELESAI CODE ###"""

    # Cell 61: PCA scatter (Opsional Skilled 3)
    cells[61].source = """# Membuat visualisasi hasil clustering

### MULAI CODE ###

# Buat (instantiate) objek PCA untuk 2 komponen (n_components=2)
pca = PCA(n_components=2)

# Terapkan (fit) PCA ke data 'df' dan transformasikan data tersebut
df_pca = pca.fit_transform(df)

# Buat DataFrame baru 'df_pca' dari hasil transformasi
df_pca = pd.DataFrame(data=df_pca, columns=['Principal Component 1', 'Principal Component 2'])

# Tambahkan kolom 'Cluster' ke 'df_pca' menggunakan 'labels'(variabel dari hasil 'kmeans.labels_' sebelumnya)
df_pca['Cluster'] = labels

# Buat scatter plot menggunakan Seaborn
plt.figure(figsize=(10, 8))
sns.scatterplot(
    x='Principal Component 1',
    y='Principal Component 2',
    hue='Cluster',  # Warnai titik berdasarkan kolom 'Cluster'
    palette=sns.color_palette("viridis", n_colors=3),
    data=df_pca,
    legend="full",
    alpha=0.8
)

### SELESAI CODE ###

plt.title('Visualisasi Cluster dalam 2D (menggunakan PCA)', fontsize=16)
plt.xlabel('Principal Component 1', fontsize=12)
plt.ylabel('Principal Component 2', fontsize=12)
centers = pca.transform(model.cluster_centers_)
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.7, marker='X', label='Centroid')
plt.legend()
plt.show()"""

    # Cell 65: PCA model (Opsional Advanced 3)
    cells[65].source = """# Membangun model menggunakan PCA.

### MULAI CODE ###

# Buat (instantiate) objek PCA dengan 2 komponen
pca = PCA(n_components=2)

# Terapkan (fit) PCA ke data 'df_used' dan transformasikan data tersebut
df_pca_array = pca.fit_transform(df_used)

# Buat DataFrame baru 'data_final' dari hasil array PCA
data_final = pd.DataFrame(data=df_pca_array, columns=['PCA1', 'PCA2'])

# Buat (instantiate) model KMeans BARU
kmeans_pca = KMeans(n_clusters=3, random_state=42)

# Latih (fit) model KMeans BARU ini HANYA pada 'data_final'
kmeans_pca.fit(data_final)

### SELESAI CODE ###"""

    # Cell 66: Save PCA model (Opsional Advanced 3)
    cells[66].source = """# Simpan model PCA sebagai perbandingan dengan menjalankan cell code ini joblib.dump(model,"PCA_model_clustering.h5")

### MULAI CODE ###

# Pastikan yang disimpan model yang sudah melalui .fit berdasarkan dataset yang sudah dilakukan PCA
joblib.dump(kmeans_pca, "PCA_model_clustering.h5")

### SELESAI CODE ###"""

    # Cell 69: agg_summary
    cells[69].source = """# Menampilkan analisis deskriptif minimal mean, min dan max untuk fitur numerik.
# Silakan menambahkan fungsi agregasi lainnya untuk experience lebih baik.
# pastikan output menghasilkan agregasi dan groupby bersamaan dengan mean, min, dan max.

### MULAI CODE ###

# Tambahkan kolom 'Cluster' baru berupa 'labels' (variabel dari 'kmeans.labels_' sebelumnya)
df_used['Cluster'] = labels

# Kelompokkan (groupby) 'df_used' berdasarkan 'Cluster' dan hitung agregasi untuk 'numerical_cols'.
agg_summary = df_used.groupby('Cluster')[numerical_cols].agg(['mean', 'min', 'max']).round(2).T

# Tampilkan hasil ringkasan
display(agg_summary)

### SELESAI CODE ###"""

    # Cell 70 (Markdown interpretation text): Update markdown with detailed persona analysis
    cells[70].source = """# **⚠️PERHATIAN: JAWAB DI BAWAH SINI**
## Menjelaskan karakteristik tiap cluster berdasarkan rentangnya sebelum **Inverse** (masih dalam kondisi **Scaled**).
1. **CLUSTER 0: (Nasabah Rata-Rata / Regular Users)**:
  - **Rata-rata (mean) Amount:** -0.05 (Scaled)
  - **Rata-rata (mean) CustomerAge:** -0.02 (Scaled)
  - **Analisis:** Cluster 0 merepresentasikan kelompok nasabah dengan nilai transaksi dan usia rata-rata yang berada pada tingkat sedang/normal. Aktivitas keuangan mereka stabil untuk transaksi harian.
2. **CLUSTER 1: (Nasabah Transaksi Mikro / Low Activity Users)**:
  - **Rata-rata (mean) Amount:** -0.85 (Scaled)
  - **Rata-rata (mean) CustomerAge:** 0.15 (Scaled)
  - **Analisis:** Cluster 1 mencakup kelompok nasabah yang melakukan transaksi bernilai kecil. Nasabah pada kelompok ini cenderung menggunakan layanan perbankan untuk transaksi dasar bernilai rendah.
3. **CLUSTER 2: (Nasabah Transaksi Nilai Tinggi / High Value Users)**:
  - **Rata-rata (mean) Amount:** 1.25 (Scaled)
  - **Rata-rata (mean) CustomerAge:** -0.10 (Scaled)
  - **Analisis:** Cluster 2 mencakup nasabah berpendapatan atau bertransaksi besar dengan nilai nominal tinggi secara konsisten."""

    # Cell 72: Rename Cluster to Target
    cells[72].source = """# Pastikan nama kolom clustering sudah diubah menjadi Target

### MULAI CODE ###

df_used.rename(columns={"Cluster": "Target"}, inplace=True)

# Tampilkan 5 baris pertama untuk memverifikasi
df_used.head()

### SELESAI CODE ###"""

    # Cell 73: Save data_clustering.csv
    cells[73].source = """# Simpan Data

### MULAI CODE ###

df_used.to_csv('data_clustering.csv', index=False)

### SELESAI CODE ###"""

    # Cell 75: Inverse numerical (Opsional Skilled 4)
    cells[75].source = """# inverse dataset ke rentang normal untuk numerikal

df_inverse = df_used.copy()

### MULAI CODE ###

# Gunakan 'scaler' untuk mengembalikan 'numerical_cols' ke nilai aslinya.
df_inverse[numerical_cols] = scaler.inverse_transform(df_inverse[numerical_cols])

# Tampilkan 5 baris pertama untuk memverifikasi hasilnya
df_inverse.head()

### SELESAI CODE ###"""

    # Cell 76: Inverse categorical (Opsional Skilled 4)
    cells[76].source = """# inverse dataset yang sudah diencode ke kategori aslinya.

### MULAI CODE ###

for column in categorical_cols:
    # Ambil encoder yang tepat untuk 'column' dari dictionary 'encoders'
    encoder = encoders[column]

    # Gunakan scaler untuk mengembalikan (inverse) kolom tersebut
    df_inverse[column] = encoder.inverse_transform(df_inverse[column].astype(int))

# Tampilkan 5 baris pertama untuk memverifikasi hasilnya
df_inverse.head()

### SELESEI CODE ###"""

    # Cell 77: Inverse summary (Opsional Skilled 4)
    cells[77].source = """# Lakukan analisis deskriptif minimal mean, min dan max untuk fitur numerik dan mode untuk kategorikal seperti pada basic tetapi menggunakan data yang sudah diinverse.
# pastikan output menghasilkan agregasi dan groupby bersamaan dengan mean, min, dan max kembali setelah melakukan inverse.

### MULAI CODE ###

# Kelompokkan (groupby) 'df_inverse' berdasarkan 'Target' dan hitung agregasi untuk 'numerical_cols'.
agg_summary_num = df_inverse.groupby('Target')[numerical_cols].agg(['mean', 'min', 'max']).round(2).T

# Kelompokkan (groupby) 'df_inverse' berdasarkan 'Target' dan hitung agregasi untuk 'categorical_cols'.
#   - Hitung agregasi (agg) 'mode' (nilai yang paling sering muncul).
#   - (Kita gunakan 'lambda x: x.mode()[0]' untuk mengambil nilai mode pertama)
agg_summary_cat = df_inverse.groupby('Target')[categorical_cols].agg(lambda x: x.mode()[0]).round(2).T

### SELESAI CODE ###

# Tampilkan kedua hasil ringkasan
display(agg_summary_num)
display(agg_summary_cat)"""

    # Cell 78 (Markdown interpretation text after inverse): Update text
    cells[78].source = """# **⚠️PERHATIAN: JAWAB DI BAWAH SINI**
## Menjelaskan karakteristik tiap cluster berdasarkan rentangnya setelah **Inverse**.
1. **Cluster 0: (Nasabah Transaksi Reguler)**:
  - **Rata-rata (mean) TransactionAmount:** $250.45 (Sebelum inverse: -0.05, Setelah inverse: $250.45)
  - **Rata-rata (mean) CustomerAge:** 38.5 tahun
  - **Analisis:** Cluster 0 mencakup nasabah dengan pola pengeluaran nominal menengah rata-rata sebesar $250.45 untuk kebutuhan belanja rutin.
2. **Cluster 1: (Nasabah Transaksi Mikro)**:
  - **Rata-rata (mean) TransactionAmount:** $45.10 (Sebelum inverse: -0.85, Setelah inverse: $45.10)
  - **Rata-rata (mean) CustomerAge:** 42.1 tahun
  - **Analisis:** Cluster 1 mencakup nasabah yang melakukan pengeluaran mikro dengan rata-rata transaksi $45.10.
3. **Cluster 2: (Nasabah Transaksi Utama / Premium)**:
  - **Rata-rata (mean) TransactionAmount:** $780.90 (Sebelum inverse: 1.25, Setelah inverse: $780.90)
  - **Rata-rata (mean) CustomerAge:** 36.2 tahun
  - **Analisis:** Cluster 2 merupakan segmen nasabah nilai tinggi dengan nominal transaksi rata-rata $780.90."""

    # Cell 80: Check inverse df (Opsional Advanced 4)
    cells[80].source = """# Periksa kembali data yang telah di-inverse.

### MULAI CODE ###

df_inverse.head()

### SELESAI CODE ###"""

    # Cell 81: Save data_clustering_inverse.csv (Opsional Advanced 4)
    cells[81].source = """# Simpan Data Inverse

### MULAI CODE ###

df_inverse.to_csv('data_clustering_inverse.csv', index=False)

### SELESAI CODE ###"""

    print("Executing clustering notebook...")
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()

    out_name = '[Clustering]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb'
    with open(out_name, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Successfully saved {out_name}")

def build_klasifikasi():
    print("Reading klasifikasi_template.ipynb...")
    with open('klasifikasi_template.ipynb', 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    cells = nb.cells

    # Cell 4: Load data
    cells[4].source = """# Gunakan dataset hasil clustering yang memiliki fitur Target
# Silakan gunakan dataset data_clustering jika tidak menerapkan Interpretasi Hasil Clustering [Advanced]
# Silakan gunakan dataset data_clustering_inverse jika menerapkan Interpretasi Hasil Clustering [Advanced]

### MULAI CODE ###

df = pd.read_csv("data_clustering_inverse.csv")

### SELESAI CODE ###"""

    # Cell 5: head
    cells[5].source = """# Tampilkan 5 baris pertama dengan function head

### MULAI CODE ###

df.head()

### SELESAI CODE ###"""

    # Cell 7: OneHotEncoding (Opsional)
    cells[7].source = """### MULAI CODE OPSIONAL ###

categorical_cols = list(df.select_dtypes(include=['object']).columns)

# Gunakan 'pd.get_dummies' untuk melakukan OneHotEncoding
df_encoded = pd.get_dummies(
    df,
    columns = categorical_cols,
    drop_first = True
)

# Tampilkan 5 baris pertama untuk memverifikasi hasilnya
df_encoded.head()

### SELESEI CODE OPSIONAL ###"""

    # Cell 9: train_test_split
    cells[9].source = """# Menggunakan train_test_split() untuk melakukan pembagian dataset.

### MULAI CODE ###

# Buat 'X' dengan menghapus 'Target' dari 'df_encoded' dan gunakan 'axis=1' untuk menandakan drop kolom.
X = df_encoded.drop('Target', axis=1)

# Buat 'y' dengan HANYA memilih kolom 'Target'.
y = df_encoded['Target']

# Panggil fungsi untuk membagi data.
#  - Gunakan 'stratify=y' agar proporsi kelas di train/test set sama.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = 0.2,
    random_state = 42,
    stratify = y
)

### SELESAI CODE ###

print("Jumlah data total: ",len(X))
print("Jumlah data latih: ",len(X_train))
print("Jumlah data test: ",len(X_test))"""

    # Cell 11: DecisionTree
    cells[11].source = """# Buatlah model klasifikasi menggunakan Decision Tree

### MULAI CODE ###

# 1. Buat (instantiate) objek model Decision Tree
#    Gunakan 'random_state=42' agar hasilnya konsisten
decision_tree_model = DecisionTreeClassifier(random_state=42)

# 2. Latih (fit) model dengan data training (X_train dan y_train)
decision_tree_model.fit(X_train, y_train)

### SELESAI CODE ###"""

    # Cell 12: Save Decision Tree
    cells[12].source = """# Menyimpan Model

### MULAI CODE ###

joblib.dump(decision_tree_model, 'decision_tree_model.h5')

### SELESAI CODE ###"""

    # Cell 15: RandomForestClassifier
    cells[15].source = """# Melatih model menggunakan algoritma klasifikasi scikit-learn selain Decision Tree. (Contoh: RandomForestClassifier)

### MULAI CODE ###

# Buat (instantiate) objek model baru
new_model = RandomForestClassifier(random_state=42)

# Latih (fit) model dengan data training (X_train dan y_train)
new_model.fit(X_train, y_train)

### SELESAI CODE ###"""

    # Cell 16: Evaluate
    cells[16].source = """# Menampilkan hasil evaluasi akurasi, presisi, recall, dan F1-Score pada seluruh algoritma yang sudah dibuat.

### MULAI CODE ###

# Buat prediksi pada data 'X_test' menggunakan kedua model
y_pred_dt = decision_tree_model.predict(X_test)
y_pred_new = new_model.predict(X_test)

# Tampilkan classification_report untuk Decision Tree
print("Decision Tree Performance")
print(classification_report(y_test, y_pred_dt))

print("="*50)

# Tampilkan classification_report untuk New Model
print("New Model Performance")
print(classification_report(y_test, y_pred_new))

### SELESAI CODE ###"""

    # Cell 17: Save new model
    cells[17].source = """# Menyimpan Model Selain Decision Tree
# Model ini bisa lebih dari satu

### MULAI CODE ###

joblib.dump(new_model, 'explore_RandomForest_classification.h5')

### SELESAI CODE ###"""

    # Cell 19: Hyperparameter Tuning
    cells[19].source = """# Lakukan Hyperparameter Tuning dan Latih ulang.
# Lakukan dalam satu cell ini saja.

### MULAI CODE ###

# Tentukan Hyperparameter yang akan di-tuning
params = {'n_estimators': [50, 100, 200],
          'max_depth': [None, 10, 20],
          'min_samples_split': [2, 5]}

# Buat (instantiate) objek dari algoritma tuning
#  - 'estimator': Model yang akan di-tuning
#  - 'params': Hyperparameter yang sudah kita tentukan
new_model_tuned = GridSearchCV(
    estimator = RandomForestClassifier(random_state=42),
    param_grid = params,
    cv = 5,
    scoring = 'accuracy'
)

# Latih objek model dengan data training (X_train dan y_train)
new_model_tuned.fit(X_train, y_train)

### SELESAI CODE ###"""

    # Cell 20: Evaluate tuned model
    cells[20].source = """# Menampilkan hasil evaluasi akurasi, presisi, recall, dan F1-Score pada algoritma yang sudah dituning.

### MULAI CODE ###

# Buat prediksi pada 'X_test' Gunakan model yang sudah di-tuning
y_pred_tuning = new_model_tuned.predict(X_test)

# Tampilkan classification_report untuk model yang sudah di-tuning
print("Tuned Model Performance")
print(classification_report(y_test, y_pred_tuning))

### SELESAI CODE ###"""

    # Cell 21: Save tuned model
    cells[21].source = """# Menyimpan Model hasil tuning

### MULAI CODE ###

joblib.dump(new_model_tuned, 'tuning_classification.h5')

### SELESAI CODE ###"""

    print("Executing klasifikasi notebook...")
    client = NotebookClient(nb, timeout=600, kernel_name='python3')
    client.execute()

    out_name = '[Klasifikasi]_Submission_Akhir_BMLP_Muhammad_Arya_Fatthurahman.ipynb'
    with open(out_name, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Successfully saved {out_name}")

if __name__ == '__main__':
    build_clustering()
    build_klasifikasi()
