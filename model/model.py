import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

    def buildGraph(self, colore, anno):
        nodes = DAO.getAllNodes(colore)
        self._graph.add_nodes_from(nodes)
        self.getAllEdges(anno)
        print(len(self._graph.nodes))
        print(len(self._graph.edges))
        return self._graph

    def getAllEdges(self, anno):
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u != v:
                    peso = DAO.getPesoArco(u, v, anno)[0]
                    if peso != 0:
                        self._graph.add_edge(u, v, weight=peso)

    def getArchiMaggiori(self):
        listaArchiPeso = []
        for u in self._graph.nodes:
            for v in self._graph[u]:
                peso = self._graph[u][v]["weight"]
                listaArchiPeso.append((u, v, peso))
        listaArchiPeso.sort(key=lambda x: x[2], reverse=True)
        return listaArchiPeso[:6]

