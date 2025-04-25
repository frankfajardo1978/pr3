import os
import openai

# Inicializar cliente
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
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

        # Llamar al modelo con la nueva API
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"Sos un revisor de código. Dado un resumen de cambios de un PR, comentá si hay algo que mejorar o si está todo bien.\n\n{commits}",
            max_tokens=150  # Puedes ajustar el límite de tokens si es necesario
        )

        revision = response['choices'][0]['text'].strip()

        print("🧠 Sugerencias de revisión:\n")
        print(revision)

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

if __name__ == "__main__":
    main()
