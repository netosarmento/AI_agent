"""
Agente de IA de Vendas e Atendimento
-------------------------------------
Autor: Neto Sarmento 📌
Descrição:
  - Atende clientes de forma amigável e profissional.
  - Cumprimenta com base no horário.
  - Apresenta menu de opções de serviço.
  - Usa ferramentas (Tools) para buscar produtos, verificar status, etc.
  - Estrutura modular, pronta para integração com FastAPI e WhatsApp API.
"""
# ============================
# 🌍 Carregando Variáveis de Ambiente
# ============================

from dotenv import load_dotenv
load_dotenv()

# ============================
# 📚 Importações e dependências
# ============================
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool
from datetime import datetime
import random


# =====================================
# 🧰 Ferramentas simuladas (exemplos)
# =====================================

@tool
async def search_product(product_name: str):
    """
    Busca um produto no catálogo e retorna suas informações.
    Use esta ferramenta para consultar detalhes como preço, estoque e descrição de produtos.
    """
    # ⚠️ Substituir por uma chamada real ao banco de dados ou API de produtos
    print(f"🔎 Buscando pelo produto: {product_name}...") # Adicionado para depuração
    
    fake_catalog = {
        "notebook": {"price": 3500.00, "stock": 5, "description": "Notebook ultrafino, 16GB RAM, SSD 512GB."},
        "smartphone": {"price": 1999.99, "stock": 10, "description": "Smartphone 128GB, câmera tripla e 5G."},
        "fone": {"price": 299.90, "stock": 25, "description": "Fone Bluetooth com cancelamento de ruído."}
    }

    produto = fake_catalog.get(product_name.lower())
    if produto:
        return (f"🔍 Produto encontrado: {product_name.title()}\n"
                f"💰 Preço: R${produto['price']:.2f}\n"
                f"📦 Estoque: {produto['stock']} unidades\n"
                f"ℹ️ {produto['description']}")
    else:
        return f"❌ Não encontrei o produto '{product_name}'. Deseja ver opções semelhantes?"


# ==================================================
# 🤖 Função para criar um agente com mais contexto
# ==================================================

def criar_agente():
    """
    Cria e retorna o agente configurado.
    Adicione novas Tools ou memória conforme evoluir o projeto.
    """

    # Aqui você pode adicionar outras Tools:
    # - Tool para verificar status do pedido
    # - Tool para cancelar compra
    # - Tool para abrir reclamação
    # - Tool para enviar informações de pagamento
    # Cada uma herda de 'Tool' e implementa o método 'run(...)'
    tools = [search_product]

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        description=(
            "Sou um agente virtual de vendas e suporte da empresa X. "
            "Ajudo clientes com informações sobre produtos, pedidos e suporte. "
            "Mantenho sempre um tom educado, simpático e profissional."
        ),
        tools=tools,
        markdown=True
    )

    return agent


# ========================================
# 👋 Lógica de saudação e introdução
# ========================================

def saudacao_inicial():
    """
    Gera uma saudação amigável de acordo com o horário.
    """

    hora = datetime.now().hour
    if 5 <= hora < 12:
        saudacao = "🌅 Bom dia!"
    elif 12 <= hora < 18:
        saudacao = "☀️ Boa tarde!"
    else:
        saudacao = "🌙 Boa noite!"

    introducoes = [
        f"{saudacao} Sou o assistente virtual da nossa loja. Como posso te ajudar hoje?",
        f"{saudacao} Bem-vindo(a) à nossa loja! 😊 Estou aqui para te ajudar com suas compras.",
        f"{saudacao} Que bom ter você por aqui! Vamos resolver o que precisar agora mesmo."
    ]

    return random.choice(introducoes)


def mostrar_menu():
    """
    Exibe as opções principais de atendimento.
    """
    menu = (
        "\n💬 Posso te ajudar com uma dessas opções:\n"
        "1️⃣ Ver produtos\n"
        "2️⃣ Informações da compra\n"
        "3️⃣ Status do pedido\n"
        "4️⃣ Fazer uma reclamação\n"
        "5️⃣ Cancelar uma compra\n"
        "Digite o número ou nome da opção desejada:"
    )
    return menu


# ===========================
# 🚀 Execução principal
# ===========================

def main():
    agente = criar_agente()

    # Introdução automática
    print(saudacao_inicial())
    print(mostrar_menu())

    # Captura a opção do usuário
    user_input = input("\nVocê: ").strip().lower()

    # Processa a escolha inicial
    if user_input in ["1", "ver produtos", "produtos"]:
        produto = input("Qual produto você procura? ").strip()
        resposta = agente.run(f"Buscar informações sobre o produto {produto}")
        print(f"\n🤖 Agente: {resposta}")

    elif user_input in ["2", "informações", "compra"]:
        print("\n🤖 Agente: Para ver informações da sua compra, informe o número do pedido.")
        pedido = input("Número do pedido: ")
        print(f"🔎 (Simulação) Consultando pedido {pedido}... [integre com API futuramente]")

    elif user_input in ["3", "status", "pedido"]:
        print("\n🤖 Agente: Claro! Me diga o número do seu pedido para verificar o status.")
        pedido = input("Número do pedido: ")
        print(f"📦 Pedido {pedido} está 'Em transporte'. (Exemplo fixo, conecte com sua API real)")

    elif user_input in ["4", "reclamação"]:
        print("\n🤖 Agente: Lamento saber disso 😞. Por favor, descreva brevemente o problema.")
        reclamacao = input("Sua reclamação: ")
        print(f"📩 Obrigado por compartilhar. Já registrei sua reclamação: '{reclamacao}'")

    elif user_input in ["5", "cancelar", "cancelar compra"]:
        print("\n🤖 Agente: Entendido! Informe o número do pedido que deseja cancelar.")
        pedido = input("Número do pedido: ")
        print(f"⚠️ Pedido {pedido} foi cancelado com sucesso. (Simulação)")

    else:
        print("\n🤖 Agente: Desculpe, não entendi sua escolha. Tente digitar o número da opção.")


# ===========================
# 🏁 Execução
# ===========================

if __name__ == "__main__":
  #  import asyncio
    main()
  #  agent = criar_agente()
  #  user_input = "Oi, quero ver os produtos!"
  #  response = asyncio.run(agent.run(user_input))
  #  print("Agente:", response)

