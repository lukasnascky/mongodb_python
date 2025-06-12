from pymongo import MongoClient
from func import *
import datetime 

cliente = MongoClient(
    "mongodb+srv://ArthurSouza:210913@cluster0.dqda2cv.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)
banco = cliente.get_database("GerenciadorTarefas")
tarefas = banco.get_collection("ListaTarefas")

user_id = DEFAULT_USER_ID

while True:
    print("\n" + "-" * 40)
    print("Escolha uma opção:")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Modificar tarefa")
    print("4. Remover tarefa")
    print("5. Inserir comentário")
    print("6. Ver métricas (Redis)")
    print("7. Sair")

    opcao = input("Opção: ")

    if opcao == "1":
        print("\n" + "-" * 40)
        titulo = input("Título da tarefa: ")
        descricao = input("Descrição da tarefa: ")
        tags = input("Tags (separadas por espaço): ").split(" ")
        adicionar_tarefa(tarefas, titulo, descricao, tags)
        print("Tarefa adicionada com sucesso!")

    elif opcao == "2":
        todas_tarefas = listar_tarefas(tarefas)
        print("\n" + "-" * 40)
        for tarefa in todas_tarefas:
            print("-" * 40)
            print(f"ID: {tarefa['_id']}")
            print(f"Título: {tarefa['titulo']}")
            print(f"Descrição: {tarefa['descricao']}")
            print(f"Criado em: {tarefa['criado_em'].strftime('%d/%m/%Y %H:%M')}")
            print(f"Status: {tarefa['status']}")
            print(f"Tags: {', '.join(tarefa['tags'])}")
            print(f"Comentários ({len(tarefa['comentarios'])}):")
            for comentario in tarefa["comentarios"]:
                print(f"  - {comentario['texto']} ({comentario['data'].strftime('%d/%m/%Y %H:%M')})")

    elif opcao == "3":
        print("\n" + "-" * 40)
        id_tarefa = input("ID da tarefa a modificar: ")
        novo_status = input("Novo status (pendente/andamento/concluída): ")
        nova_descricao = input("Nova descrição: ")
        tags = input("Novas tags (separadas por vírgula): ").split(" ")
        dados_novos = {
            "status": novo_status,
            "descricao": nova_descricao,
            "tags": tags
        }
        modificar_tarefa(tarefas, id_tarefa, dados_novos)
        print("Tarefa modificada com sucesso!")

    elif opcao == "4":
        print("\n" + "-" * 40)
        id_tarefa = input("ID da tarefa a remover: ")
        remover_tarefa(tarefas, id_tarefa)
        print("Tarefa removida com sucesso!")

    elif opcao == "5":
        print("\n" + "-" * 40)
        id_tarefa = input("ID da tarefa a comentar: ")
        texto_comentario = input("Texto do comentário: ")
        inserir_comentario(tarefas, id_tarefa, texto_comentario)
        print("Comentário inserido com sucesso!")

    elif opcao == "6":
        print("\n" + "-" * 40)
        print("\nContadores de status:")
        status_hash = redis_client.hgetall(f"user:{user_id}:tasks:status")
        if not status_hash:
            print("  (nenhum dado encontrado)")
        else:
            for campo, valor in status_hash.items():
                print(f"  {campo.decode()}: {int(valor)}")

        print("\nTarefas concluídas por dia:")
        chave_completed = f"user:{user_id}:tasks:completed"
        data_hoje = datetime.datetime.now().strftime("%Y-%m-%d")
        valor_concluidas = redis_client.hget(chave_completed, data_hoje)
        qtd_concluidas = int(valor_concluidas) if valor_concluidas else 0
        print(f"  Hoje ({data_hoje}): {qtd_concluidas}")

        print("\nRanking de tags (top 10):")
        top_tags = redis_client.zrevrange(f"user:{user_id}:tags:top", 0, 9, withscores=True)
        if not top_tags:
            print("  (nenhum dado encontrado)")
        else:
            for tag, score in top_tags:
                print(f"  {tag.decode()}: {int(score)}")

        print("\nEstatísticas de produtividade:")
        
        stats = redis_client.hgetall(f"user:{user_id}:stats:productivity")
        soma_tempo = float(stats.get(b"soma_tempo_conclusao", 0))
        num_concluidas = int(stats.get(b"num_tarefas_concluidas", 0))
        tempo_medio = soma_tempo / num_concluidas if num_concluidas else 0
        print(f"  Tempo médio de conclusão (segundos): {tempo_medio:.2f}")

        chave_created = f"user:{user_id}:tasks:created"
        valor_criadas = redis_client.hget(chave_created, data_hoje)
        qtd_criadas = int(valor_criadas) if valor_criadas else 0
        print(f"  Tarefas criadas hoje: {qtd_criadas}")

        hoje = datetime.datetime.now().date()
        total_concluidas_semana = 0
        total_criadas_semana = 0
        for i in range(7):
            dia = (hoje - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            
            qc = redis_client.hget(chave_completed, dia)
            total_concluidas_semana += int(qc) if qc else 0
            
            qc2 = redis_client.hget(chave_created, dia)
            total_criadas_semana += int(qc2) if qc2 else 0

        if total_criadas_semana:
            taxa_semanal = (total_concluidas_semana / total_criadas_semana) * 100
        else:
            taxa_semanal = 0.0
        print(f"  Taxa de conclusão últimos 7 dias: {taxa_semanal:.2f}%")

    elif opcao == "7":
        print("Saindo...")
        break

    else:
        print("Opção inválida. Tente novamente.")