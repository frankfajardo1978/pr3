import openai
import os
import sys

# Setear la API key directamente
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read()

        print("🔍 Enviando commits a OpenAI...\n")

        response = openai.ChatCompletion.create(
            model="gpt-4o",  # o usa gpt-3.5-turbo si no tenés acceso al 4 acá
            messages=[
                {
                    "role": "system",
                    "content": "Sos un revisor de código. Dado un resumen de cambios de un PR, comentá si hay algo que mejorar o si está todo bien."
                },
                {
                    "role": "user",
                    "content": f"Estos son los mensajes de commit:\n\n{commits}"
                }
            ]
        )

        print("🧠 Sugerencias de revisión:\n")
        print(response.choices[0].message["content"])

    except Exception as e:
        print("❌ Error durante la revisión:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
