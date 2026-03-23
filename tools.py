from langchain.tools import tool

@tool
def hitung_kalori_makanan(nama_makanan: str, jumlah_porsi: int = 1) -> str:
    """Gunakan tool ini untuk mendapatkan informasi kalori makanan Indonesia."""
    data_kalori = {
        "nasi goreng": 250,
        "telur mata sapi": 90,
        "nasi putih": 204,
        "sate ayam": 34,
    }
    makanan_key = nama_makanan.lower()
    if makanan_key in data_kalori:
        total = data_kalori[makanan_key] * jumlah_porsi
        return f"Total kalori untuk {jumlah_porsi} {nama_makanan} adalah {total} kkal."
    return f"Maaf, data kalori untuk {nama_makanan} tidak ditemukan."

@tool
def hitung_bmi(berat_kg: float, tinggi_cm: float) -> str:
    """Gunakan untuk menghitung Body Mass Index (BMI)."""
    tinggi_m = tinggi_cm / 100
    bmi = berat_kg / (tinggi_m ** 2)
    return f"BMI kamu adalah {bmi:.2f}"