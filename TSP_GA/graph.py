import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, ArrowStyle

class myGraph():

    def __init__(self,tsp):
        self.tsp = tsp
        self.fig2 = plt.figure(figsize=(10,7))

        #it should be in the center
        self.ax2 = self.fig2.add_subplot(1,1,1)
        self.nodes = []
        self.edge_color = []
        self.create_graph(tsp)



    def create_graph(self,tsp):
        self.tsp_size = tsp.shape[0]

        self.G = nx.Graph()
        G = self.G



        def get_coordinates_in_circle(n):
            thetas = [2 * np.pi * (float(i) / n) for i in range(n)]
            return_list = [(np.cos(theta), np.sin(theta)) for theta in thetas]
            return return_list

        self.positions = get_coordinates_in_circle(self.tsp_size)
        positions = self.positions

        self.fixed_positions = {}
        fixed_positions = self.fixed_positions

        # # Add nodes to the graph
        for i in range(tsp.shape[0]):
            G.add_node(i, color='lightblue')
            fixed_positions[i] = positions[i]

        # Add edges (connections between nodes) to the graph with labels
        for i in range(tsp.shape[0]):
            for j in range(i + 1, tsp.shape[0]):
                G.add_edge(i, j, weight=tsp[i, j], color='black')

        self.node_color = [G.nodes[n]['color'] for n in G.nodes]
        self.edge_color = [G[u][v]['color'] for u, v in G.edges]

    def plot(self, solution=[], cost=-1, show_labels=True):

        # line1, = self.ax1.plot(bestcost[:it],c='k')
        # line1.set_ydata(bestcost[:it])
        # fig1.canvas.draw()
        ax = self.ax2
        ax.clear()

        G = self.G
        fixed_positions = self.fixed_positions
        node_color = self.node_color
        edge_color = self.edge_color
        # ax.annotate(f'Best cost: {str(cost)}',xy=[0.1, 0.2],xytext=[0.9,1])
        ax.set_title(f"Best Solution: {solution}")

        # Draw the network using Matplotlib
        # pos = nx.spring_layout(G)  # Positions for all nodes
        nx.draw(G, fixed_positions, with_labels=True, node_color=node_color, edge_color=edge_color, font_weight='bold',
                ax=ax, width=2)

        if show_labels:
            # Add edge labels
            edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, fixed_positions, font_size=8, edge_labels=edge_labels, font_color='black')

        if len(solution) > 0:
            # Draw node labels for the specific node (in this case, node 3)
            nx.draw_networkx_labels(G, {
                solution[0]: (fixed_positions[solution[0]][0], fixed_positions[solution[0]][1] + 0.2)},
                                    labels={solution[0]: 'Start', }, font_size=12, font_color='blue', ax=ax)

            arrow_props = dict(facecolor='red', edgecolor='red', arrowstyle='->', lw=2, )
            # arrow_props2 = dict(facecolor='red', edgecolor='red', arrowstyle='-', lw=3, )

            style = ArrowStyle('Fancy', head_length=15, head_width=15, tail_width=0.1)

            for i in range(len(solution) - 1):
                new_pos_x1 = fixed_positions[solution[i + 1]][0]
                new_pos_x2 = fixed_positions[solution[i]][0]
                new_pos_x = (new_pos_x2 + new_pos_x1) / 2
                # new_pos_x = (new_pos_x2+new_pos_x)/2

                new_pos_y1 = fixed_positions[solution[i + 1]][1]
                new_pos_y2 = fixed_positions[solution[i]][1]
                new_pos_y = (new_pos_y2 + new_pos_y1) / 2
                # new_pos_y = (new_pos_y2+new_pos_y)/2

                ax.annotate('', xy=[new_pos_x, new_pos_y], xytext=fixed_positions[solution[i]],
                            arrowprops=arrow_props, )
                arrow = FancyArrowPatch(fixed_positions[solution[i]], [new_pos_x, new_pos_y], mutation_scale=1,
                                        arrowstyle=style, color='r')
                ax.add_patch(arrow)

            new_pos_x1 = fixed_positions[solution[0]][0]
            new_pos_x2 = fixed_positions[solution[i + 1]][0]
            new_pos_x = (new_pos_x2 + new_pos_x1) / 2
            # new_pos_x = (new_pos_x2+new_pos_x)/2

            new_pos_y1 = fixed_positions[solution[0]][1]
            new_pos_y2 = fixed_positions[solution[i + 1]][1]
            new_pos_y = (new_pos_y2 + new_pos_y1) / 2
            # new_pos_y = (new_pos_y2+new_pos_y)/2

            ax.annotate('', xy=[new_pos_x, new_pos_y], xytext=fixed_positions[solution[i + 1]],
                        arrowprops=arrow_props, )
            arrow = FancyArrowPatch(fixed_positions[solution[i + 1]], [new_pos_x, new_pos_y], mutation_scale=1,
                                    arrowstyle=style, color='r')
            ax.add_patch(arrow)
            # ax.annotate('', xy=[new_pos_x, new_pos_y], xytext=fixed_positions[solution[i+1]], arrowprops=arrow_props,)
            # arrow_props = dict(facecolor='red', edgecolor='red', arrowstyle='->', lw=3, )
            # ax.annotate('', xy=fixed_positions[1], xytext=fixed_positions[0], arrowprops=arrow_props,)

        self.fig2.canvas.draw()

    def rest_colors(self):

        G = self.G
        # for n in G.nodes:
        #     G.nodes[n]['color']='lightblue'

        for u, v in G.edges:
            G[u][v]['color'] = [x / 255 for x in [200, 200, 200]]

        # global node_color
        # global edge_color
        self.node_color = [G.nodes[n]['color'] for n in G.nodes]
        self.edge_color = [G[u][v]['color'] for u, v in G.edges]

        # [G.nodes[n]['color']='lightblue' for n in G.nodes]
        # [G[u][v]['color']='black' for u, v in G.edges]

    def plot_solution(self, solution, cost):
        # plt.figure('x')
        # plt.cla()
        # solution = np.array([0,1,2,3,4])
        G = self.G
        nodes = G.nodes
        edges = G.edges
        # solution
        self.rest_colors()
        # global node_color
        # global edge_color
        # global G
        # global fixed_positions

        for i in range(len(solution) - 1):
            G[solution[i]][solution[i + 1]]['color'] = 'red'
        G[solution[i + 1]][solution[0]]['color'] = 'red'
        # arrow_props = dict(facecolor='red', edgecolor='red', arrowstyle='<->', lw=3, )
        # ax.annotate('', xy=fixed_positions[solution[i+1]], xytext=fixed_positions[solution[i]], arrowprops=arrow_props,)

        self.node_color = [G.nodes[n]['color'] for n in nodes]
        self.edge_color = [G[u][v]['color'] for u, v in edges]
        self.plot(solution=solution, cost=cost, show_labels=False)


