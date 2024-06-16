import os
from random import randint
import time
from werkzeug.security import check_password_hash, generate_password_hash
from textwrap import wrap
import google.generativeai as genai

genai.configure(api_key="AIzaSyAlcB1egvD3BYmTzmpCjBbVtOybZNl1bDk")

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

# TODO: Arrumar a questão das datas
chat_session = model.start_chat(
  history=[
  ]
)

menu = """1 - Fale com a VoltAI
2 - Teste seus reflexos
3 - Reportar um problema
4 - Alternar conta
5 - Sair
Opção: """


def header(txt, symbol):
    gap = len(txt) * 2
    print(f"{symbol}" * gap)
    print(txt.center(gap))
    print(f"{symbol}" * gap)


def register(name, email, password):
    if not os.path.exists("database.txt"):
        file = open("database.txt", "x")
        file.close()

    file = open("database.txt", "r")
    for line in file:
        data = line.split("|")

        if data[0].strip().lower() == name.lower():
            # print("Nome de usuário já utilizado!")
            file.close()
            return False
    file.close()

    file = open("database.txt", "a")
    hash_password = generate_password_hash(password)
    file.write(f"{name:<10}|{email:<10}|{hash_password}|\n")

    file.close()
    return True


def login(name, password):
    if not os.path.exists("database.txt"):
        return False

    file = open("database.txt", "r")

    for line in file:
        data = line.split("|")

        if name.lower() == data[0].strip().lower():
            if check_password_hash(data[2], password):
                file.close()
                return True
            else:
                print("Senha Incorreta")
                file.close()
                return False

    file.close()
    print("Nome de usuário não encontrado")
    return False


def show_reports():
    if not os.path.exists("reports.txt"):
        file = open("reports.txt", "x")
        file.close()

    file = open("reports.txt", "r")

    for line in file:
        print(line, end='')

    file.close()


def report_issue(user, issue):
    file = open("reports.txt", "a")

    file.write(f"{user:<10}|'{issue}'\n")
    file.close()
    print("Problema reportado com sucesso!")


def stopwatch_minigame():
    tempo_init = time.time()
    input("\033[1;37;41mAGORA: \033[m")
    tempo_final = time.time()

    tempo = tempo_final - tempo_init

    return tempo


def ai_str_format(text, len_wrap):
    # TODO: Formatar bullet points
    text = text.replace("*", "•")
    text = text.replace("••", "")
    texto = wrap(text, width=len_wrap)

    for linha in texto:
        for char in linha:
            print(char, end='')
            time.sleep(0.03)
        print()


def main():
    logado = False
    username_session = ''
    while True:
        print("\n")
        header("CHATBOT FÓRMULA E", "▞")

        while not logado:
            print()
            user_in = input("Realizar cadastro/login: [C/L] ").lower().strip()

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

            else:
                print("Opção inválida!\n")

        while True:
            opt = input(f"{menu}\n")
            if opt not in "12345":
                print("Opção inválida! Tente novamente.")
                continue
            break

        if opt == "1":
            print()
            ai_str_format(chat_session.send_message("Conte sobre você de forma breve e cativante").text, 50)
            while True:
                print()
                pergunta = input("Você: (Para sair, digite 'q') ")
                print()
                if pergunta == 'q':
                    break
                resposta = chat_session.send_message(pergunta)
                ai_str_format(resposta.text, 50)

        elif opt == "2":
            print()
            begin_delay = randint(0, 6)
            input("""COMO FUNCIONA: A qualquer momento, uma mensagem poderá aparecer na tela, 
               assim que ela aparecer, você imediatamente deve pressionar a tecla \033[1menter\033[m. 
               Quando estiver pronto, pressione enter para prosseguir """)

            time.sleep(begin_delay)
            tempo = stopwatch_minigame()

            if tempo * 1000 <= 480:
                resultado = "\033[1;46mMUITO RÁPIDO\033[m"
            elif 480 < tempo * 1000 <= 550:
                resultado = "\033[1;42mRÁPIDO\033[m"
            elif 550 < tempo * 1000 <= 650:
                resultado = "\033[1;43mBOM\033[m"
            else:
                resultado = "\033[1;45mPrecisa melhorar...\033[m"

            print()
            print(f"Tempo: {tempo * 1000:.0f} ms | Status: {resultado}")

        elif opt == "3":
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

        elif opt == "4":
            username_session = ''
            logado = False

        elif opt == "5":
            confirm = input("Confirmar saída: [Digite 'S'] ").lower().strip()
            if confirm == "s":
                header("FINALIZANDO SEÇÃO", "=")
                for c in range(3):
                    print(".", end='')
                    time.sleep(1)
                print()
                header("CHAT FINALIZADO", "▞")
                break


main()
