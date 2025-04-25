import openai
import os
import sys
import subprocess

# Configurar cliente con OpenAI SDK v1.x
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    try:
        with open("commits.txt", "r", encoding="utf-8") as f:
            commits = f.read()

        if not commits.strip():
            print("ℹ️ No hay commits nuevos para revisar.")
            return

        print("🔍 Enviando commits a OpenAI (gpt-3.5-turbo)...\n")

        response = client.chat.completions.create(
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

        revision = response.choices[0].message.content

        print("🧠 Sugerencias de revisión:\n")
        print(revision)

        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(revision)

        # Obtener URL del PR
        pr_url = subprocess.check_output(["gh", "pr", "view", "--json", "url", "-q", ".url"]).decode().strip()
        os.environ["PR_URL"] = pr_url

    except openai.RateLimitError:
        print("⚠️ Superaste el límite de uso de la API de OpenAI.")
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write("⚠️ No se pudo completar la revisión: superaste el límite de uso de OpenAI.")

    except Exception as e:
        print("❌ Error durante la revisión:", e)
        with open("revision.txt", "w", encoding="utf-8") as out:
            out.write(f"❌ Error durante la revisión automática: {e}")
        # Evitar que falle el pipeline, pero podés descomentar si querés que corte
        # sys.exit(1)

if __name__ == "__main__":
    main()
