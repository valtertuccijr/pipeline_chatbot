# Projeto 02: Pipeline para o Chatbot de atendimento ao cliente.
# Script 01 - Instalação de Pacotes
# Este script verifica e instala os pacotes Python necessários para o projeto, listados no arquivo
# requirements.txt. Ele permite que o projeto rode em diferentes ambientes com as dependências
# corretas, garantindo compatibilidade e facilidade de instalação para novos usuários.

import subprocess
import sys
import importlib
import pkg_resources

def instalar_pacote(pacote):
    """Verifica se o pacote está instalado; se não, instala.
    
    Args:
        pacote (str): Nome do pacote que será verificado e possivelmente instalado.
    """
    try:
        # Tenta importar o pacote. Se não estiver instalado, ocorre uma exceção ImportError
        importlib.import_module(pacote.split('==')[0])  # Remove a versão (se houver) para verificação
        print(f"{pacote} já está instalado.")
        return True  # O pacote já está instalado
    except ImportError:
        # Caso o pacote não esteja instalado, ele será instalado com pip
        print(f"{pacote} não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        return False  # O pacote foi instalado

def verificar_pillow():
    """Verifica e instala a versão correta do Pillow."""
    try:
        # Tenta importar Pillow
        pillow = importlib.import_module("PIL")  # 'PIL' é o namespace que o Pillow usa
        print("Pillow já está instalado.")
        
        # Verifica a versão do Pillow
        from PIL import Image
        print(f"Versão do Pillow instalada: {Image.__version__}")
        
        return True
    except ImportError:
        # Se não estiver instalado, tenta instalar
        print("Pillow não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        return False

def pacotes_instalados(pacotes):
    """Verifica quais pacotes estão instalados no ambiente.
    
    Args:
        pacotes (list): Lista de pacotes a serem verificados.
    
    Returns:
        list: Lista de pacotes já instalados.
    """
    instalados = {pkg.key for pkg in pkg_resources.working_set}
    return [pacote for pacote in pacotes if pacote in instalados]

def instalar_pacotes_necessarios():
    """Função que percorre a lista de pacotes e instala apenas os que estão ausentes."""
    print("Verificando e instalando pacotes necessários...")
    
    # Listagem dos pacotes do arquivo requirements.txt que serão verificados e instalados, se necessário
    pacotes = [
        "streamlit",
        "langchain",
        "langchain-huggingface",
        "langchain-ollama",
        "langchain-openai",
        "python-dotenv",
    ]
    
    # Verifica o Pillow primeiro
    verificar_pillow()
    
    # Verifica quais pacotes já estão instalados
    instalados = pacotes_instalados(pacotes)
    
    # Itera pela lista de pacotes e tenta instalá-los se estiverem ausentes
    for pacote in pacotes:
        if pacote not in instalados:
            instalar_pacote(pacote)
        else:
            print(f"{pacote} já está instalado e não será reinstalado.")

# O código abaixo garante que a função de instalação seja executada apenas
# se o script for executado diretamente, evitando execuções acidentais.
if __name__ == "__main__":
    try:
        instalar_pacotes_necessarios()
        print("Pacotes Python verificados e instalados com sucesso.")
    except Exception as e:
        print(f"Erro ao executar script01_instalacao_pacotes.py: {e}")

# Fim
