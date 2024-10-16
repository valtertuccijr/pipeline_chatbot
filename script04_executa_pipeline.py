# Projeto 02: Pipeline para o Chatbot de atendimento ao cliente.
# Script 04 - Executa Pipeline
# Este script chama os scripts anteriores que foram criados para instalar pacotes,
# carregar variáveis de ambiente e construir o modelo do chatbot.
# Ao final, ele inicia a aplicação Streamlit.

import subprocess

def executar_script(script):
    try:
        print(f"Executando {script}...")
        subprocess.run(["python", script], check=True)
        print(f"{script} executado com sucesso!")
    except subprocess.CalledProcessError:
        print(f"Erro ao executar {script}. Verifique os erros acima.")
        raise

def executar_streamlit(script):
    try:
        print(f"Executando o Streamlit para {script}...")
        subprocess.run(["streamlit", "run", script], check=True)
        print(f"{script} executado com sucesso!")
    except subprocess.CalledProcessError:
        print(f"Erro ao executar {script} com Streamlit. Verifique os erros acima.")
        raise

if __name__ == "__main__":
    try:
        executar_script("script01_instalacao_pacotes.py")
        executar_script("script02_carregamento_variaveis.py")
        executar_streamlit("script03_construcao_modelo.py")
    except Exception as e:
        print("Pipeline não foi executada com sucesso. Verifique os erros acima.")

# Fim