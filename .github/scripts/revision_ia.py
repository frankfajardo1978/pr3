import os
import openai
import sys

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        # Leer commits
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read().strip()

        if not commits:
            print("ℹ️ No hay commits nuevos para revisar.")
            with open("revision.txt", "w", encoding="utf-8") as out:
                out.write("ℹ️ No hay commits nuevos para revisar.")
            return

        print("🔍 Enviando commits a OpenAI (gpt-3.5-turbo)...\n")

        # Llamar al modelo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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

        revision = response.choices[0].message.content.strip()

        print("🧠 Sugerencias de revisión:\n")
        print(revision)

        # Guardar resultado
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(revision)

    except openai.error.RateLimitError:
        print("⚠️ Superaste el límite de uso de la API de OpenAI.")
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write("⚠️ No se pudo completar la revisión: superaste el límite de uso de OpenAI.")

    except Exception as e:
        print("❌ Error durante la revisión automática:", e)
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(f"❌ Error durante la revisión automática: {e}")
        # Podés descomentar para que el workflow falle:
        # sys.exit(1)

if __name__ == "__main__":
    main()

