# Projeto 02: Pipeline para o Chatbot de atendimento ao cliente.
# Script 02 - Carregamento de Variáveis de Ambiente
# Este script carrega as variáveis de ambiente do arquivo .env, permitindo o uso de configurações
# sensíveis e específicas do ambiente no projeto, como chaves de API.

from dotenv import load_dotenv
import os

def carregar_variaveis_ambiente():
    """
    Carrega as variáveis de ambiente do arquivo .env para o ambiente atual.
    Isso permite acessar as variáveis de ambiente definidas no arquivo .env
    sem precisar codificá-las diretamente no código.
    """
    load_dotenv()  # Carrega as variáveis do arquivo .env

    # Verifica se as chaves necessárias foram carregadas
    required_keys = ["HUGGINGFACE_API_KEY", "OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if os.getenv(key) is None]

    if missing_keys:
        print(f"Erro: As seguintes chaves estão ausentes no .env: {', '.join(missing_keys)}")
    else:
        print("Todas as variáveis de ambiente necessárias foram carregadas com sucesso!")

# Função principal para execução do carregamento
if __name__ == "__main__":
    carregar_variaveis_ambiente()  # Chama a função para carregar as variáveis
    print("Script 02 executado com sucesso: Variáveis de ambiente carregadas!")  # Confirmação da execução

# Fim
