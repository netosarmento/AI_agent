# server.py

# 1. Importa a função para carregar o .env (necessário para a chave da OpenAI)
from dotenv import load_dotenv
load_dotenv() 

from fastapi import FastAPI, Request, HTTPException
import requests, os
from pydantic import BaseModel # Importar para definir o formato da requisição /chat
from main import criar_agente # Importa a função que cria o agente COMPLETO

# --- Configurações ---
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")

# 2. Inicializa o agente UMA VEZ, usando a função que carrega as ferramentas
# O agente deve ser criado APENAS UMA VEZ na inicialização do servidor.
try:
    AGENT = criar_agente()
except Exception as e:
    print(f"ERRO: Falha ao inicializar o Agente de IA. Verifique a chave OPENAI_API_KEY. Detalhes: {e}")
    # Se a chave estiver faltando, o AGENT será None e os endpoints retornarão 503
    AGENT = None

app = FastAPI()

# Modelo para validar o corpo da requisição do /chat
class ChatRequest(BaseModel):
    message: str

# Endpoint que o WhatsApp chamará (Webhook)
@app.post("/webhook")
async def whatsapp_webhook(req: Request):
    if not AGENT:
        raise HTTPException(status_code=503, detail="Agente de IA indisponível.")
        
    try:
        body = await req.json()
        
        # Lógica de extração de mensagem (pode ser complexa, dependendo do payload)
        # **Atenção:** O payload do WhatsApp pode variar. Esta é uma simplificação.
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        messages = changes.get("value", {}).get("messages", [])
        
        if not messages:
            return {"status": "ok", "message": "Nenhuma mensagem válida recebida."}

        message = messages[0]
        user_text = message["text"]["body"]
        from_number = message["from"]

        # 3. CORREÇÃO CRÍTICA: Usar await AGENT.arun()
        resposta = await AGENT.arun(user_text)

        # Envia resposta de volta via API do WhatsApp
        requests.post(
            f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages",
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "messaging_product": "whatsapp",
                "to": from_number,
                "text": {"body": resposta}
            }
         )
        return {"status": "ok"}
    
    except Exception as e:
        print(f"ERRO NO WEBHOOK: {e}")
        # Retorna 200 para o WhatsApp para evitar reenvio, mas loga o erro
        return {"status": "error", "detail": str(e)}


# Endpoint de Teste Local
@app.post("/chat")
async def chat_endpoint(request: ChatRequest): # Usa o modelo Pydantic para validação
    if not AGENT:
        raise HTTPException(status_code=503, detail="Agente de IA indisponível. Verifique a chave de API.")
        
    try:
        user_message = request.message
        
        # 4. CORREÇÃO CRÍTICA: Usar await AGENT.arun()
        resposta = await AGENT.arun(user_message)
        
        return {"response": resposta}
    
    except Exception as e:
        print(f"ERRO NO CHAT ENDPOINT: {e}")
        # Retorna um erro 500 para o cliente do /chat
        raise HTTPException(status_code=500, detail="Erro interno ao processar a mensagem.")
