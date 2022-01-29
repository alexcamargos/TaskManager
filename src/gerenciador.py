from fastapi import FastAPI
from pydantic import BaseModel, constr
from uuid import UUID, uuid4
from enum import Enum


class EstadosPossiveis(str, Enum):
    to_do = 'não finalizado'
    done = 'finalizado'


class InputTask(BaseModel):
    title: constr(min_length=3, max_length=50)
    description: constr(max_length=200)
    state: EstadosPossiveis = EstadosPossiveis.to_do


class Task(InputTask):
    id: UUID


TASKS = [
    Task(id=uuid4(),
         title='Fazer compras no supermercado',
         description='Lista de compras: leite, pão e ovos.',
         state=EstadosPossiveis.done),
    Task(id=uuid4(),
         title='Levar o cachorro ao veterinário',
         description='Consulta anual de rotina'),
    Task(id=uuid4(),
         title='Colocar as roupas na máquina para lavar',
         description=
         'Como só tenho a roupa que estou usando é urgente lavar as sujas.')
]

task_manager_app = FastAPI()


@task_manager_app.get('/task')
def get_tasks():
    return TASKS


@task_manager_app.post('/task', response_model=Task, status_code=201)
def post_task(tarefa: InputTask):

    new_task = tarefa.dict()
    new_task.update({'id': uuid4()})

    TASKS.append(new_task)

    return new_task
