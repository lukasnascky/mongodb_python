from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from redis import Redis

# Adicioanando Redis
redis_client = Redis(host='localhost', port=6379, db=0)

# Criação de uma nova tarefa
def adicionar_tarefa(colecao, titulo, descricao, tags,redis_client):
    nova_tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "criado_em": datetime.datetime.now(),
        "status": "pendente",
        "tags": tags,
        "comentarios": []
    }
    colecao.insert_one(nova_tarefa)
    # A cada nova tarefa criada, incrementa o contador no Redis
    if redis_client:
        redis_client.hincrby('tarefas', 'Criadas', 1)  

# Busca de tarefas com filtros opcionais
def listar_tarefas(colecao, status=None, tags=None):
    filtros = {}
    if status:
        filtros["status"] = status
    if tags:
        filtros["tags"] = {"$in": tags}
    return list(colecao.find(filtros))

# Atualização de uma tarefa existente
def modificar_tarefa(colecao, id_tarefa, dados_novos,redis_client):
    #Armazena atualização no banco
    result = colecao.update_one({"_id": ObjectId(id_tarefa)}, {"$set": dados_novos})
    colecao.update_one({"_id": ObjectId(id_tarefa)}, {"$set": dados_novos})
    # Incrementa o contador de modificações no Redis
    if redis_client and result.modified_count > 0:
        redis_client.hincrby('tarefas', 'modificadas', 1)

# Remoção de uma tarefa do banco
def remover_tarefa(colecao, id_tarefa,redis_client):
    #Armazena remoção no banco
    result = colecao.delete_one({"_id": ObjectId(id_tarefa)})
    colecao.delete_one({"_id": ObjectId(id_tarefa)})
    # Incrementa o contador de remoções no Redis
    if redis_client and result.deleted_count > 0:
        redis_client.hincrby('tarefas', 'removidas', 1)



# Inserção de comentário em uma tarefa específica
def inserir_comentario(colecao, id_tarefa, texto_comentario):
    comentario = {
        "texto": texto_comentario,
        "data": datetime.datetime.now()
    }
    colecao.update_one(
        {"_id": ObjectId(id_tarefa)},
        {"$push": {"comentarios": comentario}}
    )