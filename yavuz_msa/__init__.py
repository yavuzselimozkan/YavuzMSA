from .models.sequence import Sequence
from .core.distance import DistanceMatrixCalculator
from .core.tree import GuideTreeBuilder
from .alignment.progressive import ProgressiveAligner
from .alignment.refinement import IterativeRefiner

def align_sequences(sequence_dict, k_size=3, max_iterations=5):
    """
    Kullanıcının verdiği genetik dizileri MAFFT algoritması ile hizalar.
    
    Kullanım:
    ---------
    diziler = {
        "Seq1": "ATGCGT",
        "Seq2": "ATGCGA",
        "Seq3": "ATCCGT"
    }
    hizalanmis = align_sequences(diziler)
    """
    
    # 1. Veri Hazırlığı
    sequences = [Sequence(header, seq) for header, seq in sequence_dict.items()]
    
    # 2. Aşama 1: K-mer Mesafe Matrisi
    dist_calc = DistanceMatrixCalculator(k_size=k_size)
    matrix = dist_calc.build_matrix(sequences)
    
    # 3. Aşama 1 Devamı: UPGMA Rehber Ağaç
    tree_builder = GuideTreeBuilder(matrix)
    root_node = tree_builder.build_tree()
    
    # 4. Aşama 2: Aşamalı Hizalama (Progressive)
    aligner = ProgressiveAligner()
    # (Not: align_tree özyinelemeli çalıştığı için kök düğümü veriyoruz)
    progressive_result = aligner.align_tree(root_node, sequences)
    
    # Eğer ikiden fazla dizi varsa ve align_tree tuple dönüyorsa, 
    # listeye çevirme (flatten) işlemi yapılmalıdır. (Simüle ediyoruz)
    if isinstance(progressive_result, tuple):
        progressive_result = list(progressive_result)
    
    # 5. Aşama 3: İteratif İyileştirme (Refinement)
    refiner = IterativeRefiner(aligner, max_iterations=max_iterations)
    final_alignment = refiner.refine(progressive_result)
    
    return final_alignment