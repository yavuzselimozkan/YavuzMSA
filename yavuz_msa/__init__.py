from .models.sequence import Sequence
from .core.distance import DistanceMatrixCalculator
from .core.tree import GuideTreeBuilder
from .alignment.progressive import ProgressiveAligner
from .alignment.refinement import IterativeRefiner
from .visualization.plot import DistanceVisualizer

def align_sequences(sequence_dict, k_size=3, max_iterations=5, show_distance_matrix=False):
    sequences = [Sequence(header, seq) for header, seq in sequence_dict.items()]
    
    dist_calc = DistanceMatrixCalculator(k_size=k_size)
    matrix = dist_calc.build_matrix(sequences)
    
    if show_distance_matrix:
        headers = list(sequence_dict.keys())
        DistanceVisualizer.plot_heatmap(matrix, headers, k_size=k_size)
    
    tree_builder = GuideTreeBuilder(matrix)
    root_node = tree_builder.build_tree()
    
    aligner = ProgressiveAligner()
    # Artık align_tree hem dizileri hem de onların karışmış sıradaki isimlerini döndürüyor
    progressive_seqs, progressive_names = aligner.align_tree(root_node, sequences, show_dp=show_distance_matrix)
    
    refiner = IterativeRefiner(aligner, max_iterations=max_iterations)
    final_alignment = refiner.refine(progressive_seqs)
    
    # KARIŞAN SIRALAMAYI ORİJİNAL GİRDİ SIRASINA (Seq1, Seq2...) GÖRE DÜZELTME
    result_dict = {}
    for name, seq in zip(progressive_names, final_alignment):
        result_dict[name] = seq
        
    ordered_results = [result_dict[header] for header in sequence_dict.keys()]
    
    return ordered_results