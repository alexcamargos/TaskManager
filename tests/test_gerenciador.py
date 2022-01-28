from http import client
from urllib import response
from fastapi.testclient import TestClient
from fastapi import status

from src.gerenciador import TAREFAS, app


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    client = TestClient(app)
    response = client.get('/tarefas')

    assert response.status_code == status.HTTP_200_OK

def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    client = TestClient(app)
    response = client.get('/tarefas')

    assert response.headers['Content-Type'] == 'application/json'

def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    client = TestClient(app)
    response = client.get('/tarefas')

    assert isinstance(response.json(), list)

def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_ID():
    TAREFAS.append({'id':1})
    client = TestClient(app)
    response = client.get('/tarefas')

    assert 'id' in response.json().pop()

    TAREFAS.clear()

def test_quanto_listar_tarefas_a_tarefa_deve_possuir_titulo():
    TAREFAS.append({'titulo':'Exemplo de Título'})
    client = TestClient(app)
    response = client.get('/tarefas')

    assert 'titulo' in response.json().pop()

    TAREFAS.clear()

def test_quando_listar_tarefas_a_tarefa_deve_possuir_descrição():
    TAREFAS.append({'descrição':'Exemplo de descrição'})
    client = TestClient(app)
    response = client.get('/tarefas')

    assert 'descrição' in response.json().pop()

    TAREFAS.clear()

def test_quando_listar_tarefas_a_tarefa_deve_possuir_estado():
    TAREFAS.append({'estado':'Exemplo de estado'})
    client = TestClient(app)
    response = client.get('/tarefas')

    assert 'estado' in response.json().pop()

    TAREFAS.clear()