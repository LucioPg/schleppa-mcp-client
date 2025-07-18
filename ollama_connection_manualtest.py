import os
import asyncio
from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import requests
import json

# Carica le variabili d'ambiente
load_dotenv()


class OllamaChat:
    def __init__(self):
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.base_url = "http://localhost:11434"
        self.chat_model = None
        self.conversation_history = []

    def initialize_model(self):
        """Inizializza il modello ChatOllama"""
        try:
            self.chat_model = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.7,
                top_p=0.9,
                #num_predict=256,  # Limite di token per la risposta
                verbose=True
            )
            print(f"✓ Modello {self.model_name} inizializzato correttamente")
            return True
        except Exception as e:
            print(f"✗ Errore nell'inizializzazione del modello: {e}")
            return False

    def check_ollama_connection(self):
        """Verifica se Ollama è in esecuzione"""
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            if response.status_code == 200:
                version_info = response.json()
                print(f"✓ Ollama è in esecuzione - Versione: {version_info.get('version', 'Unknown')}")
                return True
            else:
                print(f"✗ Ollama non risponde correttamente (Status: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Impossibile connettersi a Ollama: {e}")
            return False

    def check_model_availability(self):
        """Verifica se il modello è disponibile"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                available_models = [model['name'] for model in models.get('models', [])]

                if self.model_name in available_models:
                    print(f"✓ Modello {self.model_name} è disponibile")
                    return True
                else:
                    print(f"✗ Modello {self.model_name} non trovato")
                    print(f"Modelli disponibili: {available_models}")
                    return False
            else:
                print(f"✗ Errore nel recupero dei modelli (Status: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Errore nella verifica dei modelli: {e}")
            return False

    def simple_chat(self, message):
        """Chat semplice con una singola domanda"""
        try:
            human_message = HumanMessage(content=message)
            response = self.chat_model.invoke([human_message])
            return response.content
        except Exception as e:
            return f"Errore: {e}"

    def chat_with_system_prompt(self, message, system_prompt="Sei un assistente AI utile e cordiale."):
        """Chat con system prompt personalizzato"""
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            response = self.chat_model.invoke(messages)
            return response.content
        except Exception as e:
            return f"Errore: {e}"

    def conversational_chat(self, message):
        """Chat conversazionale che mantiene la cronologia"""
        try:
            # Aggiungi il messaggio dell'utente alla cronologia
            self.conversation_history.append(HumanMessage(content=message))

            # Limita la cronologia per evitare di superare il context window
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            # Invia tutti i messaggi della cronologia
            response = self.chat_model.invoke(self.conversation_history)

            # Aggiungi la risposta del modello alla cronologia
            self.conversation_history.append(response)

            return response.content
        except Exception as e:
            return f"Errore: {e}"

    def reset_conversation(self):
        """Resetta la cronologia della conversazione"""
        self.conversation_history = []
        print("Cronologia della conversazione resettata.")

    def get_model_info(self):
        """Ottieni informazioni sul modello"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": self.model_name},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


def test_basic_functionality():
    """Test delle funzionalità di base"""
    print("=== Test Funzionalità Base ===")

    chat = OllamaChat()

    # Verifica connessione
    if not chat.check_ollama_connection():
        return False

    # Verifica disponibilità modello
    if not chat.check_model_availability():
        return False

    # Inizializza modello
    if not chat.initialize_model():
        return False

    # Test semplice
    print("\n--- Test Chat Semplice ---")
    response = chat.simple_chat("Ciao! Rispondi solo con 'Ciao!'")
    print(f"Risposta: {response}")

    # Test con system prompt
    print("\n--- Test con System Prompt ---")
    response = chat.chat_with_system_prompt(
        "Cos'è Python?",
        "Sei un esperto programmatore. Rispondi in modo tecnico ma comprensibile."
    )
    print(f"Risposta: {response}")

    return True


def interactive_chat():
    """Chat interattiva"""
    print("=== Chat Interattiva con Ollama ===")

    chat = OllamaChat()

    # Setup iniziale
    if not chat.check_ollama_connection():
        return

    if not chat.check_model_availability():
        return

    if not chat.initialize_model():
        print("Errore durante l'inizializzazione del modello. Riprova.")
        return

    # Informazioni sul modello
    model_info = chat.get_model_info()
    if "error" not in model_info:
        print(f"Modello: {model_info.get('details', {}).get('family', 'Unknown')}")
        print(f"Parametri: {model_info.get('details', {}).get('parameter_size', 'Unknown')}")

    print("\nComandi disponibili:")
    print("  /quit - Esci dalla chat")
    print("  /reset - Resetta la conversazione")
    print("  /info - Mostra informazioni sul modello")
    print("  /help - Mostra questo messaggio")

    while True:
        try:
            user_input = input("\nTu: ").strip()

            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("Arrivederci!")
                break
            elif user_input.lower() in ['/reset', '/r']:
                chat.reset_conversation()
                continue
            elif user_input.lower() in ['/info', '/i']:
                info = chat.get_model_info()
                print(f"Informazioni modello: {json.dumps(info, indent=2)}")
                continue
            elif user_input.lower() in ['/help', '/h']:
                print("\nComandi disponibili:")
                print("  /quit - Esci dalla chat")
                print("  /reset - Resetta la conversazione")
                print("  /info - Mostra informazioni sul modello")
                print("  /help - Mostra questo messaggio")
                continue
            elif not user_input:
                continue

            print("Ollama: Sto pensando...")
            response = chat.conversational_chat(user_input)
            print(f"Ollama: {response}")

        except KeyboardInterrupt:
            print("\nInterrotto dall'utente. Arrivederci!")
            break
        except Exception as e:
            print(f"Errore: {e}")


def batch_test():
    """Test batch con domande predefinite"""
    print("=== Test Batch ===")

    chat = OllamaChat()

    if not chat.check_ollama_connection():
        return

    if not chat.check_model_availability():
        return

    if not chat.initialize_model():
        return

    test_questions = [
        "Qual è la capitale dell'Italia?",
        "Spiegami cos'è il machine learning in parole semplici",
        "Scrivi un haiku sul caffè",
        "Traduci 'Ciao come stai?' in inglese",
        "Risolvi questa equazione: 2x + 5 = 15"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Domanda {i}: {question} ---")
        response = chat.simple_chat(question)
        print(f"Risposta: {response}")
        print("-" * 50)


def main():
    """Funzione principale"""
    print("Script di Test ChatOllama")
    print("========================")

    while True:
        print("\nScegli un'opzione:")
        print("1. Test funzionalità base")
        print("2. Chat interattiva")
        print("3. Test batch")
        print("4. Esci")

        choice = input("Scelta (1-4): ").strip()

        if choice == '1':
            test_basic_functionality()
        elif choice == '2':
            interactive_chat()
        elif choice == '3':
            batch_test()
        elif choice == '4':
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()