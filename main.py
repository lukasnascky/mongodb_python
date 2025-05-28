from pymongo import MongoClient
from func import *

# Conexão com MongoDB Atlas
cliente = MongoClient("mongodb+srv://ArthurSouza:210913@cluster0.dqda2cv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
banco = cliente.get_database("GerenciadorTarefas")
tarefas = banco.get_collection("ListaTarefas")


while True:
    print("\n" + "-"*40)
    print("Escolha uma opção:")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Modificar tarefa")
    print("4. Remover tarefa")
    print("5. Inserir comentário")
    print("6. Sair")
    print("7. Ver métricas (Redis):")
    opcao = input("Opção: ")

    if opcao == "1":
        print("\n" + "-"*40)
        titulo = input("Título da tarefa: ")
        descricao = input("Descrição da tarefa: ")
        tags = input("Tags (separadas por vírgula): ").split(",")
        adicionar_tarefa(tarefas, titulo, descricao, tags,redis_client)
        print("Tarefa adicionada com sucesso!")

    elif opcao == "2": 
        todas_tarefas = listar_tarefas(tarefas)
        print("\n" + "-"*40)
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

    elif opcao == "3":
        print("\n" + "-"*40)
        id_tarefa = input("ID da tarefa a modificar: ")
        novo_status = input("Novo status (pendente/concluída): ")
        nova_descricao = input("Nova descrição: ")
        tags = input("Novas tags (separadas por vírgula): ").split(",")
        modificar_tarefa(tarefas, id_tarefa, {"status": novo_status, "descricao": nova_descricao, "tags": tags},redis_client)
        print("Tarefa modificada com sucesso!")

    elif opcao == "4":
        print("\n" + "-"*40)
        id_tarefa = input("ID da tarefa a remover: ")
        remover_tarefa(tarefas, id_tarefa,redis_client)
        print("Tarefa removida com sucesso!")

    elif opcao == "5":
        print("\n" + "-"*40)
        id_tarefa = input("ID da tarefa a comentar: ")
        texto_comentario = input("Texto do comentário: ")
        inserir_comentario(tarefas, id_tarefa, texto_comentario)
        print("Comentário inserido com sucesso!")

    elif opcao == "7":
        metricas = redis_client.hgetall("task:metrics")
        print("\nMétricas:")
        for chave, valor in metricas.items():
            print(f"{chave.decode()}: {int(valor)}")


    elif opcao == "6":
        print("Saindo...")
        break
    
    else:
        print("Opção inválida. Tente novamente.")