from system import SistemaNoctis
 
def menu():
    print("\n" + "=" * 60)
    print("           NOCTIS - GameTracker")
    print("=" * 60)
    print("1.  Cadastrar usuário")
    print("2.  Fazer login")
    print("3.  Buscar jogos")
    print("4.  Marcar status de um jogo")
    print("5.  Filtrar jogos")
    print("6.  Avaliar jogo")
    print("7a. Criar conquista GERAL e desbloquear")
    print("7b. Criar conquista DE JOGO e desbloquear")
    print("8.  Criar lista personalizada")
    print("9.  Ver perfil")
    print("10. Ver trending")
    print("11. Ver detalhes de um jogo")
    print("0.  Sair")
    print("=" * 60)
 
 
def listar_jogos(sistema):
    for j in sistema.jogos_catalogo:
        print(f"  {j.id_jogo} - {j.nome}")
 
def selecionar_jogo(sistema):
    listar_jogos(sistema)
    try:
        idx = int(input("ID do jogo: ")) - 1
        return sistema.jogos_catalogo[idx]
    except (ValueError, IndexError):
        print("ID de jogo inválido.")
        return None
 
 
def main():
    sistema        = SistemaNoctis()
    usuario_logado = None
 
    while True:
        menu()
        op = input("Escolha uma opção: ").strip()
 
        # ── 1. Cadastro ───────────────────────────────────────
        if op == "1":
            nome  = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            sistema.cadastrar_usuario(nome, email, senha)
 
        # ── 2. Login ──────────────────────────────────────────
        elif op == "2":
            email          = input("Email: ")
            senha          = input("Senha: ")
            usuario_logado = sistema.login(email, senha)
 
        # ── 3. Buscar Jogos ───────────────────────────────────
        elif op == "3" and usuario_logado:
            termo = input("Termo de busca (ou Enter para todos): ")
            for j in sistema.buscar_jogos(termo)[:10]:
                print(f"  {j}")
 
        # ── 4. Marcar Status (usa Biblioteca) ─────────────────
        elif op == "4" and usuario_logado:
            print("Jogos disponíveis:")
            jogo = selecionar_jogo(sistema)
            if jogo:
                status = input("Status (Jogado/Jogando/Quero Jogar/Abandonado/Platinado/Favorito): ")
                sistema.marcar_status(usuario_logado, jogo, status)
 
        # ── 5. Filtrar Jogos ──────────────────────────────────
        elif op == "5":
            genero  = input("Gênero (ou Enter): ") or None
            ano_str = input("Ano (ou Enter): ")
            ano     = int(ano_str) if ano_str else None
            dev     = input("Desenvolvedora (ou Enter): ") or None
            resultado = sistema.filtrar_jogos(genero, ano, dev)
            if resultado:
                for j in resultado:
                    print(f"  {j}")
            else:
                print("Nenhum jogo encontrado com esses filtros.")
 
        # ── 6. Avaliar Jogo ───────────────────────────────────
        elif op == "6" and usuario_logado:
            print("Jogos disponíveis:")
            jogo = selecionar_jogo(sistema)
            if jogo:
                try:
                    nota      = float(input("Nota (1-5): "))
                    comentario = input("Comentário (opcional): ")
                    sistema.avaliar_jogo(usuario_logado, jogo, nota, comentario)
                except ValueError:
                    print("Nota inválida.")
 
        # ── 7a. Conquista GERAL (sem jogo) ────────────────────
        elif op == "7a" and usuario_logado:
            nome_c = input("Nome da conquista: ")
            desc   = input("Descrição: ")
            # ConquistaGeral — não precisa de jogo
            conquista = sistema.criar_conquista_geral(nome_c, desc)
            sistema.desbloquear_conquista(usuario_logado, conquista)
 
        # ── 7b. Conquista DE JOGO (com jogo obrigatório) ──────
        elif op == "7b" and usuario_logado:
            nome_c = input("Nome da conquista: ")
            desc   = input("Descrição: ")
            print("Selecione o jogo vinculado:")
            jogo = selecionar_jogo(sistema)
            if jogo:
                # ConquistaDeJogo — jogo é obrigatório
                conquista = sistema.criar_conquista_de_jogo(nome_c, desc, jogo)
                sistema.desbloquear_conquista(usuario_logado, conquista)
 
        # ── 8. Lista Personalizada (usa ListaPersonalizada) ───
        elif op == "8" and usuario_logado:
            nome_lista = input("Nome da lista: ")
            lista      = sistema.criar_lista(usuario_logado, nome_lista)
            print("Selecione um jogo para adicionar à lista:")
            jogo = selecionar_jogo(sistema)
            if jogo:
                lista.adicionar_jogo(jogo)
 
        # ── 9. Ver Perfil ─────────────────────────────────────
        elif op == "9" and usuario_logado:
            sistema.mostrar_perfil(usuario_logado)
 
        # ── 10. Trending ──────────────────────────────────────
        elif op == "10":
            sistema.atualizar_trending()
            sistema.mostrar_trending()
 
        # ── 11. Detalhes do Jogo ──────────────────────────────
        elif op == "11":
            print("Jogos disponíveis:")
            jogo = selecionar_jogo(sistema)
            if jogo:
                sistema.mostrar_detalhes_jogo(jogo)
 
        # ── 0. Sair ───────────────────────────────────────────
        elif op == "0":
            print("Saindo do NOCTIS. Até mais!")
            break
 
        else:
            print("Opção inválida ou você precisa fazer login primeiro!")
 
 
if __name__ == "__main__":
    main()
