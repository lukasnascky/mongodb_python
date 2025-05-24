from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# Criação de uma nova tarefa
def adicionar_tarefa(colecao, titulo, descricao, tags):
    nova_tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "criado_em": datetime.datetime.now(),
        "status": "pendente",
        "tags": tags,
        "comentarios": []
    }
    colecao.insert_one(nova_tarefa)

# Busca de tarefas com filtros opcionais
def listar_tarefas(colecao, status=None, tags=None):
    filtros = {}
    if status:
        filtros["status"] = status
    if tags:
        filtros["tags"] = {"$in": tags}
    return list(colecao.find(filtros))

# Atualização de uma tarefa existente
def modificar_tarefa(colecao, id_tarefa, dados_novos):
    colecao.update_one({"_id": ObjectId(id_tarefa)}, {"$set": dados_novos})

# Remoção de uma tarefa do banco
def remover_tarefa(colecao, id_tarefa):
    colecao.delete_one({"_id": ObjectId(id_tarefa)})

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