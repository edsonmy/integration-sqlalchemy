import datetime
import pprint

import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://edsonmy:<password>@cluster0.gecnhdo.mongodb.net/?retryWrites=true&w=majority")

db = client["bank"]

# definição de cliente
cliente = {
    "nome": "Maria",
    "cpf": "123456789",
    "endereco": "ABCDE",
    "conta": ({
        "tipo": "CC",
        "agencia": "0001",
        "num": 1,
        "saldo": 100
    }, {
        "tipo": "POUP",
        "agencia": "0001",
        "num": 1902,
        "saldo": 140
    })
}

# preparando para submeter as infos
clientes = db.cliente
cliente_id = clientes.insert_one(cliente).inserted_id
print(cliente_id)

# print(db.posts.find_one())
pprint.pprint(db.cliente.find_one())

#bulk inserts
new_clientes = [{
    "nome": "Jose",
    "cpf": "987654321",
    "endereco": "PLEOD",
    "conta": ({
        "tipo": "CC",
        "agencia": "0001",
        "num": 2,
        "saldo": 10
    })
}, {
    "nome": "Manoel",
    "cpf": "999999999",
    "endereco": "AAAAA",
    "conta": ({
        "tipo": "CC",
        "agencia": "0001",
        "num": 3,
        "saldo": 100
    })
}]

result = clientes.insert_many(new_clientes)
print(result.inserted_ids)

print("\nRecuperação final")
pprint.pprint(db.cliente.find_one({"nome": "Jose"}))

print("\n Documentos presentes na coleção posts")
for cliente in clientes.find():
    pprint.pprint(cliente)
    
