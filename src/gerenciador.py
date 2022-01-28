from fastapi import FastAPI

app = FastAPI()

TAREFAS = [
    {
        "id": "1",
        "titulo": "Fazer compras no supermercado",
        "descrição": "Lista de compras: leite, pão e ovos.",
        "estado": "não finalizado",
    },
    {
        "id": "2",
        "titulo": "Levar o cachorro para tosar",
        "descrição": "Como estamos o verão e o pet está muito peludo, faz-se necessário.",
        "estado": "não finalizado",
    },
    {
        "id": "3",
        "titulo": "Colocar as roupas na máquina para lavar",
        "descrição": "Como só tenho a roupa que estou usando é urgente lavar as sujas.",
        "estado": "não finalizado",
    },
]


@app.get('/tarefas')
def listar():
    return TAREFAS
