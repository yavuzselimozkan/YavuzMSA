import numpy as np
from yavuz_msa.visualization.plot import DistanceVisualizer

class ProgressiveAligner:
    def __init__(self, match_score=1, mismatch_score=-1, gap_penalty=-2):
        self.match = match_score
        self.mismatch = mismatch_score
        self.gap = gap_penalty


    def _score_characters(self, char1, char2):
        """İki tekil karakter arasındaki skoru hesaplar (SP skoru için)."""
        if char1 == '-' and char2 == '-':
            return 0
        elif char1 == char2:
            return self.match
        else:
            return self.mismatch

    def _score_columns(self, col1, col2):
        """Birden fazla diziyi (profili) hizalarken ortalama skoru hesaplar."""
        score = 0
        count = 0
        for char1 in col1:
            for char2 in col2:
                if char1 == '-' and char2 == '-': continue
                if char1 == char2: score += self.match
                else: score += self.mismatch
                count += 1
        return score / count if count > 0 else 0

    def align_profiles(self, profile1, profile2, name1="Profil1", name2="Profil2", show_dp=False):
        """İki profili Dinamik Programlama ile hizalar."""
        if isinstance(profile1, str): profile1 = [profile1]
        if isinstance(profile2, str): profile2 = [profile2]
        
        len1, len2 = len(profile1[0]), len(profile2[0])
        score_matrix = np.zeros((len1 + 1, len2 + 1))
        
        for i in range(1, len1 + 1): score_matrix[i][0] = i * self.gap
        for j in range(1, len2 + 1): score_matrix[0][j] = j * self.gap

        # Matrisi Doldurma
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                col1 = [seq[i-1] for seq in profile1]
                col2 = [seq[j-1] for seq in profile2]
                
                match_val = score_matrix[i-1][j-1] + self._score_columns(col1, col2)
                delete_val = score_matrix[i-1][j] + self.gap
                insert_val = score_matrix[i][j-1] + self.gap
                score_matrix[i][j] = max(match_val, delete_val, insert_val)

        # Traceback (Geri İzleme) ve YOLU KAYDETME
        new_p1, new_p2 = [""] * len(profile1), [""] * len(profile2)
        i, j = len1, len2
        
        # OKLAR İÇİN: Geçtiğimiz hücrelerin koordinatlarını tutan liste
        traceback_path = [(i, j)] 
        
        while i > 0 or j > 0:
            col1 = [seq[i-1] for seq in profile1] if i > 0 else []
            col2 = [seq[j-1] for seq in profile2] if j > 0 else []
            current = score_matrix[i][j]
            
            if i > 0 and j > 0 and abs(current - (score_matrix[i-1][j-1] + self._score_columns(col1, col2))) < 1e-5:
                for k in range(len(profile1)): new_p1[k] = profile1[k][i-1] + new_p1[k]
                for k in range(len(profile2)): new_p2[k] = profile2[k][j-1] + new_p2[k]
                i -= 1; j -= 1
            elif i > 0 and abs(current - (score_matrix[i-1][j] + self.gap)) < 1e-5:
                for k in range(len(profile1)): new_p1[k] = profile1[k][i-1] + new_p1[k]
                for k in range(len(profile2)): new_p2[k] = "-" + new_p2[k]
                i -= 1
            else:
                for k in range(len(profile1)): new_p1[k] = "-" + new_p1[k]
                for k in range(len(profile2)): new_p2[k] = profile2[k][j-1] + new_p2[k]
                j -= 1
                
            # OKLAR İÇİN: Yeni hücreyi listeye ekle
            traceback_path.append((i, j))

        # EĞER İSTENİRSE DP MATRİSİNİ GÖSTER (traceback_path'i de gönderiyoruz)
        if show_dp:
            DistanceVisualizer.plot_dp_matrix(score_matrix, name1, name2, profile1[0], profile2[0], traceback_path)
                
        return new_p1 + new_p2

    def align_tree(self, node, sequences, show_dp=False):
        if node.is_leaf():
            seq_obj = sequences[node.sequence_index]
            return [seq_obj.seq_data], [seq_obj.header] # Profil listesi ve İsim listesi döner
            
        left_seqs, left_names = self.align_tree(node.left, sequences, show_dp)
        right_seqs, right_names = self.align_tree(node.right, sequences, show_dp)
        
        name1 = left_names[0] if len(left_names) == 1 else "Profil"
        name2 = right_names[0] if len(right_names) == 1 else "Profil"
        
        merged_seqs = self.align_profiles(left_seqs, right_seqs, name1, name2, show_dp)
        merged_names = left_names + right_names
        
        return merged_seqs, merged_names