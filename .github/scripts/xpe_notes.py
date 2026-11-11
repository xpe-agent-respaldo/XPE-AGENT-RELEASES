import json, os, re, sys, urllib.request
commits = [l.strip() for l in sys.stdin if l.strip()]
BRANDS = r"\b(chat ?gpt|openai|gpt-[\w.-]+|groq|cerebras|cloudflare|workers ai|hugging ?face|render|oracle|claude|anthropic|gemini|cursor|copilot|llama[\w.-]*|qwen[\w.-]*|mistral[\w.-]*|gemma[\w.-]*|scout|tauri|firestore|firebase|vite|manticore|objection|quark|snowman|ghidra|jadx|frida|angr|rizin|androguard|github|discord)\b"
notes = []
try:
    acc, tok = os.environ["CF_ACC"], os.environ["CF_TOK"]
    prompt = ("Eres el redactor de novedades de XPE Agent. Convierte estos cambios tecnicos en notas para usuarios finales, en espanol, "
              "maximo 6 vinetas cortas (una linea cada una, empezando por '- '), tono cercano y claro. PROHIBIDO nombrar empresas, modelos, "
              "proveedores, librerias o herramientas de terceros; todo se llama XPE Agent. Nada de codigos de error ni jerga tecnica. "
              "Responde SOLO con las vinetas.\n\nCambios:\n" + "\n".join(commits[:40]))
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        data=json.dumps({"messages": [{"role": "user", "content": prompt}], "max_tokens": 500, "temperature": 0.3}).encode(),
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read())
    txt = (d.get("result") or {}).get("response") or ""
    for l in txt.splitlines():
        l = l.strip()
        if l.startswith(("- ", "* ", "• ")):
            l = "- " + l[2:].strip()
            if not re.search(BRANDS, l, re.I) and re.search(r"[a-zA-Záéíóúñ]{4}", l): notes.append(l)
except Exception as e:
    print("notas IA no disponibles:", e, file=sys.stderr)
if not notes:
    notes = ["- Mejoras de rendimiento, estabilidad y seguridad en XPE Agent."]
print("\n".join(notes[:6]))
