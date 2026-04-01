odels · PY
Copiar

from datetime import datetime
 
 
# =============================================================
#  USUARIO
# =============================================================
 
class Usuario:
    def __init__(self, id_usuario, nome, email, senha):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.biblioteca = Biblioteca()            # ← agora é um objeto Biblioteca
        self.listas_personalizadas = []
        self.avaliacoes = []
        self.conquistas_desbloqueadas = []
 
    def __str__(self):
        return f"Usuário {self.nome} (ID: {self.id_usuario})"
 
    def alterar_dados(self, novo_nome=None, novo_email=None, nova_senha=None):
        if novo_nome:  self.nome  = novo_nome
        if novo_email: self.email = novo_email
        if nova_senha: self.senha = nova_senha
        print("Dados do perfil atualizados com sucesso!")
 
 
# =============================================================
#  JOGO
# =============================================================
 
class Jogo:
    def __init__(self, id_jogo, nome, genero, ano_lancamento,
                 desenvolvedora, sinopse, capa="sem_capa.jpg"):
        self.id_jogo        = id_jogo
        self.nome           = nome
        self.genero         = genero
        self.ano_lancamento = ano_lancamento
        self.desenvolvedora = desenvolvedora
        self.sinopse        = sinopse
        self.capa           = capa
        self.avaliacoes     = []
 
    def __str__(self):
        return f"{self.nome} ({self.ano_lancamento}) - {self.genero} | {self.desenvolvedora}"
 
    def adicionar_avaliacao(self, avaliacao):
        self.avaliacoes.append(avaliacao)
 
    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0.0
        return round(sum(a.nota for a in self.avaliacoes) / len(self.avaliacoes), 2)
 
 
# =============================================================
#  AVALIACAO
# =============================================================
 
class Avaliacao:
    def __init__(self, usuario, jogo, nota, comentario=""):
        self.usuario    = usuario
        self.jogo       = jogo
        self.nota       = nota
        self.comentario = comentario
        self.data       = datetime.now()
 
    def __str__(self):
        return f"{self.usuario.nome} → {self.jogo.nome}: {self.nota}★ - {self.comentario}"
 
 
# =============================================================
#  HERANÇA 1: CONQUISTA
#
#  MOTIVO: O atributo jogo=None na classe original indica que
#  ela tentava representar dois conceitos distintos ao mesmo
#  tempo — uma conquista genérica da plataforma e uma conquista
#  vinculada a um jogo específico. Em OOP, quando um atributo
#  só existe em alguns objetos de uma classe, o correto é criar
#  uma classe base com o que é comum, e subclasses para cada
#  variação com seus atributos obrigatórios.
# =============================================================
 
class Conquista:
    """Classe base — atributos comuns a qualquer conquista."""
 
    def __init__(self, nome, descricao):
        self.nome     = nome
        self.descricao = descricao
 
    def __str__(self):
        return f"🏆 {self.nome}: {self.descricao}"
 
 
class ConquistaGeral(Conquista):
    """
    Conquista da plataforma, NÃO ligada a nenhum jogo.
    Exemplos: 'Fez 10 avaliações', 'Criou 5 listas'.
    """
 
    def __init__(self, nome, descricao):
        super().__init__(nome, descricao)
 
    def __str__(self):
        return f"🌐 [Geral] {self.nome}: {self.descricao}"
 
 
class ConquistaDeJogo(Conquista):
    """
    Conquista obrigatoriamente ligada a um jogo específico.
    Exemplos: 'Derrotou todos os chefes em Elden Ring'.
    O atributo jogo é OBRIGATÓRIO aqui, não opcional.
    """
 
    def __init__(self, nome, descricao, jogo):
        super().__init__(nome, descricao)
        self.jogo = jogo   # obrigatório — não existe ConquistaDeJogo sem jogo
 
    def __str__(self):
        return f"🎮 [{self.jogo.nome}] {self.nome}: {self.descricao}"
 
 
# =============================================================
#  HERANÇA 2: COLEÇÃO DE JOGOS → BIBLIOTECA e LISTA PERSONALIZADA
#
#  MOTIVO: Biblioteca (self.biblioteca do Usuario) e
#  ListaPersonalizada são ambas coleções de jogos do usuário,
#  com os mesmos comportamentos base de adicionar e remover.
#  Tratá-las como estruturas completamente diferentes (uma como
#  lista de dicts, outra como classe separada) ignora o que
#  têm em comum. A classe base ColecaoDeJogos unifica o
#  comportamento compartilhado, e cada subclasse adiciona
#  apenas o que é específico seu.
# =============================================================
 
class ColecaoDeJogos:
    """Classe base — comportamento comum a qualquer agrupamento de jogos."""
 
    def __init__(self, nome):
        self.nome  = nome
        self.jogos = []
 
    def adicionar_jogo(self, jogo):
        raise NotImplementedError("Subclasses devem implementar adicionar_jogo()")
 
    def remover_jogo(self, jogo):
        raise NotImplementedError("Subclasses devem implementar remover_jogo()")
 
    def listar(self):
        if not self.jogos:
            print(f"  (A coleção '{self.nome}' está vazia)")
            return
        for item in self.jogos:
            print(f"  - {item}")
 
    def __len__(self):
        return len(self.jogos)
 
 
class Biblioteca(ColecaoDeJogos):
    """
    Coleção OFICIAL do sistema para cada usuário.
    Armazena jogo + status (Jogado, Jogando, Quero Jogar, etc.).
    Cada entrada é um dict {"jogo": Jogo, "status": str}.
    """
 
    def __init__(self):
        super().__init__("Biblioteca")
 
    def adicionar_jogo(self, jogo, status="Quero Jogar"):
        # Verifica se o jogo já existe e apenas atualiza o status
        for item in self.jogos:
            if item["jogo"] == jogo:
                item["status"] = status
                print(f"  Status alterado: {jogo.nome} → {status}")
                return
        self.jogos.append({"jogo": jogo, "status": status})
        print(f"  Status definido: {jogo.nome} → {status}")
 
    def remover_jogo(self, jogo):
        self.jogos = [item for item in self.jogos if item["jogo"] != jogo]
        print(f"  '{jogo.nome}' removido da biblioteca.")
 
    def listar(self):
        if not self.jogos:
            print("  (Biblioteca vazia)")
            return
        for item in self.jogos:
            print(f"  [{item['status']}] {item['jogo'].nome}")
 
 
class ListaPersonalizada(ColecaoDeJogos):
    """
    Coleção CRIADA PELO USUÁRIO com nome livre.
    Armazena somente o objeto Jogo, sem status associado.
    Exemplos: 'Melhores de 2024', 'Para jogar com amigos'.
    """
 
    def __init__(self, nome_lista, usuario):
        super().__init__(nome_lista)
        self.usuario   = usuario
        self.nome_lista = nome_lista  # mantido para compatibilidade
 
    def adicionar_jogo(self, jogo):
        if jogo not in self.jogos:
            self.jogos.append(jogo)
            print(f"  '{jogo.nome}' adicionado à lista '{self.nome}'")
        else:
            print(f"  '{jogo.nome}' já está na lista '{self.nome}'")
 
    def remover_jogo(self, jogo):
        if jogo in self.jogos:
            self.jogos.remove(jogo)
            print(f"  '{jogo.nome}' removido da lista '{self.nome}'")
        else:
            print(f"  '{jogo.nome}' não encontrado na lista '{self.nome}'")
 
    def listar(self):
        if not self.jogos:
            print(f"  (Lista '{self.nome}' vazia)")
            return
        for jogo in self.jogos:
            print(f"  - {jogo.nome}")
