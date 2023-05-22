Projeto desenvolvido por Theo Rocha e Matheus Lopes de Souza.
Consiste em uma simulação de chamada automática usando Flask-Python, em que o professor cria uma aula e gera uma senha
e em seguida o aluno entra na aula criada e coloca a senha referente à aula. O professor tem acesso às aulas e à lista de alunos que confirmaram presença na aula.
Foi utilizado o SQL-Alchemy para manipulação dos bancos de dados.
Para executar o código, basta rodar as seguintes linhas no terminal do computador:

pip install -r requirements.txt
flask db init
flask db migrate -m "init"
flask db upgrade

e para executar com debugger on:

flask --app run run --debug
