from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from redis import Redis

# Configuração do Redis
redis_client = Redis(host='localhost', port=6379, db=0)
DEFAULT_USER_ID = "13"  # User id pré-definido
user_id = DEFAULT_USER_ID


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
    redis_client.hincrby(f"user:{user_id}:tasks:status", "pendente", 1)

    data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    redis_client.hincrby(f"user:{user_id}:tasks:created", data_hoje, 1)

    for tag in tags:
        redis_client.zincrby(f"user:{user_id}:tags:top", 1, tag)


def listar_tarefas(colecao, status=None, tags=None):
    filtros = {}
    if status:
        filtros["status"] = status
    if tags:
        filtros["tags"] = {"$in": tags}
    return list(colecao.find(filtros))


def modificar_tarefa(colecao, id_tarefa, dados_novos):
    tarefa_atual = colecao.find_one({"_id": ObjectId(id_tarefa)})
    if not tarefa_atual:
        return None

    status_antigo = tarefa_atual.get("status", "pendente")
    tags_antigas = tarefa_atual.get("tags", [])

    resultado = colecao.update_one(
        {"_id": ObjectId(id_tarefa)},
        {"$set": dados_novos}
    )
    if resultado.modified_count == 0:
        return None

    novo_status = dados_novos.get("status", status_antigo)
    novas_tags = dados_novos.get("tags", tags_antigas)

    if novo_status != status_antigo:
        redis_client.hincrby(f"user:{user_id}:tasks:status", status_antigo, -1)
        redis_client.hincrby(f"user:{user_id}:tasks:status", novo_status, 1)

        if novo_status == "concluida":
            data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
            redis_client.hincrby(
                f"user:{user_id}:tasks:completed",  
                data_hoje,                          
                1
            )

            criado_em = tarefa_atual.get("criado_em")
            if isinstance(criado_em, datetime.datetime):
                tempo_conclusao = (datetime.datetime.now() - criado_em).total_seconds()
                redis_client.hincrbyfloat(
                    f"user:{user_id}:stats:productivity",
                    "soma_tempo_conclusao",
                    tempo_conclusao
                )
                redis_client.hincrby(
                    f"user:{user_id}:stats:productivity",
                    "num_tarefas_concluidas",
                    1
                )

    if set(novas_tags) != set(tags_antigas):
        for tag in novas_tags:
            redis_client.zincrby(f"user:{user_id}:tags:top", 1, tag)

    return resultado


def remover_tarefa(colecao, id_tarefa):
    tarefa = colecao.find_one({"_id": ObjectId(id_tarefa)})
    if not tarefa:
        return None

    status_atual = tarefa.get("status", "pendente")
    resultado = colecao.delete_one({"_id": ObjectId(id_tarefa)})

    if resultado.deleted_count > 0:
        redis_client.hincrby(f"user:{user_id}:tasks:status", status_atual, -1)

    return resultado


def inserir_comentario(colecao, id_tarefa, texto_comentario):
    comentario = {
        "texto": texto_comentario,
        "data": datetime.datetime.now()
    }
    return colecao.update_one(
        {"_id": ObjectId(id_tarefa)},
        {"$push": {"comentarios": comentario}}
    )
