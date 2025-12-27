# DocuTrack 📄

Sistema de controle e gestão de documentos com interface gráfica intuitiva.

## 📋 Descrição

DocuTrack é uma aplicação desktop desenvolvida em Python que permite gerenciar, organizar e rastrear documentos de forma eficiente. Com uma interface gráfica amigável, é possível cadastrar, editar, excluir e buscar documentos mantendo histórico de versões e status.

## ✨ Funcionalidades

- ✅ **Cadastro de Documentos**: Adicione novos documentos com informações detalhadas
- ✅ **Busca Avançada**: Procure por nome, tipo, setor ou responsável
- ✅ **Edição**: Modifique documentos existentes facilmente
- ✅ **Controle de Versão**: Rastreie diferentes versões do mesmo documento
- ✅ **Gestão de Status**: Marque documentos como Ativo, Em revisão ou Obsoleto
- ✅ **Anexo de Arquivos**: Associe arquivos PDF, Word ou texto aos documentos
- ✅ **Banco de Dados**: Persistência de dados com SQLite

## 🛠️ Requisitos

- Python 3.8+
- PySide6 (Qt para Python)

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/DocuTrack.git
cd DocuTrack
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

Ou manualmente:
```bash
pip install PySide6
```

## 🚀 Como Usar

Execute a aplicação:
```bash
python app.py
```

A janela principal será aberta com a seguinte interface:

### Barra de Ferramentas
- **Novo**: Criar novo documento
- **Editar**: Modificar documento selecionado
- **Excluir**: Remover documento selecionado
- **Atualizar Status**: Alterar status do documento
- **Atualizar Versão**: Incrementar versão do documento

### Campo de Busca
Digite para filtrar documentos por:
- Nome
- Tipo
- Setor
- Responsável

## 📁 Estrutura do Projeto

```
DocuTrack/
├── app.py                    # Ponto de entrada da aplicação
├── db.py                     # Módulo de banco de dados
├── requirements.txt          # Dependências do projeto
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # Janela principal
│   └── dialog_add_edit.py   # Dialog para adicionar/editar
├── data/
│   └── documentos.db        # Banco de dados (criado automaticamente)
├── assets/                  # Recursos e ícones (opcional)
└── LICENSE
```

## 💾 Banco de Dados

O aplicativo cria automaticamente um banco de dados SQLite em `data/documentos.db` com a tabela de documentos contendo:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Identificador único |
| nome | TEXT | Nome do documento |
| tipo | TEXT | Tipo/categoria |
| setor | TEXT | Setor responsável |
| responsavel | TEXT | Pessoa responsável |
| versao | TEXT | Versão do documento |
| status | TEXT | Status (Ativo/Em revisão/Obsoleto) |
| criado_em | TEXT | Data/hora de criação |
| arquivo | TEXT | Caminho do arquivo associado |

## 🎨 Interface

A aplicação usa PySide6 (Qt6) para criar uma interface moderna e responsiva com:
- Tabela interativa para exibir documentos
- Diálogos para adicionar/editar documentos
- Campo de busca em tempo real
- Seleção por linhas

## 📝 Exemplo de Uso

1. **Adicionar documento**: Clique em "Novo" e preencha os campos
2. **Buscar**: Digite no campo de busca para filtrar resultados
3. **Editar**: Selecione um documento e clique em "Editar"
4. **Mudar status**: Selecione um documento e clique em "Atualizar Status"
5. **Excluir**: Selecione um documento e clique em "Excluir"

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📧 Contato

Para dúvidas ou sugestões, entre em contato através das issues do repositório.

---

**Desenvolvido com ❤️ em Python**
