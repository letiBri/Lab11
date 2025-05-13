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
        visitati = []
        for u in self._graph.nodes:
            visitati.append(u)
            for v in self._graph[u]:
                if v not in visitati:
                    peso = self._graph[u][v]["weight"]
                    listaArchiPeso.append((u, v, peso))
        listaArchiPeso.sort(key=lambda x: x[2], reverse=True)
        return listaArchiPeso[:3]


    # manca il fatto di pulire il grafo, altrimenti se richiamo il metodo aggiunge un botto di archi e nodi allo stesso grafo
    def contaNodi(listaArchi):
        res = []
        for tupla in listaArchi:
            res.append(tupla[0])
            res.append(tupla[1])
        return res

    def contaApparizioni(res, nodo):
        tot = 0
        for i in res:
            if i == nodo:
                tot += 1
        return tot





