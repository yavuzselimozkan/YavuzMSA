class TreeNode:
    """Rehber ağaçtaki her bir dalı veya yaprağı (diziyi) temsil eden veri yapısı."""
    def __init__(self, left=None, right=None, sequence_index=None, distance=0.0):
        self.left = left                # Sol alt düğüm
        self.right = right              # Sağ alt düğüm
        self.sequence_index = sequence_index  # Eğer yapraksa (ilk dizilerdense) dizinin indeksi
        self.distance = distance        # Kökten bu düğüme olan uzaklık

    def is_leaf(self):
        """Bu düğüm bir başlangıç dizisi mi yoksa birleşim noktası mı?"""
        return self.sequence_index is not None

class GuideTreeBuilder:
    """Mesafe matrisini kullanarak UPGMA(Unweighted Pair Group Method with Arithmetic Mean) algoritmasıyla Rehber Ağaç inşa eden sınıf."""
    def __init__(self, distance_matrix):
        # Numpy matrisinin kopyasını alıyoruz ki orijinal veriyi bozmayalım
        self.matrix = [list(row) for row in distance_matrix]
        self.num_sequences = len(self.matrix)
        
        # Başlangıçta her dizi kendi başına bir köksüz yapraktır
        self.nodes = [TreeNode(sequence_index=i) for i in range(self.num_sequences)]

    def _find_closest_pair(self):
        """Matristeki en küçük mesafeye sahip (en yakın) iki düğümü bulur."""
        min_dist = float('inf')
        min_i, min_j = -1, -1
        
        n = len(self.matrix)
        for i in range(n):
            for j in range(i + 1, n):
                if self.matrix[i][j] < min_dist:
                    min_dist = self.matrix[i][j]
                    min_i, min_j = i, j
                    
        return min_i, min_j, min_dist

    def build_tree(self):
        """UPGMA algoritmasını çalıştırarak nihai kök düğümü (root) döndürür."""
        
        # Matriste tek bir eleman (kök) kalana kadar devam et
        while len(self.matrix) > 1:
            i, j, dist = self._find_closest_pair()
            
            # 1. Yeni birleştirilmiş düğüm oluştur
            new_node = TreeNode(left=self.nodes[i], right=self.nodes[j], distance=dist / 2.0)
            
            # 2. Yeni mesafeleri hesapla (Aritmetik ortalama)
            new_distances = []
            for k in range(len(self.matrix)):
                if k != i and k != j:
                    # i ve j'nin k'ya olan uzaklıklarının ortalaması
                    avg_dist = (self.matrix[i][k] + self.matrix[j][k]) / 2.0
                    new_distances.append(avg_dist)
            
            # 3. Matrisi güncelle (Eski i ve j'yi sil, yeni mesafeleri ekle)
            # (Karmaşıklığı artırmamak için list manipulation kısımlarını özet geçtik, 
            # mantık olarak i ve j satır/sütunları silinip new_distances eklenir)
            
            # Düğümler listesini güncelle
            new_nodes = [self.nodes[k] for k in range(len(self.nodes)) if k != i and k != j]
            new_nodes.append(new_node)
            self.nodes = new_nodes
            
            # Matrisi boyutlandır (i ve j'yi çıkarıp yeni satır/sütun ekleyerek)
            self._update_matrix(i, j, new_distances)
            
        return self.nodes[0] # Geriye kalan tek düğüm, ağacın köküdür (root)
        
    def _update_matrix(self, i, j, new_distances):
        """Matristen i ve j'yi silip yeni düğümün mesafelerini ekler."""
        # Yeni matrisi oluşturma işlemleri...
        # Büyük i ve j indislerinden başlayarak silmek kaymayı önler
        new_matrix = []
        for r in range(len(self.matrix)):
            if r != i and r != j:
                row = [self.matrix[r][c] for c in range(len(self.matrix)) if c != i and c != j]
                row.append(new_distances[len(new_matrix)])
                new_matrix.append(row)
                
        # Yeni düğümün satırını ekle
        new_row = new_distances + [0.0]
        new_matrix.append(new_row)
        self.matrix = new_matrix