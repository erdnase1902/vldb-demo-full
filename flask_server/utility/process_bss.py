from enum import Enum
import json
from random import random


def process_bss(bss_path, output_path=None):
    STATE = Enum('STATE', 'GRAPH_ID NUM_NODE_EDGE NODES EDGES')
    with open(bss_path, mode='r') as bss:
        bss_lines = bss.readlines()
        bss_lines = [l.strip() for l in bss_lines]
        num_lines = len(bss_lines)
        graph = None
        graphid = None
        graphs = dict()
        num_nodes = 0
        num_edges = 0
        line_idx = 0
        state = STATE.GRAPH_ID
        while line_idx < num_lines:
            if state == STATE.GRAPH_ID:
                graph = {'nodes': [], 'edges': []}
                graphid = bss_lines[line_idx]
                line_idx += 1
                state = STATE.NUM_NODE_EDGE
            elif state == STATE.NUM_NODE_EDGE:
                num_nodes = int(bss_lines[line_idx].split(" ")[0])
                num_edges = int(bss_lines[line_idx].split(" ")[1])
                line_idx += 1
                state = STATE.NODES
            elif state == STATE.NODES:
                nodeid = 0
                for line in bss_lines[line_idx: line_idx + num_nodes]:
                    node = {'id': "n{}".format(nodeid), 'label': line, 'x': random(), 'y': random()}
                    graph['nodes'].append(node)
                    nodeid += 1
                line_idx += num_nodes
                state = STATE.EDGES
            elif state == STATE.EDGES:
                edgeid = 0
                for line in bss_lines[line_idx: line_idx + num_edges]:
                    edge_source = 'n' + line.split(" ")[0]
                    edge_target = 'n' + line.split(" ")[1]
                    edge = {'id': "e{}".format(edgeid), 'source': edge_source, 'target': edge_target}
                    graph['edges'].append(edge)
                    edgeid += 1
                graphs[graphid] = graph
                line_idx += num_edges
                state = STATE.GRAPH_ID

        if output_path:
            with open(output_path, mode='w') as output:
                json.dump(graphs, output)


if __name__ == '__main__':
    bss_path = '/project/Graph-Hashing/data/FULL_ALCHEMY/train/graphs.bss'
    process_bss(bss_path)
