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

@tool
def hitung_kebutuhan_nutrisi(berat_badan_kg: float) -> str:
    """
    Gunakan tool ini untuk menghitung kebutuhan nutrisi harian berdasarkan berat badan.
    Input: berat_badan_kg (float) - berat badan dalam kilogram
    """
    kalori = berat_badan_kg * 30
    protein = berat_badan_kg * 1.2
    air = berat_badan_kg * 35

    return (
        f"Kebutuhan harian berdasarkan berat badan {berat_badan_kg} kg:\n"
        f"- Kalori: {kalori:.0f} kkal\n"
        f"- Protein: {protein:.1f} gram\n"
        f"- Air minum: {air:.0f} ml"
    )