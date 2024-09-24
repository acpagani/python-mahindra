import os
from random import randint
import time
from werkzeug.security import check_password_hash, generate_password_hash
from textwrap import wrap
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Chave API da Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Chave API provinda do Google AI Studio
genai.configure(api_key=GEMINI_API_KEY)

# Configuração da IA
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_LOW_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_LOW_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_LOW_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_LOW_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="""Você é a Volt, uma assistente amigável que trabalha para a plataforma E-WAY. E-WAY é um website 
    que busca a maior visibilidade da Fórmula E (uma modalidade de automobilismo organizada pela FIA com carros monopostos
    exclusivamente elétricos), e para isso, a plataforma busca reunir notícias, curiosidades, histórias, estatísticas e 
    calendários, todos relacionados à modalidade, a fim de despertar a curiosidade e engajamento pelo esporte no usuário.
    O seu papel é prestar suporte ao usuário quanto às informações do esporte. Caso não tenha acesso ao conteúdo 
    solicitado, sinalize ao usuário e recomende-o buscar outras fontes, tendendo a ser a plataforma E-WAY. Utilize uma 
    linguagem simples. As solicitações sempre tenderão a ter algum tipo de relação à Fórmula E. Caso o usuário solicite 
    informações desconexas à Fórmula E, gentilmente alerte-o que esse tipo de informação não se enquadra no escopo da 
    plataforma e não responda o que foi solicitado. """
)

chat_session = model.start_chat(
  history=[
  ]
)

# Mensagem-display do menu do chatbot
menu = """1 - Fale com a VoltAI
2 - Teste seus reflexos
3 - Reportar um problema
4 - Alternar conta
5 - Sair
Opção: """


# Função que formata textos em estilo cabeçalho
def header(txt, symbol):
    gap = len(txt) * 2
    print(f"{symbol}" * gap)
    print(txt.center(gap))
    print(f"{symbol}" * gap)


# Registrar usuário no arquivo .txt
def register(name, email, password):
    # Arquivo não foi criado ainda
    if not os.path.exists("database.txt"):
        file = open("database.txt", "x")
        file.close()

    # Ler o arquivo
    file = open("database.txt", "r")
    for line in file:
        # As seções de cada tipo de dado são divididas pelo '|' no .txt
        # O programa pega estas seções e as transforma em uma lista
        data = line.split("|")

        if data[0].strip().lower() == name.lower():
            # Nome de usuário já utilizado
            file.close()
            return False
    file.close()

    # Caso o nome ainda não tenha sido utilizado
    file = open("database.txt", "a")

    # Transformando a senha em hash
    hash_password = generate_password_hash(password)

    # Inserindo informações no arquivo seguindo a formatação
    file.write(f"{name:<10}|{email:<10}|{hash_password}|\n")

    file.close()
    # Cadastro concluído com sucesso
    return True


def login(name, password):
    # Arquivo não foi criado ainda
    if not os.path.exists("database.txt"):
        return False
    # Ler o arquivo
    file = open("database.txt", "r")

    for line in file:
        # As seções de cada tipo de dado são divididas pelo '|' no .txt
        # O programa pega estas seções e as transforma em uma lista
        data = line.split("|")

        if name.lower() == data[0].strip().lower():
            # Nome de usuário encontrado
            if check_password_hash(data[2], password):
                # Senha correspondida com o input
                file.close()
                return True
            else:
                # Senha não corresponde
                print("Senha Incorreta")
                file.close()
                return False

    file.close()
    print("Nome de usuário não encontrado")
    return False


# Itera pelo .txt dos problemas
def show_reports():
    # Arquivo não foi criado ainda
    if not os.path.exists("reports.txt"):
        file = open("reports.txt", "x")
        file.close()

    file = open("reports.txt", "r")

    # Lê cada linha
    for line in file:
        print(line, end='')

    file.close()


# Reportar um novo problema
def report_issue(user, issue):
    file = open("reports.txt", "a")

    # Formatar o problema
    file.write(f"{user:<10}|'{issue}'\n")
    file.close()
    print("Problema reportado com sucesso!")


# Minigame
def stopwatch_minigame():
    # Flag de início
    tempo_init = time.time()
    input("\033[1;37;41mAGORA: \033[m")
    # Flag final
    tempo_final = time.time()

    tempo = tempo_final - tempo_init

    return tempo


# Formatar o markdown recebido pela IA e a quebra de linha
def ai_str_format(text, len_wrap):
    # Formatar bullet points
    text = text.replace("*", "•")
    text = text.replace("••", "")
    texto = wrap(text, width=len_wrap)

    # Efeito visual de geração de texto da IA
    for linha in texto:
        for char in linha:
            print(char, end='')
            time.sleep(0.03)
        print()


def main():
    # Informações default
    logado = False
    username_session = ''
  
    while True:
        print("\n")
        header("CHATBOT FÓRMULA E", "▞")

        while not logado:
            print()
            user_in = input("Realizar cadastro/login: [C/L] ").lower().strip()

            # Realizar cadastro
            if user_in == "c":
                print()
                header("CADASTRO", "=")
                nome = input("Nome: ")
                email = input("E-mail: ")
                senha = input("Senha: ")

                if register(nome, email, senha):
                    print("Registro realizado com sucesso!\n")
                    username_session = nome
                    logado = True
                else:
                    print("Nome de usuário já utilizado!\n")

            # Realizar login
            elif user_in == "l":
                print()
                header("LOGIN", "=")
                nome = input("Nome: ")
                senha = input("Senha: ")

                if login(nome, senha):
                    print(f"Olá {nome.capitalize()}, você logou com sucesso!\n")
                    username_session = nome
                    logado = True
                    break

            # Opção não corresponde ao solicitado
            else:
                print("Opção inválida!\n")

        match input(f"{menu}\n"):
            case "1":
                print()
                # Instruindo a IA a se introduzir ao usuário
                ai_str_format(chat_session.send_message("Conte sobre você de forma breve e cativante").text, 50)
                while True:
                    print()
                    # Interação com o usuário
                    pergunta = input("Você: (Para sair, digite 'q') ")
                    print()
                    # Flag de saída
                    if pergunta == 'q':
                        break
                    resposta = chat_session.send_message(pergunta)
                    ai_str_format(resposta.text, 50)
    
            case "2":
                print()
                # Tempo randomizado para o início da contagem do teste
                begin_delay = randint(0, 6)
                # Instruções
                input("""COMO FUNCIONA: A qualquer momento, uma mensagem poderá aparecer na tela, 
                   assim que ela aparecer, você imediatamente deve pressionar a tecla \033[1menter\033[m. 
                   Quando estiver pronto, pressione enter para prosseguir """)
    
                # Ativação do minigame
                time.sleep(begin_delay)
                tempo = stopwatch_minigame()
    
                # Classificação de acordo com o tempo levado
                if tempo * 1000 <= 480:
                    resultado = "\033[1;46mMUITO RÁPIDO\033[m"
                elif 480 < tempo * 1000 <= 550:
                    resultado = "\033[1;42mRÁPIDO\033[m"
                elif 550 < tempo * 1000 <= 650:
                    resultado = "\033[1;43mBOM\033[m"
                else:
                    resultado = "\033[1;45mPrecisa melhorar...\033[m"
    
                print()
                # Output do resultado
                print(f"Tempo: {tempo * 1000:.0f} ms | Status: {resultado}")
    
            case "3":
                print()
                opt3 = int(input("""    1 - Reportar um novo problema
        2 - Consultar problemas reportados
        Opção: """))
                print()
                if opt3 == 1:
                    problema = input("Problema a reportar: ")
                    report_issue(username_session, problema)
                elif opt3 == 2:
                    show_reports()
    
            # Limpar os dados do usuário
            case "4":
                username_session = ''
                logado = False
    
            # Encerrar o programa
            case "5":
                confirm = input("Confirmar saída: [Digite 'S'] ").lower().strip()
                # Flag de saída
                if confirm == "s":
                    # Efeito visual de finalização de seção
                    header("FINALIZANDO SEÇÃO", "=")
                    for c in range(3):
                        print(".", end='')
                        time.sleep(1)
                    print()
                    header("CHAT FINALIZADO", "▞")
                    break

            case _:
                print("Opção inválida! Tente novamente.")


# Execução do programa
main()
