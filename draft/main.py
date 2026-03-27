from system import SistemaNoctis

def menu():
    print("\n" + "="*60)
    print("NOCTIS - GameTracker")
    print("="*60)
    print("1. Cadastrar usuário")
    print("2. Fazer login")
    print("3. Buscar jogos")
    print("4. Marcar status de um jogo")
    print("5. Filtrar jogos")
    print("6. Avaliar jogo")
    print("7. Criar conquista e desbloquear")
    print("8. Criar lista personalizada")
    print("9. Ver perfil")
    print("10. Ver trending")
    print("11. Ver detalhes de um jogo")
    print("0. Sair")
    print("="*60)

def main():
    sistema = SistemaNoctis()
    usuario_logado = None

    while True:
        menu()
        op = input("Escolha uma opção: ").strip()

        if op == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            sistema.cadastrar_usuario(nome, email, senha)

        elif op == "2":
            email = input("Email: ")
            senha = input("Senha: ")
            usuario_logado = sistema.login(email, senha)

        elif op == "3" and usuario_logado:
            termo = input("Termo de busca (ou Enter para todos): ")
            resultados = sistema.buscar_jogos(termo)
            for j in resultados[:10]:
                print(j)

        elif op == "4" and usuario_logado:
            print("Jogos disponíveis:")
            for j in sistema.jogos_catalogo:
                print(f"{j.id_jogo} - {j.nome}")
            try:
                idx = int(input("ID do jogo: ")) - 1
                jogo = sistema.jogos_catalogo[idx]
                status = input("Status (Jogado/Jogando/Quero Jogar/Abandonado/Platinado/Favorito): ")
                sistema.marcar_status(usuario_logado, jogo, status)
            except (ValueError, IndexError):
                print("ID de jogo inválido.")

        elif op == "5":
            genero = input("Gênero (ou Enter): ") or None
            ano_str = input("Ano (ou Enter): ")
            ano = int(ano_str) if ano_str else None
            dev = input("Desenvolvedora (ou Enter): ") or None
            resultados = sistema.filtrar_jogos(genero, ano, dev)
            for j in resultados:
                print(j)

        elif op == "6" and usuario_logado:
            print("Jogos disponíveis:")
            for j in sistema.jogos_catalogo:
                print(f"{j.id_jogo} - {j.nome}")
            try:
                idx = int(input("ID do jogo: ")) - 1
                jogo = sistema.jogos_catalogo[idx]
                nota = float(input("Nota (1-5): "))
                comentario = input("Comentário (opcional): ")
                sistema.avaliar_jogo(usuario_logado, jogo, nota, comentario)
            except (ValueError, IndexError):
                print("Entrada inválida. Certifique-se de digitar números corretamente.")

        elif op == "7" and usuario_logado:
            nome_c = input("Nome da conquista: ")
            desc = input("Descrição: ")
            conquista = sistema.criar_conquista(nome_c, desc)
            sistema.desbloquear_conquista(usuario_logado, conquista)

        elif op == "8" and usuario_logado:
            nome_lista = input("Nome da lista: ")
            lista = sistema.criar_lista(usuario_logado, nome_lista)
            print("Adicionando primeiro jogo automaticamente para demonstração...")
            lista.adicionar_jogo(sistema.jogos_catalogo[0])

        elif op == "9" and usuario_logado:
            sistema.mostrar_perfil(usuario_logado)

        elif op == "10":
            sistema.atualizar_trending()
            sistema.mostrar_trending()

        elif op == "11":
            print("Jogos disponíveis:")
            for j in sistema.jogos_catalogo:
                print(f"{j.id_jogo} - {j.nome}")
            try:
                idx = int(input("ID do jogo: ")) - 1
                jogo = sistema.jogos_catalogo[idx]
                sistema.mostrar_detalhes_jogo(jogo)
            except (ValueError, IndexError):
                print("ID de jogo inválido.")

        elif op == "0":
            print("Saindo do NOCTIS. Até mais!")
            break

        else:
            print("Opção inválida ou você precisa fazer login primeiro!")

if __name__ == "__main__":
    main()
