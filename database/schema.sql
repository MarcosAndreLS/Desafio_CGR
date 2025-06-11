-- Tabela: Equipamentos de Rede
CREATE TABLE IF NOT EXISTS equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    ip_gerenciamento TEXT NOT NULL,
    status TEXT NOT NULL,
    localizacao TEXT NOT NULL
);

-- Tabela: Recursos de Rede
CREATE TABLE IF NOT EXISTS recursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    tipo_recurso TEXT NOT NULL,
    valor_recurso TEXT NOT NULL,
    status_alocacao TEXT NOT NULL,
    cliente_associado TEXT,
    status_atualizado_em TEXT DEFAULT (datetime('now', '-3 hours')),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id) ON DELETE CASCADE
);

-- Tabela: Eventos/Logs
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL DEFAULT (datetime('now', '-3 hours')),
    tipo_evento TEXT NOT NULL,
    descricao TEXT,
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id) ON DELETE CASCADE
);
