from yavuz_msa import align_sequences

def main():
    print("=== YavuzMSA Çoklu Dizi Hizalama Test Aracı ===")
    user_sequences = {}
    counter = 1
    
    while True:
        name = input(f"{counter}. Dizi Adı (Örn: Seq{counter} veya bitirmek için 'q'): ").strip()
        if name.lower() == 'q':
            break
        seq_data = input(f"{name} için diziyi girin: ").strip().upper()
        if seq_data:
            user_sequences[name] = seq_data
            counter += 1
            print("-" * 30)
            
    if len(user_sequences) < 2:
        print("Hizalama için en az 2 dizi gereklidir.")
        return

    print("\n[Bilgi] MAFFT Algoritması başlatılıyor...")
    
    # Kütüphaneyi çağırıyoruz ve görselleştirmeyi AKTİF ediyoruz
    aligned_results = align_sequences(user_sequences, show_distance_matrix=True)
    
    print("\n=== FİNAL HİZALAMA SONUCU ===")
    headers = list(user_sequences.keys())
    for i, aligned_seq in enumerate(aligned_results):
        print(f"{headers[i]:<10}: {aligned_seq}")
    print("=============================\n")

if __name__ == "__main__":
    main()

    # Seq1: ACGTCCGA
    # Seq2: ACGTCCGT
    # Seq3: ACGTGA