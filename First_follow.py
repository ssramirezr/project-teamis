def calcular_conjuntos_first(gramatica):
    first = {}

    def first_de(simbolo):
        # If the symbol already has its First set calculated, return it
        if simbolo in first:
            return first[simbolo]
        first[simbolo] = set()  # Initialize the First set for the symbol

        # If the symbol is not in the grammar (it's a terminal)
        if simbolo not in gramatica:
            if not simbolo.isupper():
                first[simbolo].add(simbolo)
            return first[simbolo]

        # If the symbol is a non-terminal, process its productions
        for produccion in gramatica[simbolo]:
            if produccion == 'e':
                first[simbolo].add('e')
                continue
            todos_anulables = True  # Variable to check if all symbols in the production are nullable
            for caracter in produccion:
                if caracter == simbolo:
                    todos_anulables = False
                    break
                conjunto_first = first_de(caracter)  # Calculate the First set of the current symbol
                if conjunto_first:
                    first[simbolo].update(conjunto_first - {'e'})
                if 'e' not in conjunto_first:  # If the symbol is not nullable, break the loop
                    todos_anulables = False
                    break
            if todos_anulables:
                first[simbolo].add('e')  # Add 'e' if all symbols are nullable
        return first[simbolo]

    # Calculate the First sets for each non-terminal in the grammar
    for no_terminal in gramatica:
        first_de(no_terminal)

    return first

def calcular_conjuntos_follow(gramatica, first):
    follow = {no_terminal: set() for no_terminal in gramatica}
    simbolo_inicial = 'S'  # Assume 'S' is the start symbol
    follow[simbolo_inicial].add('$')

    def follow_de(simbolo):
        # Iterate over all non-terminals and their productions
        for nt in gramatica:
            for produccion in gramatica[nt]:
                seguir_temp = set()
                # Iterate over each character in the production
                for i, caracter in enumerate(produccion):
                    if caracter == simbolo:
                        seguir_temp.clear()
                        # Calculate the First set of the symbols following the current symbol
                        for j in range(i + 1, len(produccion)):
                            siguiente_simbolo = produccion[j]
                            if siguiente_simbolo in first:
                                conjunto_first = first[siguiente_simbolo]
                                seguir_temp.update(conjunto_first - {'e'})  # Add elements except 'e'
                                if 'e' not in conjunto_first:
                                    break
                            else:
                                seguir_temp.add(siguiente_simbolo)
                                break
                        else:
                            if nt != simbolo:
                                seguir_temp.update(follow[nt])
                        follow[simbolo].update(seguir_temp)

    cambiado = True
    while cambiado:
        cambiado = False
        viejos_follow = {k: v.copy() for k, v in follow.items()}  # Copy the previous state of Follow
        # Calculate the Follow sets for each non-terminal
        for nt in gramatica:
            follow_de(nt)
        if viejos_follow != follow:
            cambiado = True  # Continue until there are no changes in the Follow sets

    return follow

def leer_entrada():
    c = int(input())  # Read the number of cases
    casos = []
    for _ in range(c):
        m = int(input())  # Read the number of productions for each case
        gramatica = {}
        for _ in range(m):
            linea = input().split()
            no_terminal = linea[0]
            producciones = linea[1:]
            gramatica[no_terminal] = producciones
        casos.append(gramatica)
    return casos

def principal():
    casos = leer_entrada()  # Read all the cases
    for gramatica in casos:
        conjuntos_first = calcular_conjuntos_first(gramatica)  # Calculate the First sets
        conjuntos_follow = calcular_conjuntos_follow(gramatica, conjuntos_first)  # Calculate the Follow sets
        for no_terminal in gramatica:
            if no_terminal in conjuntos_first:
                print(f"First({no_terminal}) = {{{', '.join(conjuntos_first[no_terminal])}}}")
        for no_terminal in gramatica:
            if no_terminal in conjuntos_follow:
                print(f"Follow({no_terminal}) = {{{', '.join(conjuntos_follow[no_terminal])}}}")

if __name__ == "__main__":
    principal()