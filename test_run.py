import matplotlib.pyplot as plt
import seaborn as sns
from yavuz_msa import align_sequences
from yavuz_msa.core.distance import DistanceMatrixCalculator
from yavuz_msa.models.sequence import Sequence

def get_sequences_from_user():
    """Kullanıcıdan terminal üzerinden dinamik olarak dizileri alır."""
    sequences_dict = {}
    print("=== YavuzMSA Çoklu Dizi Hizalama Test Aracı ===")
    print("Dizileri girmeye başlayın. (İşlemi bitirmek için dizi adı kısmına 'q' yazın)\n")
    
    counter = 1
    while True:
        name = input(f"{counter}. Dizi Adı (Örn: Seq{counter} veya q): ").strip()
        if name.lower() == 'q':
            break
            
        seq_data = input(f"{name} için genetik diziyi girin (Örn: ATGC...): ").strip().upper()
        
        # Sadece geçerli karakterler girilmiş mi diye ufak bir kontrol eklenebilir
        if not seq_data:
            print("Dizi boş olamaz, tekrar deneyin.")
            continue
            
        sequences_dict[name] = seq_data
        counter += 1
        print("-" * 30)
        
    return sequences_dict

def visualize_distance_matrix(sequence_dict, k_size=3):
    """Verilen dizilerin K-mer tabanlı mesafe matrisini ısı haritası (heatmap) olarak çizer."""
    print("\n[Bilgi] Uzaklık matrisi hesaplanıyor ve görselleştiriliyor...")
    
    # Kütüphanemizin iç modellerini kullanarak dizileri nesneye çeviriyoruz
    sequences = [Sequence(header, seq) for header, seq in sequence_dict.items()]
    
    # Mesafe matrisini hesaplıyoruz
    dist_calc = DistanceMatrixCalculator(k_size=k_size)
    matrix = dist_calc.build_matrix(sequences)
    
    headers = list(sequence_dict.keys())
    
    # Matrisi Seaborn ile görselleştirme
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, cmap="YlOrRd", xticklabels=headers, yticklabels=headers, fmt=".2f")
    plt.title(f"Diziler Arası K-mer (k={k_size}) Uzaklık Matrisi (Jaccard)", pad=20)
    plt.xlabel("Diziler")
    plt.ylabel("Diziler")
    
    # Grafiği ekranda göster
    print("[Bilgi] Grafik penceresi açıldı. İşleme devam etmek için grafik penceresini kapatın.")
    plt.tight_layout()
    plt.show()

def main():
    # 1. Kullanıcıdan verileri al
    user_sequences = get_sequences_from_user()
    
    if len(user_sequences) < 2:
        print("\nHizalama yapabilmek için en az 2 dizi girmelisiniz. Program sonlandırılıyor.")
        return

    # 2. Mesafe matrisini görselleştir
    visualize_distance_matrix(user_sequences)
    
    # 3. Kütüphanenin ana fonksiyonunu çağırarak hizalamayı yap
    print("\n[Bilgi] MAFFT Algoritması çalıştırılıyor. Hizalama yapılıyor...")
    aligned_results = align_sequences(user_sequences)
    
    # 4. Sonuçları ekrana yazdır
    print("\n=== FİNAL HİZALAMA SONUCU ===")
    headers = list(user_sequences.keys())
    for i, aligned_seq in enumerate(aligned_results):
        print(f"{headers[i]:<10}: {aligned_seq}")
    print("=============================\n")

if __name__ == "__main__":
    main()