# SPRINT 1: ENTREGA DE PYTHON
## Chatbot para a plataforma *E-WAY*

### Integrantes:
#### Arthur Cotrick Pagani - RM554510
#### Diogo Leles Franciulli - RM558487
#### Felipe Sousa de Oliveira - RM559085
#### Ryan Brito Pereira Ramos - RM554497

***
 
### Detalhes do Projeto
Buscamos desenvolver um chatbot com funcionalidades diversas relacionadadas à fórmula E. 
A ideia principal é eventualmente trazer estas funcionalidades à plataforma E-WAY, a nossa
proposta de projeto do Challenge. Portanto, utilizamos a linguagem Python para prototipar e testar
tais funcionalidades.
Desenvolvemos primeiramente um sistema que se aproxima de um login/cadastro
no chatbot. Logo que o programa é iniciado, esses dados são solicitados ao usuário.  
Caso o usuário opte por *cadastro* na plataforma, terá de preencher:
* Nome
* E-mail
* Senha

Caso tente fazer login sem um cadastro prévio, o chatbot não poderá ser acessado,
o cadastro inicial é mandatório. Esses dados são armazenados em arquivos .txt, 
simulando um **banco de dados**, todos colocados e lidos através de conceitos 
de manipulação de arquivos em python.

E não se esqueça da senha que colocar! Depois de inserida, ela será armazenada no
"Banco de dados" de forma totalmente criptografada, e apenas o programa terá acesso
à chave.

**Após o cadastro ou login com dados já registrados no banco, o chatbot será inicializado**

Dentro do chatbot, o usuário irá se deparar com 5 opções:
* Fale com a VoltAI
* Teste seus reflexos
* Reportar um problema
* Alternar conta
* Sair

***

### Funcionalidades
Para cada opção, haverá um índice numérico. O número correspondente que o usuário digitar
será aquele escolhido para dar seguimento à execução.  

**Na opção 1**, nós decidimos inovar. Criamos uma Inteligência Artificial especializada em Fórmula E,
e que depois será integrada de fato à nossa plataforma web - **A VoltAI**.  
Você pode fazer perguntas, conversar, pedir curiosidades, se divirta! Ela vai te ajudar.
Colocamos filtros de assuntos desconexos ao esporte e a vocabulários desrespeitosos.

**Na opção 2**, você irá se deparar com um minijogo! Como um bom piloto de Fórmula E, os seus reflexos
devem ser bastante aguçados, e é justamente isso que vai treinar lá. Logo que acessar a opção, terá acesso
às instruções, dê o seu melhor!

Você pode utilizar a **opção 3** caso se depare com algum problema no programa. Essa funcionalidade também funciona
através da manipulação de arquivos. Ao registrar um novo problema, o programa o registra junto ao seu nome 
de usuário, que é armazenado logo no início, para sabermos quem está ou estava tendo o problema.  
Além disso, você pode também consultar os problemas já reportados anteriormente, para ver se outra pessoa já passou
por isso antes!

**Na opção 4**, buscamos trazer a ideia de "Log Out", seu usuário é "esquecido" pelo programa e ele volta à tela
de login. Mas lembre-se, o programa pode ter "esquecido" o seu login, mas seus dados de cadastro ainda estão no
arquivo de texto, o nosso "banco de dados", então se quiser entrar com esses dados de novo, mesmo depois de encerrar 
o programa e começá-lo novamente, você pode!

E por fim, na **opção 5**, você tem a possibilidade de encerrar o programa. Após a escolha da opção, ainda há uma confirmação
de saída do usuário. Após a confirmação, um timer é ativado, e quando finalizado, o programa se encerra.

***

### Requisitos
Para o funcionamento de todas as funcionalidades citadas acima, você precisará ter os seguintes *imports*:
* import os  
* from random import randint  
* import time  
* from werkzeug.security import check_password_hash, generate_password_hash  
* from textwrap import wrap  
* import google.generativeai as genai  

***

### Observação
A VoltAI foi feita através da plataforma **Google AI Studio**, criamos um prompt adequado e importamos as dependências
dela para o código através de uma chave API gerada pela plataforma, tudo de acordo com as normas de utilização explicitadas
pela provedora.

