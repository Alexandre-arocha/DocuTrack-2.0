import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "documentos.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT NOT NULL,
                setor TEXT NOT NULL,
                responsavel TEXT NOT NULL,
                versao TEXT NOT NULL,
                status TEXT NOT NULL,
                criado_em TEXT NOT NULL,
                arquivo TEXT
            )
            """
        )
        conn.commit()


def add_document(
    nome: str,
    tipo: str,
    setor: str,
    responsavel: str,
    versao: str,
    status: str,
    arquivo: Optional[str] = None,
) -> int:
    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO documentos
            (nome, tipo, setor, responsavel, versao, status, criado_em, arquivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, tipo, setor, responsavel, versao, status, criado_em, arquivo),
        )
        conn.commit()
        return cursor.lastrowid


def list_documents(search: str = "") -> List[sqlite3.Row]:
    with get_connection() as conn:
        if search:
            like_value = f"%{search}%"
            cursor = conn.execute(
                """
                SELECT * FROM documentos
                WHERE nome LIKE ? OR tipo LIKE ? OR setor LIKE ? OR responsavel LIKE ?
                ORDER BY criado_em DESC
                """,
                (like_value, like_value, like_value, like_value),
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM documentos ORDER BY criado_em DESC"
            )
        return cursor.fetchall()


def update_document(
    doc_id: int,
    nome: str,
    tipo: str,
    setor: str,
    responsavel: str,
    versao: str,
    status: str,
    arquivo: Optional[str] = None,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE documentos
            SET nome = ?, tipo = ?, setor = ?, responsavel = ?, versao = ?, status = ?, arquivo = ?
            WHERE id = ?
            """,
            (nome, tipo, setor, responsavel, versao, status, arquivo, doc_id),
        )
        conn.commit()


def delete_document(doc_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))
        conn.commit()


def update_status(doc_id: int, status: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE documentos SET status = ? WHERE id = ?",
            (status, doc_id),
        )
        conn.commit()


def update_version(doc_id: int, versao: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE documentos SET versao = ? WHERE id = ?",
            (versao, doc_id),
        )
        conn.commit()
