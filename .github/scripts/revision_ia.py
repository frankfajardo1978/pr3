import os
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_commits_from_github():
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/commits"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    commits = response.json()
    return [commit["commit"]["message"] for commit in commits]

def comentar_en_pr(mensaje):
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": mensaje}
    requests.post(url, headers=headers, json=data)

def analizar_con_gemini(commits):
    prompt = (
        "Sos un revisor técnico. A continuación te paso mensajes de commits "
        "de un Pull Request. Hacé una revisión técnica de buenas prácticas, claridad, "
        "posibles problemas o mejoras.\n\n"
        f"Commits:\n{chr(10).join(commits)}"
    )
    model = genai.GenerativeModel("models/text-bison-001")
    response = model.generate_content(prompt)
    return response.text

# Ejecución principal
try:
    commits = get_commits_from_github()
    revision = analizar_con_gemini(commits)
    comentar_en_pr("🤖 **Revisión automática con Gemini**\n\n" + revision)
except Exception as e:
    print("Error durante la revisión:", e)
    exit(1)



