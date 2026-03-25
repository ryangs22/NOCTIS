from datetime import datetime

class Usuario:
    def __init__(self, id_usuario, nome, email, senha):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha 
        self.biblioteca = []         
        self.listas_personalizadas = []  
        self.avaliacoes = []          
        self.conquistas_desbloqueadas = []  

    def __str__(self):
        return f"Usuário {self.nome} (ID: {self.id_usuario})"

    def alterar_dados(self, novo_nome=None, novo_email=None, nova_senha=None):
        if novo_nome: self.nome = novo_nome
        if novo_email: self.email = novo_email
        if nova_senha: self.senha = nova_senha
        print("Dados do perfil atualizados com sucesso!")


class Jogo:
    def __init__(self, id_jogo, nome, genero, ano_lancamento, desenvolvedora, sinopse, capa="sem_capa.jpg"):
        self.id_jogo = id_jogo
        self.nome = nome
        self.genero = genero
        self.ano_lancamento = ano_lancamento
        self.desenvolvedora = desenvolvedora
        self.sinopse = sinopse
        self.capa = capa
        self.avaliacoes = []  

    def __str__(self):
        return f"{self.nome} ({self.ano_lancamento}) - {self.genero} | {self.desenvolvedora}"

    def adicionar_avaliacao(self, avaliacao):
        self.avaliacoes.append(avaliacao)

    def media_avaliacoes(self):
        if not self.avaliacoes:
            return 0.0
        return round(sum(a.nota for a in self.avaliacoes) / len(self.avaliacoes), 2)


class Avaliacao:
    def __init__(self, usuario, jogo, nota, comentario=""):
        self.usuario = usuario
        self.jogo = jogo
        self.nota = nota 
        self.comentario = comentario
        self.data = datetime.now()

    def __str__(self):
        return f"{self.usuario.nome} → {self.jogo.nome}: {self.nota}★ - {self.comentario}"


class Conquista:
    def __init__(self, nome, descricao, jogo=None):
        self.nome = nome
        self.descricao = descricao
        self.jogo = jogo 

    def __str__(self):
        return f"🏆 {self.nome}: {self.descricao}"


class ListaPersonalizada:
    def __init__(self, nome_lista, usuario):
        self.nome_lista = nome_lista
        self.usuario = usuario
        self.jogos = [] 
    def adicionar_jogo(self, jogo):
        if jogo not in self.jogos:
            self.jogos.append(jogo)
            print(f"Jogo '{jogo.nome}' adicionado à lista '{self.nome_lista}'")

    def remover_jogo(self, jogo):
        if jogo in self.jogos:
            self.jogos.remove(jogo)
            print(f"Jogo '{jogo.nome}' removido da lista '{self.nome_lista}'")
