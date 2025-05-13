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
            self._view.txtOut.controls.append(
                ft.Text(f"Arco da {i[0]} a {i[1]}, peso={i[2]}"))
        self._view.update_page()
        return

    def fillDDProduct(self):
        pass

    def handle_search(self, e):
        pass
