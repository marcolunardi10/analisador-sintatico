Tabela de Conjuntos de Itens Válidos e Transições (Goto)
--- ESTADO 0 ---
Itens:
PROGRAMA' -> .PROGRAMA
PROGRAMA -> .COMANDO
COMANDO -> .create table var
COMANDO -> .create var from var
COMANDO -> .select PARTE_SELECT from var PARTE_WHERE
Transições:
PROGRAMA -> 1
COMANDO -> 2
create -> 3
select -> 4

--- ESTADO 1 ---
Itens:
PROGRAMA' -> PROGRAMA .COMANDO
COMANDO -> .create table var
COMANDO -> .create var from var
COMANDO -> .select PARTE_SELECT from var PARTE_WHERE
Transições:
COMANDO -> 5
create -> 3
select -> 4

--- ESTADO 2 ---
Itens:
PROGRAMA -> COMANDO .
Transições:
(nenhuma)

--- ESTADO 3 ---
Itens:
COMANDO -> create .table var
COMANDO -> create .var from var
Transições:
table -> 6
var -> 7

--- ESTADO 4 ---
Itens:
COMANDO -> select .PARTE_SELECT from var PARTE_WHERE
PARTE_SELECT -> .ELEMENTO_SELECT
PARTE_SELECT -> .ELEMENTO_SELECT PARTE_SELECT
ELEMENTO_SELECT -> .var
ELEMENTO_SELECT -> .EXP_CASE
EXP_CASE -> .case LISTA_WHEN
Transições:
PARTE_SELECT -> 8
ELEMENTO_SELECT -> 9
var -> 10
EXP_CASE -> 11
case -> 12

--- ESTADO 5 ---
Itens:
PROGRAMA' -> PROGRAMA COMANDO .
Transições:
(nenhuma)

--- ESTADO 6 ---
Itens:
COMANDO -> create table .var
Transições:
var -> 13

--- ESTADO 7 ---
Itens:
COMANDO -> create var .from var
Transições:
from -> 14

--- ESTADO 8 ---
Itens:
COMANDO -> select PARTE_SELECT .from var PARTE_WHERE
Transições:
from -> 15

--- ESTADO 9 ---
Itens:
PARTE_SELECT -> ELEMENTO_SELECT .
PARTE_SELECT -> ELEMENTO_SELECT .PARTE_SELECT
PARTE_SELECT -> .ELEMENTO_SELECT
PARTE_SELECT -> .ELEMENTO_SELECT PARTE_SELECT
ELEMENTO_SELECT -> .var
ELEMENTO_SELECT -> .EXP_CASE
EXP_CASE -> .case LISTA_WHEN
Transições:
PARTE_SELECT -> 16
ELEMENTO_SELECT -> 9
var -> 10
EXP_CASE -> 11
case -> 12

--- ESTADO 10 ---
Itens:
ELEMENTO_SELECT -> var .
Transições:
(nenhuma)

--- ESTADO 11 ---
Itens:
ELEMENTO_SELECT -> EXP_CASE .
Transições:
(nenhuma)

--- ESTADO 12 ---
Itens:
EXP_CASE -> case .LISTA_WHEN
LISTA_WHEN -> .CLAUSULA_WHEN
LISTA_WHEN -> .CLAUSULA_WHEN LISTA_WHEN
CLAUSULA_WHEN -> .when CONDICAO then var
Transições:
LISTA_WHEN -> 17
CLAUSULA_WHEN -> 18
when -> 19

--- ESTADO 13 ---
Itens:
COMANDO -> create table var .
Transições:
(nenhuma)

--- ESTADO 14 ---
Itens:
COMANDO -> create var from .var
Transições:
var -> 20

--- ESTADO 15 ---
Itens:
COMANDO -> select PARTE_SELECT from .var PARTE_WHERE
Transições:
var -> 21

--- ESTADO 16 ---
Itens:
PARTE_SELECT -> ELEMENTO_SELECT PARTE_SELECT .
Transições:
(nenhuma)

--- ESTADO 17 ---
Itens:
EXP_CASE -> case LISTA_WHEN .
Transições:
(nenhuma)

--- ESTADO 18 ---
Itens:
LISTA_WHEN -> CLAUSULA_WHEN .
LISTA_WHEN -> CLAUSULA_WHEN .LISTA_WHEN
LISTA_WHEN -> .CLAUSULA_WHEN
LISTA_WHEN -> .CLAUSULA_WHEN LISTA_WHEN
CLAUSULA_WHEN -> .when CONDICAO then var
Transições:
LISTA_WHEN -> 22
CLAUSULA_WHEN -> 18
when -> 19

--- ESTADO 19 ---
Itens:
CLAUSULA_WHEN -> when .CONDICAO then var
CONDICAO -> .var op var
Transições:
CONDICAO -> 23
var -> 24

--- ESTADO 20 ---
Itens:
COMANDO -> create var from var .
Transições:
(nenhuma)

--- ESTADO 21 ---
Itens:
COMANDO -> select PARTE_SELECT from var .PARTE_WHERE
PARTE_WHERE -> .
PARTE_WHERE -> .where CONDICAO
PARTE_WHERE -> .where EXP_CASE op var
Transições:
PARTE_WHERE -> 25
where -> 26

--- ESTADO 22 ---
Itens:
LISTA_WHEN -> CLAUSULA_WHEN LISTA_WHEN .
Transições:
(nenhuma)

--- ESTADO 23 ---
Itens:
CLAUSULA_WHEN -> when CONDICAO .then var
Transições:
then -> 27

--- ESTADO 24 ---
Itens:
CONDICAO -> var .op var
Transições:
op -> 28

--- ESTADO 25 ---
Itens:
COMANDO -> select PARTE_SELECT from var PARTE_WHERE .
Transições:
(nenhuma)

--- ESTADO 26 ---
Itens:
PARTE_WHERE -> where .CONDICAO
PARTE_WHERE -> where .EXP_CASE op var
CONDICAO -> .var op var
EXP_CASE -> .case LISTA_WHEN
Transições:
CONDICAO -> 29
EXP_CASE -> 30
var -> 24
case -> 12

--- ESTADO 27 ---
Itens:
CLAUSULA_WHEN -> when CONDICAO then .var
Transições:
var -> 31

--- ESTADO 28 ---
Itens:
CONDICAO -> var op .var
Transições:
var -> 32

--- ESTADO 29 ---
Itens:
PARTE_WHERE -> where CONDICAO .
Transições:
(nenhuma)

--- ESTADO 30 ---
Itens:
PARTE_WHERE -> where EXP_CASE .op var
Transições:
op -> 33

--- ESTADO 31 ---
Itens:
CLAUSULA_WHEN -> when CONDICAO then var .
Transições:
(nenhuma)

--- ESTADO 32 ---
Itens:
CONDICAO -> var op var .
Transições:
(nenhuma)

--- ESTADO 33 ---
Itens:
PARTE_WHERE -> where EXP_CASE op .var
Transições:
var -> 34

--- ESTADO 34 ---
Itens:
PARTE_WHERE -> where EXP_CASE op var .
Transições:
(nenhuma)