import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._bestPath = []

    def buildGraph(self, colore, anno):
        self._graph.clear()
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
        res = listaArchiPeso[:3]
        return res

    def contaNodi(self, listaArchi):
        res = []
        for tupla in listaArchi:
            res.append(tupla[0])
            res.append(tupla[1])
        insiemeStampare = set()
        for i in range(0, len(res)):
            for j in range(i+1, len(res)):
                if res[i] == res[j]:
                    insiemeStampare.add(res[i])
        return insiemeStampare

    def getBestSolution(self, source):
        self._bestPath = []
        parziale = [source]
        # successori = self.getSuccessoriAmmissibili(parziale, source)
        self.ricorsione(parziale, list(self._graph.neighbors(source)))
        return self._bestPath

    def ricorsione(self, parziale, successori):
        if len(successori) == 0:
            if len(self._bestPath) < len(parziale):
                self._bestPath = copy.deepcopy(parziale)
                print(self._bestPath)
        else:
            for n in successori:
                parziale.append(n)
                successoriAmmissibili = self.getSuccessoriAmmissibili(parziale, n)
                self.ricorsione(parziale, successoriAmmissibili)
                parziale.pop()

    def getSuccessoriAmmissibili(self, parziale, source):
        ammissibili = []
        pesoUltimo = self._graph[parziale[-2]][parziale[-1]]["weight"]
        for node in list(self._graph.neighbors(source)):
            if self.checkArchi(parziale, node):
                pesoNuovo = self._graph[parziale[-1]][node]["weight"]
                if pesoNuovo >= pesoUltimo:
                    ammissibili.append(node)
        return ammissibili

    def checkArchi(self, parziale, nodo):
        for i in range(0, len(parziale) - 1):
            nodo1 = parziale[i]
            nodo2 = parziale[i + 1]
            if (nodo1, nodo2) == (parziale[-1], nodo) or (nodo2, nodo1) == (parziale[-1], nodo):
                return False
        return True

