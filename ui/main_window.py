from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import db
from ui.dialog_add_edit import DialogAddEdit, STATUS_OPTIONS


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Controle de Documentos")
        self.resize(1000, 600)
        self._build_ui()
        self.load_data()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome, tipo, setor ou responsável")
        self.search_input.textChanged.connect(self.load_data)

        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Nome",
                "Tipo",
                "Setor",
                "Responsável",
                "Versão",
                "Status",
                "Criado em",
                "Arquivo",
            ]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)

        self.new_button = QPushButton("Novo")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Excluir")
        self.status_button = QPushButton("Atualizar Status")
        self.version_button = QPushButton("Atualizar Versão")

        self.new_button.clicked.connect(self.add_document)
        self.edit_button.clicked.connect(self.edit_document)
        self.delete_button.clicked.connect(self.delete_document)
        self.status_button.clicked.connect(self.update_status)
        self.version_button.clicked.connect(self.update_version)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.new_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.status_button)
        buttons_layout.addWidget(self.version_button)
        buttons_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)

        central_widget.setLayout(layout)

    def load_data(self) -> None:
        search_text = self.search_input.text().strip()
        documents = db.list_documents(search_text)
        self.table.setRowCount(0)
        for row in documents:
            current_row = self.table.rowCount()
            self.table.insertRow(current_row)
            values = [
                row["id"],
                row["nome"],
                row["tipo"],
                row["setor"],
                row["responsavel"],
                row["versao"],
                row["status"],
                row["criado_em"],
                row["arquivo"],
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table.setItem(current_row, col, item)
        self.table.resizeRowsToContents()

    def _get_selected_document_id(self) -> Optional[int]:
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Seleção necessária", "Selecione um documento na tabela.")
            return None
        row = selected_items[0].row()
        id_item = self.table.item(row, 0)
        return int(id_item.text()) if id_item else None

    def add_document(self) -> None:
        dialog = DialogAddEdit(self)
        if dialog.exec() == DialogAddEdit.Accepted:
            data = dialog.get_data()
            if not all([data["nome"], data["tipo"], data["setor"], data["responsavel"], data["versao"]]):
                QMessageBox.warning(self, "Dados incompletos", "Preencha todos os campos obrigatórios.")
                return
            db.add_document(**data)
            self.load_data()

    def edit_document(self) -> None:
        doc_id = self._get_selected_document_id()
        if doc_id is None:
            return
        row = self._get_row_data(doc_id)
        dialog = DialogAddEdit(self, row)
        if dialog.exec() == DialogAddEdit.Accepted:
            data = dialog.get_data()
            if not all([data["nome"], data["tipo"], data["setor"], data["responsavel"], data["versao"]]):
                QMessageBox.warning(self, "Dados incompletos", "Preencha todos os campos obrigatórios.")
                return
            db.update_document(doc_id, **data)
            self.load_data()

    def _get_row_data(self, doc_id: int) -> dict:
        for row_index in range(self.table.rowCount()):
            if int(self.table.item(row_index, 0).text()) == doc_id:
                arquivo = self.table.item(row_index, 8).text()
                return {
                    "id": doc_id,
                    "nome": self.table.item(row_index, 1).text(),
                    "tipo": self.table.item(row_index, 2).text(),
                    "setor": self.table.item(row_index, 3).text(),
                    "responsavel": self.table.item(row_index, 4).text(),
                    "versao": self.table.item(row_index, 5).text(),
                    "status": self.table.item(row_index, 6).text(),
                    "criado_em": self.table.item(row_index, 7).text(),
                    "arquivo": arquivo if arquivo else None,
                }
        return {}

    def delete_document(self) -> None:
        doc_id = self._get_selected_document_id()
        if doc_id is None:
            return
        reply = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este documento?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            db.delete_document(doc_id)
            self.load_data()

    def update_status(self) -> None:
        doc_id = self._get_selected_document_id()
        if doc_id is None:
            return
        status, ok = QInputDialog.getItem(
            self, "Atualizar status", "Selecione o novo status:", STATUS_OPTIONS, 0, False
        )
        if ok and status:
            db.update_status(doc_id, status)
            self.load_data()

    def update_version(self) -> None:
        doc_id = self._get_selected_document_id()
        if doc_id is None:
            return
        current_version = self._get_row_data(doc_id).get("versao", "")
        version, ok = QInputDialog.getText(
            self, "Atualizar versão", "Nova versão:", text=current_version
        )
        if ok and version.strip():
            db.update_version(doc_id, version.strip())
            self.load_data()