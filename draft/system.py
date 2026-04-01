from models import (
    Usuario, Jogo, Avaliacao,
    ConquistaGeral, ConquistaDeJogo,
    ListaPersonalizada
)
 
 
class SistemaNoctis:
    def __init__(self):
        self.usuarios           = []
        self.jogos_catalogo     = []
        self.trending           = []
        self.proximo_id_usuario = 1
        self.proximo_id_jogo    = 1
 
        self._popular_catalogo_mock()
 
    def _popular_catalogo_mock(self):
        """Simula consulta à API (RAWG/IGDB)."""
        jogos_mock = [
            ("The Witcher 3",  "RPG",          2015, "CD Projekt Red",      "Uma épica caçada a monstros em um mundo aberto."),
            ("God of War",     "Ação/Aventura", 2018, "Santa Monica Studio", "Kratos e seu filho em uma jornada mitológica."),
            ("Cyberpunk 2077", "RPG",           2020, "CD Projekt Red",      "Vida noturna em Night City."),
            ("Hades",          "Roguelike",     2020, "Supergiant Games",    "Escape do submundo grego."),
            ("Elden Ring",     "Ação/RPG",      2022, "FromSoftware",        "Um mundo aberto sombrio."),
        ]
        for nome, genero, ano, dev, sinopse in jogos_mock:
            jogo = Jogo(self.proximo_id_jogo, nome, genero, ano, dev, sinopse)
            self.jogos_catalogo.append(jogo)
            self.proximo_id_jogo += 1
 
        self.trending = self.jogos_catalogo[:3]
 
    # ----------------------------------------------------------
    # Funcionalidade 1 — Login / Cadastro
    # ----------------------------------------------------------
 
    def cadastrar_usuario(self, nome, email, senha):
        if any(u.email == email for u in self.usuarios):
            print("Erro: Email já cadastrado!")
            return None
        usuario = Usuario(self.proximo_id_usuario, nome, email, senha)
        self.usuarios.append(usuario)
        self.proximo_id_usuario += 1
        print(f"Sucesso no Cadastro! Bem-vindo, {nome}.")
        return usuario
 
    def login(self, email, senha):
        for u in self.usuarios:
            if u.email == email and u.senha == senha:
                print(f"Sucesso no Login! Bem-vindo de volta, {u.nome}.")
                return u
        print("Erro de autenticação: Email não cadastrado ou senha incorreta.")
        return None
 
    # ----------------------------------------------------------
    # Funcionalidade 2 — Busca de Jogos
    # ----------------------------------------------------------
 
    def buscar_jogos(self, termo=""):
        if not termo:
            return self.jogos_catalogo
        resultados = [
            j for j in self.jogos_catalogo
            if termo.lower() in j.nome.lower() or termo.lower() in j.genero.lower()
        ]
        print(f"Resultados para '{termo}': {len(resultados)} jogo(s) encontrado(s).")
        return resultados
 
    # ----------------------------------------------------------
    # Funcionalidade 3 — Status dos Jogos
    # Usa Biblioteca (subclasse de ColecaoDeJogos)
    # ----------------------------------------------------------
 
    def marcar_status(self, usuario, jogo, status):
        usuario.biblioteca.adicionar_jogo(jogo, status)
 
    # ----------------------------------------------------------
    # Funcionalidade 4 — Filtragem Avançada
    # ----------------------------------------------------------
 
    def filtrar_jogos(self, genero=None, ano=None, desenvolvedora=None):
        filtrados = self.jogos_catalogo
        if genero:
            filtrados = [j for j in filtrados if j.genero.lower() == genero.lower()]
        if ano:
            filtrados = [j for j in filtrados if j.ano_lancamento == ano]
        if desenvolvedora:
            filtrados = [j for j in filtrados if desenvolvedora.lower() in j.desenvolvedora.lower()]
        return filtrados
 
    # ----------------------------------------------------------
    # Funcionalidade 5 — Avaliação
    # ----------------------------------------------------------
 
    def avaliar_jogo(self, usuario, jogo, nota, comentario=""):
        if not (1 <= nota <= 5):
            print("Nota deve ser entre 1 e 5.")
            return
        avaliacao = Avaliacao(usuario, jogo, nota, comentario)
        jogo.adicionar_avaliacao(avaliacao)
        usuario.avaliacoes.append(avaliacao)
        print(f"Avaliação registrada: {jogo.nome} → {nota}★")
 
    # ----------------------------------------------------------
    # Funcionalidade 6 — Conquistas
    # Usa ConquistaGeral e ConquistaDeJogo (subclasses de Conquista)
    # ----------------------------------------------------------
 
    def criar_conquista_geral(self, nome, descricao):
        """Cria conquista da plataforma, sem jogo vinculado."""
        conquista = ConquistaGeral(nome, descricao)
        print(f"Conquista criada: {conquista}")
        return conquista
 
    def criar_conquista_de_jogo(self, nome, descricao, jogo):
        """Cria conquista obrigatoriamente vinculada a um jogo."""
        conquista = ConquistaDeJogo(nome, descricao, jogo)
        print(f"Conquista criada: {conquista}")
        return conquista
 
    def desbloquear_conquista(self, usuario, conquista):
        if conquista not in usuario.conquistas_desbloqueadas:
            usuario.conquistas_desbloqueadas.append(conquista)
            print(f"🏆 Conquista desbloqueada por {usuario.nome}: {conquista.nome}")
 
    # ----------------------------------------------------------
    # Funcionalidade 7 — Listas Personalizadas
    # Usa ListaPersonalizada (subclasse de ColecaoDeJogos)
    # ----------------------------------------------------------
 
    def criar_lista(self, usuario, nome_lista):
        lista = ListaPersonalizada(nome_lista, usuario)
        usuario.listas_personalizadas.append(lista)
        print(f"Lista '{nome_lista}' criada com sucesso.")
        return lista
 
    # ----------------------------------------------------------
    # Funcionalidade 8 — Perfil
    # ----------------------------------------------------------
 
    def mostrar_perfil(self, usuario):
        print("\n=== PERFIL ===")
        print(usuario)
        print(f"Jogos na biblioteca:      {len(usuario.biblioteca)}")
        print(f"Avaliações feitas:        {len(usuario.avaliacoes)}")
        print(f"Conquistas desbloqueadas: {len(usuario.conquistas_desbloqueadas)}")
        print(f"Listas personalizadas:    {len(usuario.listas_personalizadas)}")
 
        print("\n  [Biblioteca]")
        usuario.biblioteca.listar()
 
        if usuario.listas_personalizadas:
            print("\n  [Listas Personalizadas]")
            for lista in usuario.listas_personalizadas:
                print(f"  → {lista.nome}:")
                lista.listar()
 
        if usuario.conquistas_desbloqueadas:
            print("\n  [Conquistas]")
            for c in usuario.conquistas_desbloqueadas:
                print(f"  {c}")
 
    # ----------------------------------------------------------
    # Funcionalidade 9 — Trending
    # ----------------------------------------------------------
 
    def atualizar_trending(self):
        self.trending = sorted(
            self.jogos_catalogo,
            key=lambda j: len(j.avaliacoes),
            reverse=True
        )[:5]
        print("Trending atualizado!")
 
    def mostrar_trending(self):
        print("\n=== JOGOS TRENDING NO MOMENTO ===")
        for i, jogo in enumerate(self.trending, 1):
            print(f"{i}. {jogo.nome} | Avaliações: {len(jogo.avaliacoes)} | Média: {jogo.media_avaliacoes()}★")
 
    # ----------------------------------------------------------
    # Funcionalidade 10 — Detalhes do Jogo
    # ----------------------------------------------------------
 
    def mostrar_detalhes_jogo(self, jogo):
        print("\n=== DETALHES DO JOGO ===")
        print(jogo)
        print(f"Sinopse:  {jogo.sinopse}")
        print(f"Gênero:   {jogo.genero} | Ano: {jogo.ano_lancamento} | Desenvolvedora: {jogo.desenvolvedora}")
        print(f"Média:    {jogo.media_avaliacoes()}★")
        if jogo.avaliacoes:
            print("Últimas avaliações:")
            for a in jogo.avaliacoes[-3:]:
                print(f"  - {a}")
