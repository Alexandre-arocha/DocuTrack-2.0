from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


STATUS_OPTIONS = ["Ativo", "Em revisão", "Obsoleto"]


class DialogAddEdit(QDialog):
    def __init__(self, parent: Optional[QWidget] = None, data: Optional[dict] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Documento")
        self.data = data or {}
        self._build_ui()
        self._load_initial_data()

    def _build_ui(self) -> None:
        self.nome_input = QLineEdit()
        self.tipo_input = QLineEdit()
        self.setor_input = QLineEdit()
        self.responsavel_input = QLineEdit()
        self.versao_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(STATUS_OPTIONS)

        self.arquivo_input = QLineEdit()
        self.arquivo_input.setPlaceholderText("Caminho para o arquivo (opcional)")
        self.arquivo_browse_button = QPushButton("Escolher arquivo")
        self.arquivo_browse_button.clicked.connect(self._choose_file)

        arquivo_layout = QHBoxLayout()
        arquivo_layout.addWidget(self.arquivo_input)
        arquivo_layout.addWidget(self.arquivo_browse_button)

        form_layout = QFormLayout()
        form_layout.addRow("Nome", self.nome_input)
        form_layout.addRow("Tipo", self.tipo_input)
        form_layout.addRow("Setor", self.setor_input)
        form_layout.addRow("Responsável", self.responsavel_input)
        form_layout.addRow("Versão", self.versao_input)
        form_layout.addRow("Status", self.status_input)
        form_layout.addRow("Arquivo", arquivo_layout)

        self.save_button = QPushButton("Salvar")
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def _load_initial_data(self) -> None:
        if not self.data:
            return
        self.nome_input.setText(self.data.get("nome", ""))
        self.tipo_input.setText(self.data.get("tipo", ""))
        self.setor_input.setText(self.data.get("setor", ""))
        self.responsavel_input.setText(self.data.get("responsavel", ""))
        self.versao_input.setText(self.data.get("versao", ""))
        status = self.data.get("status")
        if status and status in STATUS_OPTIONS:
            self.status_input.setCurrentText(status)
        self.arquivo_input.setText(self.data.get("arquivo", ""))

    def _choose_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Escolher arquivo",
            "",
            "Documentos (*.pdf *.doc *.docx *.txt);;Todos os arquivos (*)",
        )
        if file_path:
            self.arquivo_input.setText(file_path)

    def get_data(self) -> dict:
        arquivo = self.arquivo_input.text().strip()
        return {
            "nome": self.nome_input.text().strip(),
            "tipo": self.tipo_input.text().strip(),
            "setor": self.setor_input.text().strip(),
            "responsavel": self.responsavel_input.text().strip(),
            "versao": self.versao_input.text().strip(),
            "status": self.status_input.currentText(),
            "arquivo": arquivo if arquivo else None,
        }