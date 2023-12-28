import graphviz
import yaml

def visualize_turing_machine(config, output_file='diagram'):
    G = graphviz.Digraph(format='png')
    G.attr(rankdir='LR')

    # Set global graph attributes
    G.graph_attr.update({
        'dpi': '100',
        'size': '15,10',
        'bgcolor': 'white',
        'fontcolor': 'black',
    })

    # Add states with enhanced styling
    for state in config['states']:
        pos = config['positions'][state]
        G.node(state, pos=str(pos), shape='circle', style='filled', color='lightgreen', fontcolor='black', fontname='Arial')

    # Add transitions with enhanced styling
    for transition in config['transitions']:
        input_symbols = ", ".join(map(str, transition['input_symbol']))
        label = f"{input_symbols} -> {transition['write_symbol']}, {transition['move']}"
        G.edge(
            transition['current_state'],
            transition['next_state'],
            label=label,
            fontcolor='black',
            color='orange',
            penwidth='2.0',
            fontname='Arial',
        )

    # Save the graph to a PNG file
    G.render(output_file, cleanup=True)

if __name__ == '__main__':
    # Load YAML configuration
    with open('binary_inc.yaml', 'r') as file:
        turing_machine_config = yaml.safe_load(file)

    # Visualize the Turing machine and save the diagram as a PNG file
    visualize_turing_machine(turing_machine_config)
