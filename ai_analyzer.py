import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def analiz_et(departman, sistem, gerekce, sure):
    prompt = f"""Sen bir kurumsal BT erişim talebi analiz asistanısın.
Departman: {departman}
Talep edilen sistem: {sistem}
Gerekçe: {gerekce}
Süre: {sure}

Sadece şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{{"risk_seviyesi": "düşük/orta/yüksek", "karar": "otomatik onay/yönetici onayı/güvenlik onayı", "aciklama": "kısa gerekçe"}}
"""
    response = model.generate_content(prompt)
    return response.text
