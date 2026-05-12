from collections import Counter
import numpy as np

class DistanceMatrixCalculator:
    """K-mer sayımı ile diziler arası mesafeyi hesaplayan sınıf."""
    def __init__(self, k_size=3):
        self.k_size = k_size

    def get_kmers(self, sequence_string):
        """Bir diziyi k-mer parçalarına ayırır ve frekanslarını sayar."""
        kmers = []
        for i in range(len(sequence_string) - self.k_size + 1):
            kmers.append(sequence_string[i : i + self.k_size])
        return Counter(kmers)

    def calculate_distance(self, seq1, seq2):
        """İki dizi arasındaki k-mer tabanlı basit Jaccard benzerliği/mesafesi hesabı."""
        kmers1 = self.get_kmers(seq1.seq_data)
        kmers2 = self.get_kmers(seq2.seq_data)
        
        # Ortak k-mer'lerin kesişimini buluyoruz
        intersection = sum((kmers1 & kmers2).values())
        union = sum((kmers1 | kmers2).values())
        
        # Jaccard Mesafesi = 1 - (Kesişim / Birleşim)
        # 0'a yakınsa çok benzer, 1'e yakınsa tamamen farklı.
        if union == 0:
            return 1.0
            
        distance = 1.0 - (intersection / union)
        return distance

    def build_matrix(self, sequences):
        """Tüm dizileri karşılaştırarak NxN boyutunda mesafe matrisi oluşturur."""
        n = len(sequences)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n): # Sadece üst üçgeni hesaplamak yeterli
                dist = self.calculate_distance(sequences[i], sequences[j])
                matrix[i][j] = dist
                matrix[j][i] = dist # Matris simetriktir
                
        return matrix