import matplotlib.pyplot as plt
import seaborn as sns

class DistanceVisualizer:
    """Hesaplanan mesafe matrislerini görselleştiren sınıf."""
    
    @staticmethod
    def plot_heatmap(matrix, headers, k_size=3):
        """Mesafe matrisini ısı haritası (heatmap) olarak ekrana çizer."""
        print(f"\n[Bilgi] {len(headers)} dizi için K-mer (k={k_size}) matrisi çiziliyor...")
        plt.figure(figsize=(8, 6))
        ax = sns.heatmap(matrix, annot=True, cmap="YlOrRd", xticklabels=headers, yticklabels=headers, fmt=".2f")

        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        
        plt.title(f"Diziler Arası K-mer (k={k_size}) Uzaklık Matrisi", pad=20)
        plt.xlabel("Diziler")
        plt.ylabel("Diziler")
        
        print("[Bilgi] Grafik penceresi açıldı. İşleme devam etmek için grafiği kapatın.")
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_dp_matrix(score_matrix, seq1_name, seq2_name, seq1_str, seq2_str, traceback_path=None):
        """Skor matrisini ve oklarla geri izleme (traceback) yolunu görselleştirir."""
        plt.figure(figsize=(10, 8))
        
        x_labels = ["-"] + list(seq2_str)
        y_labels = ["-"] + list(seq1_str)
        
        ax = sns.heatmap(score_matrix, annot=True, cmap="coolwarm", xticklabels=x_labels, yticklabels=y_labels, fmt=".0f")
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        
        # EĞER TRACEBACK YOLU GELDİYSE OKLARI ÇİZ
        if traceback_path:
            # Traceback sağ alttan sol üste gider, okları baştan sona çizmek için listeyi ters çeviriyoruz
            path = traceback_path
            
            for k in range(len(path) - 1):
                r1, c1 = path[k]       # Başlangıç hücresi (row, col)
                r2, c2 = path[k + 1]   # Gidilecek hücre (row, col)
                
                # Seaborn heatmap'te hücre merkezleri 0.5 offsetlidir (Örn: 0. sütun x=0.5'tedir)
                x1, y1 = c1 + 0.5, r1 + 0.5
                x2, y2 = c2 + 0.5, r2 + 0.5
                
                # Hücreden hücreye siyah, kalın bir ok çiz
                ax.annotate("", 
                            xy=(x2, y2), xycoords='data',
                            xytext=(x1, y1), textcoords='data',
                            arrowprops=dict(arrowstyle="->", color="black", lw=3, shrinkA=15, shrinkB=15))

        plt.title(f"Dinamik Programlama Skor Matrisi\n({seq1_name} vs {seq2_name})", pad=20)
        
        print(f"[Bilgi] {seq1_name} ve {seq2_name} için DP Matrisi açıldı. Devam etmek için kapatın.")
        plt.tight_layout()
        plt.show()