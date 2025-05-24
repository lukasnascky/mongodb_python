from pymongo import MongoClient
from func import *

# Conexão com MongoDB Atlas
cliente = MongoClient("mongodb+srv://lucasnascimento:lusak2025@cluster0.aptlpuj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
banco = cliente.get_database("GerenciadorTarefas")
tarefas = banco.get_collection("ListaTarefas")

# Exemplo de uso
adicionar_tarefa(tarefas, "Estudar MongoDB", "Revisar operações básicas para a prova", ["estudo", "banco de dados"])

todas_tarefas = listar_tarefas(tarefas)
for tarefa in todas_tarefas:
    print("-" * 40)
    print(f"ID: {tarefa['_id']}")
    print(f"Título: {tarefa['titulo']}")
    print(f"Descrição: {tarefa['descricao']}")
    print(f"Criado em: {tarefa['criado_em'].strftime('%d/%m/%Y %H:%M')}")
    print(f"Status: {tarefa['status']}")
    print(f"Tags: {', '.join(tarefa['tags'])}")
    print(f"Comentários ({len(tarefa['comentarios'])}):")
    for comentario in tarefa['comentarios']:
        print(f"  - {comentario['texto']} ({comentario['data'].strftime('%d/%m/%Y %H:%M')})")
print("-" * 40)