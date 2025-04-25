import sys
import json
import os
import google.generativeai as genai

commits_file = sys.argv[1]
diff_file = sys.argv[2]

# Leer datos del PR
with open(commits_file) as f:
    commits_data = json.load(f)

with open(diff_file) as f:
    diff_text = f.read()

commit_messages = "\n".join(f"- {c['message']}" for c in commits_data["commits"])

# Inicializar Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

prompt = f"""
Quiero que actúes como revisor de código en un pull request de GitHub.
A continuación te paso los commits y los cambios propuestos.

Commits:
{commit_messages}

Cambios propuestos:
{diff_text[:4000]}  # Limita tokens para no pasarte

Decime si encontrás errores, cosas poco claras, duplicadas, mejoras posibles o estilo.
"""

response = model.generate_content(prompt)

print("Respuesta de Gemini:\n", response.text)

# Comentar en el PR
comment = f"🤖 **Revisión automática por Gemini**:\n\n{response.text}"

# Guardar como archivo temporal
with open("gemini_review.txt", "w") as f:
    f.write(comment)

# Publicar el comentario en el PR
os.system(f'gh pr comment {os.environ["GITHUB_REF"].split("/")[-1]} --body-file gemini_review.txt')
