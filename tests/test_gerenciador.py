from fastapi.testclient import TestClient
from fastapi import status

from src.gerenciador import TASKS, Task, task_manager_app


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    client = TestClient(task_manager_app)

    response = client.get('/task')
    assert response.status_code == status.HTTP_200_OK


def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    client = TestClient(task_manager_app)

    response = client.get('/task')
    assert response.headers['Content-Type'] == 'application/json'


def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    client = TestClient(task_manager_app)

    response = client.get('/task')
    assert isinstance(response.json(), list)


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_ID():
    client = TestClient(task_manager_app)
    TASKS.append({'id': 1})

    response = client.get('/task')
    assert 'id' in response.json().pop()

    TASKS.clear()


def test_quanto_listar_tarefas_a_tarefa_deve_possuir_titulo():
    client = TestClient(task_manager_app)
    TASKS.append({'title': 'Exemplo de Título'})

    response = client.get('/task')
    assert 'title' in response.json().pop()

    TASKS.clear()


def test_quando_listar_tarefas_a_tarefa_deve_possuir_descrição():
    client = TestClient(task_manager_app)
    TASKS.append({"description": 'Exemplo de descrição'})

    response = client.get('/task')
    assert "description" in response.json().pop()

    TASKS.clear()


def test_quando_listar_tarefas_a_tarefa_deve_possuir_estado():
    TASKS.append({'state': 'Exemplo de estado'})
    client = TestClient(task_manager_app)

    response = client.get('/task')
    assert 'state' in response.json().pop()

    TASKS.clear()


def test_recurso_tarefas_deve_aceitar_o_verbo_POST():
    client = TestClient(task_manager_app)

    response = client.post('/task')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo():
    client = TestClient(task_manager_app)

    response = client.post('/task', json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    client = TestClient(task_manager_app)

    response = client.post('/task', json={'title': '*' * 2})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post('/task', json={'title': '*' * 51})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_uma_tarefa_e_submetida_deve_possuir_uma_descricao():
    client = TestClient(task_manager_app)

    response = client.post('/task', json={'title': 'Título'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_descrição_da_tarefa_pode_conter_no_maximo_200_caracteres():
    client = TestClient(task_manager_app)

    response = client.post('/task',
                           json={
                               'title': 'Título',
                               "description": '*' * 201
                           })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
    client = TestClient(task_manager_app)
    task = {
        'title': 'Título de exemplo',
        "description": "Descrição de exemplo.",
        'state': 'não finalizado'
    }

    response = client.post('/task', json=task)
    assert response.json()['title'] == task['title'] and \
           response.json()['description'] == task['description'] and \
           response.json()['state'] == task['state']


def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
    client = TestClient(task_manager_app)
    task_1 = {
        'title': 'Exemplo de Título',
        "description": 'Exemplo de descrição',
    }
    task_2 = {
        'title': 'Exemplo de Título',
        "description": 'Exemplo de descrição',
    }

    response_1 = client.post('/task', json=task_1)
    response_2 = client.post('/task', json=task_2)

    assert response_1.json()['id'] != response_2.json()['id']


def test_quando_criar_uma_tarefa_seu_estado_padrao_deve_ser_nao_finalizado():
    client = TestClient(task_manager_app)
    task = {
        'title': 'Exemplo de Título',
        "description": 'Exemplo de descrição'
    }

    response = client.post('/task', json=task)
    assert response.json()['state'] == 'não finalizado'


def test_quando_criar_uma_tarefa_codigo_de_status_retornado_deve_ser_201():
    client = TestClient(task_manager_app)
    task = {
        'title': 'Exemplo de Título',
        "description": 'Exemplo de descrição.'
    }

    response = client.post('/task', json=task)

    assert response.status_code == status.HTTP_201_CREATED


def test_quando_criar_uma_nova_tarefa_a_mesma_deve_ser_persistida():
    client = TestClient(task_manager_app)

    task = {
        'title': 'Exemplo de Título',
        'description': 'Exemplo de descrição'
    }
    response = client.post('/task', json=task)

    print(response.json())

    assert response.status_code == status.HTTP_201_CREATED and len(TASKS) == 6

    TASKS.clear()
