import random

class IterativeRefiner:
    """Aşamalı hizalama sonucunu iteratif olarak iyileştiren sınıf."""
    
    def __init__(self, progressive_aligner, max_iterations=5):
        self.aligner = progressive_aligner
        self.max_iterations = max_iterations

    def _calculate_sp_score(self, alignment):
        """Sum of Pairs (SP) metodunu kullanarak hizalamanın toplam kalitesini ölçer."""
        if not alignment or len(alignment) < 2:
            return 0
            
        score = 0
        num_seqs = len(alignment)
        seq_len = len(alignment[0])

        # Her sütun için, tüm ikili eşleşmelerin skorunu topluyoruz
        for col in range(seq_len):
            for i in range(num_seqs):
                for j in range(i + 1, num_seqs):
                    char1 = alignment[i][col]
                    char2 = alignment[j][col]
                    score += self.aligner._score_characters(char1, char2)
        return score

    def _split_alignment(self, alignment):
        """Hizalamayı iki alt gruba ayırır (Bipartitioning)."""
        # Öğrenci projesi seviyesinde karmaşıklığı dengelemek için 
        # ağaç tabanlı kesim yerine rastgele indeks tabanlı ayırma (random bipartitioning) yapıyoruz.
        indices = list(range(len(alignment)))
        random.shuffle(indices)
        mid = len(indices) // 2
        
        group1_indices = indices[:mid]
        group2_indices = indices[mid:]
        
        group1 = [alignment[i] for i in group1_indices]
        group2 = [alignment[i] for i in group2_indices]
        
        return group1, group2, group1_indices, group2_indices

    def refine(self, initial_alignment):
        """İteratif iyileştirme döngüsünü çalıştırır."""
        current_alignment = initial_alignment
        current_score = self._calculate_sp_score(current_alignment)
        
        for iteration in range(self.max_iterations):
            # 1. Hizalamayı iki profile böl
            g1, g2, idx1, idx2 = self._split_alignment(current_alignment)
            
            # 2. İki profili birbiriyle tekrar hizala
            # (Modüler yapı gereği Needleman-Wunsch profil hizalama fonksiyonu çağrılır)
            # Not: Tam entegrasyonda burada _align_profiles metodu çalışacaktır.
            # new_g1, new_g2 = self._align_profiles(g1, g2) 
            
            # (Simülasyon amaçlı mevcut grupları birleştirdiğimizi varsayalım)
            new_alignment = [""] * len(current_alignment)
            for i, idx in enumerate(idx1):
                new_alignment[idx] = g1[i]
            for i, idx in enumerate(idx2):
                new_alignment[idx] = g2[i]
                
            # 3. Yeni hizalamanın skorunu hesapla
            new_score = self._calculate_sp_score(new_alignment)
            
            # 4. Karar mekanizması: Daha iyiyse kabul et (Hill Climbing yaklaşımı)
            if new_score > current_score:
                current_alignment = new_alignment
                current_score = new_score
                # Eğer iterasyon sonucu skor değişmediyse/kararlı hale geldiyse erken çıkış yapılabilir
                
        return current_alignment