"""
    Implementação de uma Arvore Rubro-Negra
"""

import sys
from collections import deque


class No():
    """
        Classe Nó que comporá arvore
    """

    def __init__(self, valor):
        self.valor = valor
        self.pai = None
        self.esquerda = None
        self.direita = None
        self.cor = 1


class ArvoreRubroNegra():
    """
        Classe da Arvore Rubro-Negra que utiliza da classe Nó para compor seus vértices.
    """

    def __init__(self):
        self.nulo = No(0)
        self.nulo.cor = 0
        self.nulo.esquerda = None
        self.nulo.direita = None
        self.raiz = self.nulo

    def ajustar_regras_deletar(self, x):
        """
            Este método ajusta a árvore de forma que as regras sejam atendidas
            após um nó ser deletado, mudando as cores dos nós e utilizando dos
            métodos que fazem rotações.
        """

        while x != self.raiz and x.cor == 0:
            if x == x.pai.esquerda:
                s = x.pai.direita
                if s.cor == 1:
                    s.cor = 0
                    x.pai.cor = 1
                    self.rotacionar_esquerda(x.pai)
                    s = x.pai.direita

                if s.esquerda.cor == 0 and s.direita.cor == 0:
                    s.cor = 1
                    x = x.pai
                else:
                    if s.direita.cor == 0:
                        s.esquerda.cor = 0
                        s.cor = 1
                        self.rotacionar_direita(s)
                        s = x.pai.direita

                    s.cor = x.pai.cor
                    x.pai.cor = 0
                    s.direita.cor = 0
                    self.rotacionar_esquerda(x.pai)
                    x = self.raiz
            else:
                s = x.pai.esquerda
                if s.cor == 1:
                    s.cor = 0
                    x.pai.cor = 1
                    self.rotacionar_direita(x.pai)
                    s = x.pai.esquerda

                if s.direita.cor == 0 and s.direita.cor == 0:
                    s.cor = 1
                    x = x.pai
                else:
                    if s.esquerda.cor == 0:
                        s.direita.cor = 0
                        s.cor = 1
                        self.rotacionar_esquerda(s)
                        s = x.pai.esquerda

                    s.cor = x.pai.cor
                    x.pai.cor = 0
                    s.esquerda.cor = 0
                    self.rotacionar_direita(x.pai)
                    x = self.raiz
        x.cor = 0

    def troca(self, u, v):
        """
            Este método troca os dois nós 'u' e 'v' de lugar
        """

        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def deletar_no_auxiliar(self, no, chave):
        """
            Método chamado pelo deletar_no(). É ele quem realmente possui a lógica
            para deletar o nó da árvore.
        """

        z = self.nulo
        while no != self.nulo:
            if no.valor == chave:
                z = no

            if no.valor <= chave:
                no = no.direita
            else:
                no = no.esquerda

        if z == self.nulo:
            print("Cannot find chave in the no")
            return

        y = z
        y_original_cor = y.cor
        if z.esquerda == self.nulo:
            x = z.direita
            self.troca(z, z.direita)
        elif z.direita == self.nulo:
            x = z.esquerda
            self.troca(z, z.esquerda)
        else:
            y = self.minimo(z.direita)
            y_original_cor = y.cor
            x = y.direita
            if y.pai == z:
                x.pai = y
            else:
                self.troca(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y

            self.troca(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor
        if y_original_cor == 0:
            self.ajustar_regras_deletar(x)

    def ajustar_regras_inserir(self, k):
        """
            Este método ajusta a árvore de forma que as regras sejam atendidas
            após um nó ser inserido, mudando as cores dos nós e utilizando dos
            métodos que fazem rotações.
        """

        while k.pai.cor == 1:
            if k.pai == k.pai.pai.direita:
                u = k.pai.pai.esquerda
                if u.cor == 1:
                    u.cor = 0
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    k = k.pai.pai
                else:
                    if k == k.pai.esquerda:
                        k = k.pai
                        self.rotacionar_direita(k)
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    self.rotacionar_esquerda(k.pai.pai)
            else:
                u = k.pai.pai.direita

                if u.cor == 1:
                    u.cor = 0
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    k = k.pai.pai
                else:
                    if k == k.pai.direita:
                        k = k.pai
                        self.rotacionar_esquerda(k)
                    k.pai.cor = 0
                    k.pai.pai.cor = 1
                    self.rotacionar_direita(k.pai.pai)
            if k == self.raiz:
                break
        self.raiz.cor = 0

    def mostrar_arvore_auxiliar(self, no, indentacao, ultimo):
        """
            Esta método é chamada pelo método mostrar_arvore() como um método auxiliar
            É ele quem realmente possui a lógica utilizada para mostrar a árvore.
        """

        if no != self.nulo:
            sys.stdout.write(indentacao)
            if ultimo:
                sys.stdout.write("R----")
                indentacao += "     "
            else:
                sys.stdout.write("L----")
                indentacao += "|    "

            s_cor = "RED" if no.cor == 1 else "BLACK"
            print(str(no.valor) + "(" + s_cor + ")")
            self.mostrar_arvore_auxiliar(no.esquerda, indentacao, False)
            self.mostrar_arvore_auxiliar(no.direita, indentacao, True)

    def minimo(self, no):
        """
            Retorna o menor valor na sub arvore, ou seja, o mais a esquerda
        """

        while no.esquerda != self.nulo:
            no = no.esquerda
        return no

    def maximo(self, no):
        """
            Retorna o maior valor na sub arvore, ou seja, o mais a direita.
        """

        while no.direita != self.nulo:
            no = no.direita
        return no

    def rotacionar_esquerda(self, x):
        """
            Este método realiza o processo de rotação para a esquerda.
        """

        y = x.direita
        x.direita = y.esquerda
        if y.esquerda != self.nulo:
            y.esquerda.pai = x

        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def rotacionar_direita(self, x):
        """
            Este método realiza o processo de rotação para a direita.
        """

        y = x.esquerda
        x.esquerda = y.direita
        if y.direita != self.nulo:
            y.direita.pai = x

        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.direita:
            x.pai.direita = y
        else:
            x.pai.esquerda = y
        y.direita = x
        x.pai = y

    def inserir(self, chave):
        """
            Este método insere um elemento na arvore. Ao seu final, chama o método
            ajustar_regras_inserir() para que as regras da árvore rubro-negra sejam
            mantidas.
        """

        no = No(chave)
        no.pai = None
        no.valor = chave
        no.esquerda = self.nulo
        no.direita = self.nulo
        no.cor = 1

        y = None
        x = self.raiz

        while x != self.nulo:
            y = x
            if no.valor < x.valor:
                x = x.esquerda
            else:
                x = x.direita

        no.pai = y
        if y is None:
            self.raiz = no
        elif no.valor < y.valor:
            y.esquerda = no
        else:
            y.direita = no

        if no.pai is None:
            no.cor = 0
            return

        if no.pai.pai is None:
            return

        self.ajustar_regras_inserir(no)

    def deletar_no(self, valor):
        """
            Este método deleta um no da arvore com ajuda do método deletar_no_auxiliar()
            que ao seu final, chama o método ajustar_regras_deletar() para que as regras da
            árvore rubro-negra sejam mantidas.
        """

        self.deletar_no_auxiliar(self.raiz, valor)

    def mostrar_arvore(self):
        """
            Esta método mostra todos os nós da árvore
        """

        self.mostrar_arvore_auxiliar(self.raiz, "", True)

    def mostrar_largura(self):
        """
            Questão 1)
            Esta método mostra a largura da árvore
        """

        if self.raiz is None:
            return
        fila = deque([self.raiz])
        largura = 1

        while fila:
            largura_nivel = len(fila)
            largura = max(largura, largura_nivel)
            for _ in range(largura_nivel):
                no = fila.popleft()
                # print(no.valor)
                if no.esquerda:
                    fila.append(no.esquerda)
                if no.direita:
                    fila.append(no.direita)

        print(largura)

    def altura_auxiliar(self, no):
        """
            Questão 2)
            Este médoto possui a lógica utilizada para encontrar a altura da arvore.
        """

        # se o nó for None, retorna altura 0
        if not no:
            return 0

        # calcula a altura da subárvore à esquerda
        altura_esquerda = self.altura_auxiliar(no.esquerda)

        # calcula a altura da subárvore à direita
        altura_direita = self.altura_auxiliar(no.direita)

        # retorna a maior altura + 1 (altura do nó atual)
        return max(altura_esquerda, altura_direita) + 1

    def altura(self):
        """
            Questão 2)
            Este método mostra a altura da árvore, chamando o metodo altura_auxiliar().
        """

        print(self.altura_auxiliar(self.raiz))

    def esta_cheio_auxiliar(self, no):
        """
            Questão 3)
            Este método possui a lógica para verificar se a árvore esa cheia.
        """

        if no.esquerda.valor and no.direita.valor:
            return self.esta_cheio_auxiliar(no.esquerda) and self.esta_cheio_auxiliar(no.direita)
        if not no.esquerda.valor and not no.direita.valor:
            return True
        return False

    def esta_cheio_primeiro_caso(self, no):
        """
            Questão 3)
            Este método cobre a verificação da raiz.
        """

        if no.esquerda.valor and no.direita.valor:
            return True
        return False

    def esta_cheio(self):
        """
            Questão 3)
            Este método verifica se a árvore esa cheia.
        """

        if self.esta_cheio_primeiro_caso(self.raiz):
            return self.esta_cheio_auxiliar(self.raiz)
        return False

    def arvore_espelho_auxiliar(self, no):
        """
            Questão 4)
            Este método possui a lógica para espelhar a arvore.
        """

        # caso base: se o nó é uma folha, então não precisamos fazer nada
        if no is None:
            return

        # trocamos os filhos do nó atual
        no.esquerda, no.direita = no.direita, no.esquerda

        # chamamos a função recursivamente para os filhos do nó atual
        self.arvore_espelho_auxiliar(no.esquerda)
        self.arvore_espelho_auxiliar(no.direita)

    def arvore_espelho(self):
        """
            Questão 4)
            Este método espelha a arvore, chamando o método arvore_espelho_auxiliar().
        """

        self.arvore_espelho_auxiliar(self.raiz)


    def pos_ordem_auxiliar(self, no):
        """
            Questão 5-a)
            Este método possui a lógica que percore a árvore em pos-ordem.
        """

        if no != self.nulo:
            self.pos_ordem_auxiliar(no.esquerda)
            self.pos_ordem_auxiliar(no.direita)
            sys.stdout.write(str(no.valor) + " ")

    def pos_ordem(self):
        """
            Questão 5-a)
            Este método percore a árvore em pos-ordem.
        """

        self.pos_ordem_auxiliar(self.raiz)


    def pre_ordem_auxiliar(self, no):
        """
            Questão 5-b)
            Este método possui a lógica que percore a árvore em pré-ordem
        """

        if no != self.nulo:
            sys.stdout.write(str(no.valor) + " ")
            self.pre_ordem_auxiliar(no.esquerda)
            self.pre_ordem_auxiliar(no.direita)

    def pre_ordem(self):
        """
            Questão 5-b)
            Este método percore a árvore em ordem simétrica.
        """
        self.pre_ordem_auxiliar(self.raiz)


    def em_ordem_auxiliar(self, no):
        """
            Questão 5-c)
            Este método possui a lógica que percore a árvore em em ordem simétrica
        """

        if no != self.nulo:
            self.em_ordem_auxiliar(no.esquerda)
            sys.stdout.write(str(no.valor) + " ")
            self.em_ordem_auxiliar(no.direita)

    def em_ordem(self):
        """
            Questão 5-c)
            Este método percore a árvore em pre-ordem.
        """
        self.em_ordem_auxiliar(self.raiz)


if __name__ == "__main__":
    arn = ArvoreRubroNegra()

    arn.inserir(1)

    arn.inserir(2)

    arn.inserir(3)

    arn.inserir(4)

    arn.inserir(5)

    arn.inserir(6)

    arn.inserir(7)
    arn.inserir(8)
    arn.inserir(9)
    arn.inserir(10)


    # arn.deletar_no(1)
    # arn.deletar_no(2)
    # arn.deletar_no(3)
    arn.mostrar_arvore()
    # arn.mostrar_arvore()
    # arn.mostrar_largura()

    print(arn.esta_completo())

    # arn.arvore_espelho()
    # arn.mostrar_arvore()

    # arn.mostrar_largura()

    # arn.altura()

    arn.em_ordem()
