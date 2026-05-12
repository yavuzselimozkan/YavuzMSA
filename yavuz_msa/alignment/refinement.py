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

        for col in range(seq_len):
            for i in range(num_seqs):
                for j in range(i + 1, num_seqs):
                    char1 = alignment[i][col]
                    char2 = alignment[j][col]
                    # Az önce ProgressiveAligner'a geri eklediğimiz fonksiyonu çağırıyor
                    score += self.aligner._score_characters(char1, char2)
        return score

    def _split_alignment(self, alignment):
        """Hizalamayı iki alt gruba ayırır (Bipartitioning)."""
        indices = list(range(len(alignment)))
        random.shuffle(indices)
        mid = len(indices) // 2
        
        group1_indices = indices[:mid]
        group2_indices = indices[mid:]
        
        group1 = [alignment[i] for i in group1_indices]
        group2 = [alignment[i] for i in group2_indices]
        
        return group1, group2, group1_indices, group2_indices

    def _strip_gaps(self, profile):
        """Profildeki tamamen boşluklardan oluşan (---) gereksiz sütunları temizler."""
        if not profile: return profile
        seq_len = len(profile[0])
        valid_cols = []
        for col in range(seq_len):
            # Eğer sütundaki her karakter '-' değilse, bu sütun geçerlidir
            if any(seq[col] != '-' for seq in profile):
                valid_cols.append(col)
                
        return ["".join(seq[col] for col in valid_cols) for seq in profile]

    def refine(self, initial_alignment):
        """İteratif iyileştirme döngüsünü çalıştırır."""
        current_alignment = initial_alignment
        current_score = self._calculate_sp_score(current_alignment)
        
        for iteration in range(self.max_iterations):
            # 1. Hizalamayı iki profile böl
            g1, g2, idx1, idx2 = self._split_alignment(current_alignment)
            
            # 2. Profillerdeki ortak boşlukları temizle ki hizalama şişmesin
            clean_g1 = self._strip_gaps(g1)
            clean_g2 = self._strip_gaps(g2)
            
            # 3. GERÇEK HİZALAMA: İki profili DP ile tekrar hizala
            realigned = self.aligner.align_profiles(clean_g1, clean_g2, "Grup1", "Grup2", show_dp=False)
            
            # Hizalanmış yeni listeyi iki gruba geri ayır
            new_g1 = realigned[:len(g1)]
            new_g2 = realigned[len(g1):]
            
            # Orijinal sıraya göre birleştir
            new_alignment = [""] * len(current_alignment)
            for i, idx in enumerate(idx1):
                new_alignment[idx] = new_g1[i]
            for i, idx in enumerate(idx2):
                new_alignment[idx] = new_g2[i]
                
            # 4. Yeni hizalamanın skorunu hesapla
            new_score = self._calculate_sp_score(new_alignment)
            
            # 5. Karar mekanizması: Daha iyiyse kabul et
            if new_score > current_score:
                current_alignment = new_alignment
                current_score = new_score
                
        return current_alignment