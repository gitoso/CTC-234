###########################################################
## CTC-34: Autômata e Linguagens Formais                 ##
## Prof. Forster                                         ##
##                                                       ##
## Equipe:                                               ##
##   Arthur Fernandes de Morais                          ##
##   Gianluigi Dal Toso                                  ##
##   Lucas Alberto Bilobran Lema                         ##
##                                                       ##
###########################################################

# Importa bibliotecas auxiliares
from IPython.display import Image, display
from Automata import *

# Lê a expressão regular do usuário e constrói o autômato referênte à ela
regEx = input('Digite a expressão regular: ')
Machine = Automata()

# Variável auxiliar para contar o número de grafos impressos
graph_counter = 0

# ----- PASSO I: Inicialização do autômato -----

# Inicializa os estados S0 e S1 (sendo S1 um estado final)
S0 = State('S0')
S1 = State('S1', final=True)

# Adiciona os estados à e-NFA
Machine.set_initial_state(S0)
Machine.add_state(S1)

# Adiciona a transição S0 -> S1 à e-NFA utilizando a regEx de entrada
Machine.add_transition(S0, S1, regEx)

# Imprime o resultado do passo I
filename = 'grafos/Q1_grafo_' + str(graph_counter) + '.dot'
#Machine.print_graph(filename, view=False)
#imagename = filename + '.png'
#display(Image(filename=#imagename))

# Incrementa o contador de grafos
graph_counter = graph_counter + 1

# Enquanto o autômato não estiver pronto (somente arcos de um símbolo), contrói o autômato
automata_ready = False
while(not automata_ready):
    # ----- PASSO II: Verifica se alguma transição é união de linguagens -----

    # Vetores para armazenar as novas transições a serem inseridas e as transições existentes a serem deletadas
    new_transitions = []
    to_delete_transitions = []

    # Para cada transição, verifica se ela não é união de linguagens
    for transition in Machine.transitions:

        # Verifica se uma transição é união de linguagens
        parsed_label = Machine.union_parser(transition.label)

        # Se for, seleciona as transições a serem separadas
        if len(parsed_label) > 1:

            # Novas transições a serem adicionadas ao autômato
            for new_label in parsed_label:
                new_transitions.append((transition.from_state, transition.to_state, new_label))

            # Acidiona a transição atual à lista de deletação
            to_delete_transitions.append(transition)

    # Adiciona as novas transições
    for transition in new_transitions:
        Machine.add_transition(transition[0], transition[1], transition[2])

    # Deleta as transições antigas 
    for transition in to_delete_transitions:
        Machine.delete_transition(transition)

    # Imprime o resultado do passo II
    filename = 'grafos/Q1_grafo_' + str(graph_counter) + '.dot'
    #Machine.print_graph(filename, view=False)
    #imagename = filename + '.png'
    #display(Image(filename=#imagename))

    # Incrementa o contador de grafos
    graph_counter = graph_counter + 1

    # ----- PASSO III: Verifica se existem concatenações de linguagens -----

    # Vetores para armazenar as novas transições a serem inseridas e as transições existentes a serem deletadas
    new_transitions = []
    to_delete_transitions = []

    # Para cada transição, verifica se ela não é concatenação de linguagens
    for transition in Machine.transitions:

        # Verifica se uma transição é concatenação de linguagens
        parsed_label = Machine.concatenation_parser(transition.label)

        # Se for, seleciona os novos estados e transições à serem adicionados
        if len(parsed_label) > 1:

            # Pega o número de nós na NFA atualmente (para saber nomear os novos nós)
            node_count = Machine.get_node_count()

            # Para cada linguagem, adiciona um novo estado (nó)
            for i in range(len(parsed_label) - 1):

                # Cria o novo estado
                number = node_count + i
                label = 'S' + str(number)
                new_state = State(label)

                # Adiciona o estado à NFA
                Machine.add_state(new_state)
            
            # Adiciona as novas transições referentes aos novos estados

            # Estado de partida inicial
            from_state = transition.from_state

            # Estado de término inicial
            last_state = transition.to_state

            # Númeração dos próximo estado
            number = node_count
            new_state_name = 'S' + str(number)
            to_state = Machine.states[new_state_name]

            # Adiciona todas as transições referentes aos novos estados
            for new_label in parsed_label:

                # Adiciona uma nova transição
                new_transitions.append((from_state, to_state, new_label))

                # Mapeia a próxima transição
                from_state = to_state
                number = number + 1

                # Se for a última transição vai para o estado final original
                if number >= node_count + len(parsed_label) - 1:
                    label = last_state.label

                # Senão, vai para o próximo estado na lista
                else:
                    label = 'S' + str(number)

                to_state = Machine.states[label]
            
            # Corrige a última transição
            label = last_state.label
            to_state = Machine.states[label]

            # Adiciona a transição original à lista de deletação
            to_delete_transitions.append(transition)

    # Adiciona as novas transições
    for transition in new_transitions:
        Machine.add_transition(transition[0], transition[1], transition[2])

    # Deleta as transições antigas
    for transition in to_delete_transitions:
        Machine.delete_transition(transition)

    # Imprime o resultado do passo III
    filename = 'grafos/Q1_grafo_' + str(graph_counter) + '.dot'
    #Machine.print_graph(filename, view=False)
    #imagename = filename + '.png'
    #display(Image(filename=#imagename))

    # Incrementa o contador de grafos
    graph_counter = graph_counter + 1

    # ----- PASSO IV: Identificar e adaptar os fechos de Kleene -----
    
    # Vetores para armazenar as novas transições a serem inseridas e as transições existentes a serem deletadas
    new_transitions = []
    to_delete_transitions = []

    # Para cada transição, verifica se ela não é fecho de Kleene
    for transition in Machine.transitions:

        # Verifica se uma transição é fecho de Kleene
        if transition.label[-1] == '*':

            # Se for, cria um novo estado intermediário atingido pro transições épsilon

            # Adiciona novo estado
            node_count = Machine.get_node_count()
            number = node_count
            label = 'S' + str(number)
            new_state = State(label)
            Machine.add_state(new_state)

            # Adiciona as novas transições épsilon
            intermediary_state = Machine.states[label]
            new_transitions.append((transition.from_state, intermediary_state, '&'))
            new_transitions.append((intermediary_state, transition.to_state, '&'))

            # Adiciona uma transição do estado para ele mesmo, mas sem o '*'
            new_transitions.append((intermediary_state, intermediary_state, transition.label[:-1]))

            # Adiciona a transição original à lista de deletação
            to_delete_transitions.append(transition)

    # Adiciona as novas transições
    for transition in new_transitions:
        Machine.add_transition(transition[0], transition[1], transition[2])

    # Deleta as transições antigas
    for transition in to_delete_transitions:
        Machine.delete_transition(transition)

    # Imprime o resultado do passo IV
    filename = 'grafos/Q1_grafo_' + str(graph_counter) + '.dot'
    #Machine.print_graph(filename, view=False)
    #imagename = filename + '.png'
    #display(Image(filename=#imagename))

    # Incrementa o contador de grafos
    graph_counter = graph_counter + 1

    # ----- PASSO V: Identificar os parênteses e remover -----
    
    # Se não tiver nenhum parênteses neste estágio o autômato estará pronto, vamos setar uma flag para verificar
    automata_ready = True

    # Vetores para armazenar as novas transições a serem inseridas e as transições existentes a serem deletadas
    new_transitions = []
    to_delete_transitions = []

    # Para cada transição, verifica se começa com parênteses
    for transition in Machine.transitions:
        if transition.label[0] == '(':

            # Se tiver transição com parênteses, a máquina não está pronta, retirar os parênteses e repetir todo o processo
            automata_ready = False

            # Remove os parênteses da transição (cria uma nova sem os parênteses e deleta a atual)
            new_transitions.append((transition.from_state, transition.to_state, transition.label[1:-1]))

            # Adiciona a transição atual à lista de deletação
            to_delete_transitions.append(transition)

    # Adiciona as novas transições
    for transition in new_transitions:
        Machine.add_transition(transition[0], transition[1], transition[2])

    # Deleta as transições antigas
    for transition in to_delete_transitions:
        Machine.delete_transition(transition)

# Imprimir a imagem do grafo
filename='grafos/Q1_grafo_final.dot'
Machine.print_graph(filename, view=False)
#imagename = filename + '.png'
#display(Image(filename=#imagename))

# Imprimir o código do grafo
Machine.print_source()

# Enquanto o usuário desejar, verifica se uma cadeia de caracteres é aceito pelo autômato

while True:
    text = input('Digite uma string: ')
    if Machine.accept_string(text):
        print('Válido!')
    else:
        print('Inválido!')