-- Arquivo que irá conter os dados para inserção

-- Insere Equipamentos
INSERT INTO equipamentos (nome, tipo, ip_gerenciamento, status, localizacao) VALUES
('Switch A', 'Switch', '192.168.0.1', 'Online', 'Loc X'),
('Router B', 'Router', '192.168.0.2', 'Offline', 'Loc Y'),
('Server C', 'Server', '192.168.0.3', 'Manutenção', 'Loc Z');

-- Insere Recursos para o Switch A (id=1)
INSERT INTO recursos (equipamento_id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado) VALUES
(1, 'Porta Ethernet', 'Eth0/1', 'Alocado', 'Cliente X'),
(1, 'Porta Ethernet', 'Eth0/2', 'Disponível', NULL),
(1, 'IP v4', '192.168.1.10', 'Alocado', 'Cliente Y'),
(1, 'IP v4', '192.168.1.11', 'Reservado', NULL),
(1, 'IP v6', '2001:db8::1', 'Disponível', NULL);

-- Insere recursos para o Router B (id=2)
INSERT INTO recursos (equipamento_id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado) VALUES
(2, 'Porta Ethernet', 'Eth1/1', 'Disponível', NULL),
(2, 'Porta Ethernet', 'Eth1/2', 'Alocado', 'Cliente Z'),
(2, 'IP v4', '10.0.0.1', 'Alocado', 'Cliente W'),
(2, 'IP v4', '10.0.0.2', 'Reservado', NULL),
(2, 'IP v6', '2001:db8::2', 'Disponível', NULL);

-- Insere recursos para o Server C (id=3)
INSERT INTO recursos (equipamento_id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado) VALUES
(3, 'Porta Ethernet', 'Eth2/1', 'Alocado', 'Cliente A'),
(3, 'Porta Ethernet', 'Eth2/2', 'Disponível', NULL),
(3, 'IP v4', '172.16.0.1', 'Reservado', NULL),
(3, 'IP v4', '172.16.0.2', 'Alocado', 'Cliente B'),
(3, 'IP v6', '2001:db8::3', 'Disponível', NULL);

-- Insere Eventos
INSERT INTO eventos (equipamento_id, timestamp, tipo_evento, descricao) VALUES
(1, '2025-06-01 10:00:00', 'Status Change', 'Status alterado de Offline para Online'),
(2, '2025-06-02 14:30:00', 'Resource Allocated', 'Recurso 1 alocado ao cliente Cliente X'),
(3, '2025-06-03 08:15:00', 'Resource Deallocated', 'Recurso 6 desalocado com sucesso');