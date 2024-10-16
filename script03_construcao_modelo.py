# Projeto 02: Pipeline para o Chatbot de atendimento ao cliente.
# Script 03 - Construção do Modelo
# Este script contém a lógica principal para a construção do chatbot utilizando o Streamlit.
# Ele configura a interface do usuário e interage com os modelos de linguagem selecionados
# para fornecer respostas às consultas dos usuários.

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv
import os
from PIL import Image 

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Streamlit
st.set_page_config(page_title="app chatbot")

# Criação de colunas para layout da página
col1, col4 = st.columns([3, 1])  # Ajusta as proporções para melhor exibição

# Configuração da primeira coluna para exibir o título do projeto
with col1:
    st.title("🤖 WAIrty Seu Chatbot")

# Carrega e exibe a imagem
if os.path.exists(r'C:\Users\Walter\Desktop\Eng_IA\14_Projetos_Experts_LLMs\Projeto_2_Chatbot\pipeline_chatbot\imagens\wairty.png'):
    image = Image.open(r'C:\Users\Walter\Desktop\Eng_IA\14_Projetos_Experts_LLMs\Projeto_2_Chatbot\pipeline_chatbot\imagens\wairty.png')
    st.image(image, use_column_width=True)
else:
    st.warning("Imagem não encontrada!")

# Define o modelo a ser utilizado
model_class = "hf_hub"  # @param ["hf_hub", "openai", "ollama"]

# Função para carregar o modelo HuggingFace Hub
def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    llm = HuggingFaceHub(
        repo_id=model,
        model_kwargs={
            "temperature": temperature,
            "return_full_text": False,
            "max_new_tokens": 512,
            # Outros parâmetros podem ser adicionados aqui
        }
    )
    return llm

# Função para carregar o modelo OpenAI
def model_openai(model="gpt-4o-mini", temperature=0.1):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature
        # Outros parâmetros podem ser adicionados aqui
    )
    return llm

# Função para carregar o modelo Ollama
def model_ollama(model="llama3.2:1b", temperature=0.1):
    llm = ChatOllama(
        model=model,
        temperature=temperature,
    )
    return llm

# Função para gerar a resposta do modelo baseado na consulta do usuário
def model_response(user_query, chat_history, model_class):
    # Carrega o modelo apropriado com base na seleção
    if model_class == "hf_hub":
        llm = model_hf_hub()
    elif model_class == "openai":
        llm = model_openai()
    elif model_class == "ollama":
        llm = model_ollama()

    # Define o prompt do sistema
    system_prompt = """
    Você é um assistente e está respondendo perguntas gerais. Responda em {language}.
    """
    language = "português"  # Define o idioma da resposta

    # Ajusta o prompt do usuário com base no modelo
    if model_class.startswith("hf"):
        user_prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    else:
        user_prompt = "{input}"

    # Cria o template do prompt
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt)
    ])

    # Cria a Chain
    chain = prompt_template | llm | StrOutputParser()

    # Retorna a resposta do modelo em formato de stream
    # Aqui, garantimos que a resposta seja convertida em string
    response_generator = chain.stream({
        "chat_history": chat_history,
        "input": user_query,
        "language": language
    })

    # Converte a resposta gerada em uma string
    response_text = "".join(list(response_generator))  # Converte o gerador em string

    return response_text

# Inicializa o histórico do chat se não existir
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Olá, sou o seu assistente virtual! Como posso ajudar você?"),
    ]

# Exibe o histórico de mensagens
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Captura a entrada do usuário
user_query = st.chat_input("Digite sua mensagem aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        # Gera a resposta do modelo
        resp = model_response(user_query, st.session_state.chat_history, model_class)
        st.session_state.chat_history.append(AIMessage(content=resp))

        # Exibe a resposta no Streamlit
        st.write(resp)

print("Script 03 executado com sucesso: Modelo construído!")  # Confirmação da execução

# Fim
