from google import genai

print("1. Conectando a Google Cloud...")
# Usamos tu proyecto y la región principal de siempre
client = genai.Client(vertexai=True, project="arandubot", location="us-central1")

print("2. Llamando al modelo actual (Gemini 2.5 Flash)...")
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Responde solo con la palabra: Funciona'
    )
    print("\n==========================")
    print("✅ Respuesta de la IA:", response.text)
    print("==========================\n")
except Exception as e:
    print("❌ Error:", e)