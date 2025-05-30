from transacao import adicionar_transacao, listar_transacoes, calcular_resumo, filtrar_por_data
from datetime import datetime

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_adicionar_transacao()
        elif opcao == "2":
            menu_listar_transacoes()
        elif opcao == "3":
            menu_exibir_resumo()
        elif opcao == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def exibir_menu():
    print("\n=== Gerenciador Financeiro ===\n")
    print("1. Adicionar Transação")
    print("2. Listar Transações")
    print("3. Exibir Resumo Financeiro")
    print("4. Sair\n")
    print("==============================")


def menu_adicionar_transacao():
    print("\n[Adicionar Transação]")
    tipo = input("Tipo (receita/despesa): ").strip().lower()
    while tipo not in ["receita", "despesa"]:
        print("Tipo inválido. Digite 'receita' ou 'despesa'.")
        tipo = input("Tipo (receita/despesa): ").strip().lower()

    categoria = input("Categoria: ").strip()
    while not categoria:
        print("Categoria não pode estar vazia.")
        categoria = input("Categoria: ").strip()

    try:
        valor = float(input("Valor: "))
        while valor <= 0:
            print("Valor deve ser maior que zero.")
            valor = float(input("Valor: "))
    except ValueError:
        print("Valor inválido. Use números.")
        return

    descricao = input("Descrição: ").strip()
    if not descricao:
        descricao = "Sem descrição"

    adicionar_transacao(tipo, categoria, valor, descricao)
    print("Transação adicionada com sucesso!")

def menu_listar_transacoes():
    print("\n[Listar Transações]")
    transacoes = listar_transacoes()

    if not transacoes:
        print("Nenhuma transação encontrada.")
        return

    opcao_filtro = input("Deseja filtrar por data? (s/n): ").strip().lower()
    if opcao_filtro == "s":
        try:
            data_inicio = datetime.strptime(input("Data início (YYYY-MM-DD): "), "%Y-%m-%d")
            data_fim = datetime.strptime(input("Data fim (YYYY-MM-DD): "), "%Y-%m-%d")
            transacoes = filtrar_por_data(transacoes, data_inicio, data_fim)
        except ValueError:
            print("Formato de data inválido.")
            return

    if transacoes:
        for i, t in enumerate(transacoes, start=1):
            print(f"{i}. {t['data']} - {t['tipo'].capitalize()} - {t['categoria']} - R$ {t['valor']:.2f} ({t['descricao']})")
    else:
        print("Nenhuma transação encontrada para o filtro aplicado.")

def menu_exibir_resumo():
    print("\n[Resumo Financeiro]")
    transacoes = listar_transacoes()

    opcao_filtro = input("Deseja filtrar por data? (s/n): ").strip().lower()
    if opcao_filtro == "s":
        try:
            data_inicio = datetime.strptime(input("Data início (YYYY-MM-DD): "), "%Y-%m-%d")
            data_fim = datetime.strptime(input("Data fim (YYYY-MM-DD): "), "%Y-%m-%d")
            transacoes = filtrar_por_data(transacoes, data_inicio, data_fim)
        except ValueError:
            print("Formato de data inválido.")
            return

    total_receitas = sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
    total_despesas = sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
    saldo = total_receitas - total_despesas

    print(f"Total de Receitas: R$ {total_receitas:.2f}")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print(f"Saldo Atual: R$ {saldo:.2f}")

if __name__ == "__main__":
    main()
