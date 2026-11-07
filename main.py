import os
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Ruang Iman - REED Engine API",
    version="2.0.0",
    description="Interactive Apologetics & Pastoral Healing RAG Engine"
)

# Membuka izin CORS agar frontend di Google Sites dapat mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Model Skema Input & Output
class QueryInput(BaseModel):
    user_id: str
    message: str

class MatrixMetrics(BaseModel):
    dimensi: str
    kondisi_input: str
    protokol_act: str
    status_vektor: str

class REEDResponse(BaseModel):
    direct_answer: str
    matrix_table: List[MatrixMetrics]
    synthesis: str
    closing: str

# 2. Classifier / Routing Logika Teologis
def classify_and_route(message: str) -> Dict[str, Any]:
    msg_lower = message.lower()
    
    emotional_keywords = ["marah", "kecewa", "depresi", "kehilangan", "putus asa", "sedih", "mati", "kejam", "sakit", "takut"]
    intellectual_keywords = ["kontradiksi", "sejarah", "dogma", "sains", "manuskrip", "bukti", "logis", "salah", "alkitab", "tuhan"]
    
    is_emotional = any(kw in msg_lower for kw in emotional_keywords)
    is_intellectual = any(kw in msg_lower for kw in intellectual_keywords)
    
    if is_emotional:
        return {
            "route": "PASTORAL-FIRST-EMPATHY-OVERRIDE",
            "balancer": "Pastoral 80% | Apologetics 20%"
        }
    elif is_intellectual:
        return {
            "route": "M4-HIGH-VERACITY-APOLOGETICS",
            "balancer": "Apologetics 70% | Pastoral 30%"
        }
    else:
        return {
            "route": "STANDARD-COVENANTAL-BALANCE",
            "balancer": "Pastoral 50% | Apologetics 50%"
        }

# 3. Endpoint Utama
@app.get("/")
def home():
    return {"status": "Online", "service": "Ruang Iman REED Engine API"}

@app.post("/api/v2/chat", response_model=REEDResponse)
async def process_reed_engine(payload: QueryInput):
    try:
        routing_config = classify_and_route(payload.message)
        
        if routing_config["route"] == "PASTORAL-FIRST-EMPATHY-OVERRIDE":
            response_data = REEDResponse(
                direct_answer="Saya mendengar jeritan hati Anda, dan ketahuilah bahwa Allah tidak sedang menjauh atau menghukum Anda di tengah badai ini.",
                matrix_table=[
                    MatrixMetrics(dimensi="Kondisi Jiwa", kondisi_input="Hancur & Terluka", protokol_act="Asymmetric Comfort Integration", status_vektor="Ditopang Dekapan-Nya"),
                    MatrixMetrics(dimensi="Persepsi Diri", kondisi_input="Merasa Ditinggalkan", protokol_act="SAB Lock (M_merit = 0)", status_vektor="Kasih Karunia Mutlak"),
                    MatrixMetrics(dimensi="Serangan Jiwa", kondisi_input="Malware Keputusasaan", protokol_act="Pembersihan Firmware (-γ)", status_vektor="Agape Gain Infusion Max")
                ],
                synthesis="Secara pastoral, air mata Anda adalah bejana yang berharga di hadapan Tuhan. Kristus telah merasakan titik tergelap dari rasa ditinggalkan agar Anda tidak pernah sendirian.",
                closing="Teduhlah di dalam kasih-Nya. Buluh yang patah tidak akan dipatahkan oleh-Nya."
            )
        else:
            response_data = REEDResponse(
                direct_answer="Pencarian kebenaran intelektual Anda tidak bertentangan dengan iman, karena seluruh kebenaran objektif berakar pada Allah Logos.",
                matrix_table=[
                    MatrixMetrics(dimensi="Logika Iman", kondisi_input="Paradoks / Skeptis", protokol_act="Penyelarasan Kosmis TIMSK", status_vektor="Iman Berakal Budi"),
                    MatrixMetrics(dimensi="Filter Doktrin", kondisi_input="Malware Reduksionisme", protokol_act="Eliminasi Firmware Otomatis", status_vektor="Akurasi Manuskrip Murni"),
                    MatrixMetrics(dimensi="Kedaulatan", kondisi_input="Keraguan Akademis", protokol_act="Transmutasi Asimetris (ACT)", status_vektor="Divine Order Terjaga")
                ],
                synthesis="Secara apologetis, setiap pertanyaan logis memiliki jawaban teologis yang kokoh. Uji sejarah menunjukkan transmisi teks firman-Nya berdiri di atas fondasi manuskrip yang valid.",
                closing="Tetaplah mencari dengan hati yang jujur. Kebenaran-Nya tidak pernah takut untuk diuji."
            )
            
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
