from Automata import *
import pydotplus

graph = pydotplus.graph_from_dot_file('teste.dot')
Machine = Automata()

for node in graph.get_nodes():
    node_name = node.get_name()
    if node_name != 'node':
        if node_name == 'S1':
            final = True
        else:
            final = False
                
        state = State(node_name, final=final)

        if node_name == 'S0':
            Machine.set_initial_state(state)
        else:
            Machine.add_state(state)

for edge in graph.get_edges():
    from_state = Machine.states[edge.get_source()]
    to_state = Machine.states[edge.get_destination()]
    label = edge.to_string()
    print(label)
    label = label.split('=')
    label = label[1]
    label = label[:-2]
    label = label.replace('"', '')
    
    Machine.add_transition(from_state, to_state, label)

Machine.print_source()
    
