import numpy as np

class ProgressiveAligner:
    """Rehber ağacı kullanarak dizileri aşamalı olarak hizalayan sınıf."""
    
    def __init__(self, match_score=1, mismatch_score=-1, gap_penalty=-2):
        self.match = match_score
        self.mismatch = mismatch_score
        self.gap = gap_penalty

    def _score_characters(self, char1, char2):
        """İki karakter (veya profil kolonu) arasındaki skoru hesaplar."""
        # Basit eşleşme skoru. Gelişmiş versiyonlarda BLOSUM matrisi eklenebilir.
        if char1 == '-' and char2 == '-':
            return 0  # İki boşluğu eşleştirmenin bir anlamı yok
        elif char1 == char2:
            return self.match
        else:
            return self.mismatch

    def needleman_wunsch(self, seq1, seq2):
        """İki diziyi (veya hizalanmış profili) dinamik programlama ile hizalar."""
        len1, len2 = len(seq1), len(seq2)
        
        # Skor matrisi (Score Matrix) ve Yön matrisi (Traceback Matrix) oluşturma
        score_matrix = np.zeros((len1 + 1, len2 + 1))
        
        # İlk satır ve sütunu boşluk cezaları ile doldurma
        for i in range(1, len1 + 1):
            score_matrix[i][0] = i * self.gap
        for j in range(1, len2 + 1):
            score_matrix[0][j] = j * self.gap

        # Matrisi doldurma (İleri doğru hesaplama)
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                match_val = score_matrix[i-1][j-1] + self._score_characters(seq1[i-1], seq2[j-1])
                delete_val = score_matrix[i-1][j] + self.gap
                insert_val = score_matrix[i][j-1] + self.gap
                
                score_matrix[i][j] = max(match_val, delete_val, insert_val)

        # Traceback (Geriye doğru giderek en iyi hizalamayı bulma)
        aligned_seq1, aligned_seq2 = "", ""
        i, j = len1, len2
        
        while i > 0 or j > 0:
            current_score = score_matrix[i][j]
            
            # Çaprazdan mı geldik? (Eşleşme/Mismatch)
            if i > 0 and j > 0 and current_score == score_matrix[i-1][j-1] + self._score_characters(seq1[i-1], seq2[j-1]):
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                i -= 1
                j -= 1
            # Üstten mi geldik? (seq2'ye boşluk)
            elif i > 0 and current_score == score_matrix[i-1][j] + self.gap:
                aligned_seq1 = seq1[i-1] + aligned_seq1
                aligned_seq2 = "-" + aligned_seq2
                i -= 1
            # Soldan mı geldik? (seq1'e boşluk)
            else:
                aligned_seq1 = "-" + aligned_seq1
                aligned_seq2 = seq2[j-1] + aligned_seq2
                j -= 1
                
        return aligned_seq1, aligned_seq2

    def align_tree(self, node, sequences):
        """Ağacı aşağıdan yukarıya özyinelemeli (recursive) olarak dolaşır ve hizalar."""
        # Eğer düğüm bir yapraksa, doğrudan orijinal diziyi döndür
        if node.is_leaf():
            return sequences[node.sequence_index].seq_data
            
        # Değilse, önce sol ve sağ dalları (çocukları) hizala
        left_alignment = self.align_tree(node.left, sequences)
        right_alignment = self.align_tree(node.right, sequences)
        
        # Elde edilen iki alt hizalamayı birbiriyle hizala
        aligned_left, aligned_right = self.needleman_wunsch(left_alignment, right_alignment)
        
        return aligned_left, aligned_right