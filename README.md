# Árvores Rubro-Negras

Árvores rubro negras são árvores de pesquisa binária
com um bit de informação adicional que é a cor de um
nódulo. A cor pode ser vermelha ou preta. Dependendo
da cor que um nódulo tem ele vai ter propriedades
diferentes.

Suas propriedades são:

- Todo nódulo ou é negro ou é rubro (vermelho);
- A raiz (root) é negra;
- Toda folha é negra:
    - Folhas são somente os nódulos vazios (ponteiros nulos);
- Se um nodulo for rubro, então ambos os filos são negros;
- Para todo nódulo, todos os caminhos até uma folha contém o mesmo número de nódulos negros;