class Sequence:
    """Genetik veya protein dizilerini tutacak temel veri sınıfımız."""
    def __init__(self, header, seq_data):
        self.header = header
        self.seq_data = seq_data
        
    def __repr__(self):
        return f"<{self.header}: {self.seq_data[:10]}...>"