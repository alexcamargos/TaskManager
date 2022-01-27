from fastapi.testclient import TestClient
from fastapi import status

from src.gerenciador import app


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    client = TestClient(app)
    response = client.get('/tarefas')

    assert response.status_code == status.HTTP_200_OK
