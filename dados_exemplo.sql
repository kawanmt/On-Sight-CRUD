USE `mydb`;

-- Limpa as tabelas antes (ordem inversa das dependências), assim o script
-- pode ser rodado de novo para "resetar" os dados de teste.
DELETE FROM partida;
DELETE FROM serie;
DELETE FROM participantes;
DELETE FROM config;
DELETE FROM jogador;
DELETE FROM campeonato;
DELETE FROM time;

INSERT INTO time (id, nome, ranking, titulos) VALUES
  (1, 'FURIA',    8,  3),
  (2, 'Vitality', 1, 12),
  (3, 'G2',       5,  9),
  (4, 'MIBR',    20,  2);

INSERT INTO jogador (id, nome, idade, nick, ganhos, rating, time_id, premiacoes) VALUES
  (1, 'Lucas Andrade',   24, 'lukz',    450000, 1.12, 1, 6),
  (2, 'Rafael Moura',    27, 'rafx',    620000, 1.05, 1, 9),
  (3, 'Pierre Lambert',  23, 'plmb',   1300000, 1.28, 2, 15),
  (4, 'Nikola Petrov',   26, 'nkp',     910000, 1.09, 3, 11),
  (5, 'Bruno Teixeira',  21, 'brt',      80000, 0.98, 4, 1),
  (6, 'Caio Ramos',      22, 'kayo',      5000, 0.95, NULL, 0);  -- sem time

INSERT INTO config (id_jogador, dpi, sensibilidade, resolucao, cod_mira) VALUES
  (1, 400, 2.00, '1280x960',  'CSGO-a1b2c-d3e4f-g5h6i'),
  (2, 800, 1.10, '1920x1080', 'CSGO-j7k8l-m9n0o-p1q2r'),
  (3, 400, 1.75, '1280x960',  NULL);

INSERT INTO campeonato (id, nome, localizacao, premiacao_total, fase) VALUES
  (1, 'IEM Rio',        'Rio de Janeiro', 1000000, 'playoffs'),
  (2, 'Major Cologne',  'Colônia',        1250000, 'grupos');

INSERT INTO participantes (id_campeonato, id_time, classificacao, premiacao) VALUES
  (1, 1, 0, 0),
  (1, 2, 0, 0),
  (1, 3, 0, 0),
  (2, 2, 0, 0);

INSERT INTO serie (id, id_campeonato, id_time1, id_time2, id_vencedor, status, formato, fase) VALUES
  (1, 1,    1, 2, 2,    'finalizada',   'MD3', 'semifinal'),
  (2, 1,    3, 1, NULL, 'em andamento', 'MD3', 'quartas'),
  (3, NULL, 1, 4, NULL, 'agendada',     'MD1', 'showmatch');  -- fora de campeonato

INSERT INTO partida (id, id_serie, id_vencedor, id_perdedor, mapa, placar, ordem) VALUES
  (1, 1, 1, 2, 'Mirage',  '13-9',  1),
  (2, 1, 2, 1, 'Inferno', '13-11', 2),
  (3, 1, 2, 1, 'Nuke',    '13-7',  3),
  (4, 2, 3, 1, 'Ancient', '13-10', 1);
