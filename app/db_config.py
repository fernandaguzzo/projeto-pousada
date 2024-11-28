from tinydb import TinyDB, Query


db_clientes = TinyDB('data/clientes.json')
db_pousadas = TinyDB('data/pousadas.json')
db_reservas = TinyDB('data/reservas.json')
db_funcionarios = TinyDB('data/funcionarios.json')  


Cliente = Query()
Pousada = Query()
Reserva = Query()
Funcionario = Query()
