import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self.choiceDDProduct = None

    def fillDD(self):
        for i in range(2015, 2019):
            self._view._ddyear.options.append(ft.dropdown.Option(str(i)))

        colori = DAO.getAllColori()
        for c in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(str(c)))

    def handle_graph(self, e):
        if self._view._ddcolor.value is None or self._view._ddyear.value is None:
            self._view.create_alert("Selezionare un colore e un anno!")
            self._view.update_page()
            return
        colore = self._view._ddcolor.value
        anno = self._view._ddyear.value
        grafo = self._model.buildGraph(colore, anno)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {len(grafo.nodes)} Numero di archi: {len(grafo.edges)}"))
        archiMaggiori = self._model.getArchiMaggiori()
        for i in archiMaggiori:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {i[0]} a {i[1]}, peso={i[2]}"))

        nodiApparsi = self._model.contaNodi(archiMaggiori)
        res = []
        for i in nodiApparsi:
            res.append(i.Product_number)
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {res}"))
        self.fillDDProduct()
        self._view._ddnode.disabled = False
        self._view.btn_search.disabled = False
        self._view.update_page()
        return

    def fillDDProduct(self):
        nodes = self._model._graph.nodes
        for n in nodes:
            self._view._ddnode.options.append(ft.dropdown.Option(key=n.Product_number, data=n, on_click=self.readDDProduct))
        self._view.update_page()
        return

    def readDDProduct(self, e):
        self.choiceDDProduct = e.control.data

    def handle_search(self, e):
        if self.choiceDDProduct is None:
            self._view.create_alert("Selezionare un prodotto")
            self._view.update_page()
            return
        path = self._model.getBestSolution(self.choiceDDProduct)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(path) - 1}"))
        self._view.update_page()
        return
