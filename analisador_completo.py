import os

# =====================================================================
# PARTE 1: ANALISADOR LÉXICO
# =====================================================================
afd = {
    'q0': {'s': 'q1', 'f': 'q7', 'v': 'q22', 'o': 'q42', 'c': 'q16_q25', 't': 'q33_q37', 'w': 'q11_q29'},
    'q1': {'e': 'q2'},
    'q2': {'l': 'q3'},
    'q3': {'e': 'q4'},
    'q4': {'c': 'q5'},
    'q5': {'t': 'q6'},
    'q7': {'r': 'q8'},
    'q8': {'o': 'q9'},
    'q9': {'m': 'q10'},
    'q22': {'a': 'q23'},
    'q23': {'r': 'q24'},
    'q42': {'p': 'q43'},
    'q16_q25': {'r': 'q17', 'a': 'q26'},
    'q17': {'e': 'q18'},
    'q18': {'a': 'q19'},
    'q19': {'t': 'q20'},
    'q20': {'e': 'q21'},
    'q26': {'s': 'q27'},
    'q27': {'e': 'q28'},
    'q33_q37': {'h': 'q34', 'a': 'q38'},
    'q34': {'e': 'q35'},
    'q35': {'n': 'q36'},
    'q38': {'b': 'q39'},
    'q39': {'l': 'q40'},
    'q40': {'e': 'q41'},
    'q11_q29': {'h': 'q12_q30'},
    'q12_q30': {'e': 'q13_q31'},
    'q13_q31': {'r': 'q14', 'n': 'q32'},
    'q14': {'e': 'q15'},
    'q32': {}
}

estados_finais = ['q6', 'q10', 'q15', 'q21', 'q24', 'q28', 'q32', 'q36', 'q41', 'q43']

def transicao(token):
    estado = 'q0'
    for letra in token:
        if estado in afd and letra in afd.get(estado, {}):
            estado = afd[estado][letra]
        else:
            if all(c.isalnum() or c == '_' for c in token): return 'q24'
            if token in ['=', '>', '<', '>=', '<=', '!=']: return 'q43'
            return 'X'
    return estado if estado in estados_finais else 'X'

def processar_entrada(caminho_arquivo):
    tabela_simbolos = []
    fita_saida = []
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: O arquivo de entrada '{caminho_arquivo}' não foi encontrado.")
        return None, None
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    for numero_linha, linha in enumerate(linhas, start=1):
        tokens = linha.strip().split()
        for token in tokens:
            estado_final = transicao(token)
            fita_saida.append(estado_final)
            # Adiciona um ID único para cada token na tabela de símbolos
            tabela_simbolos.append({'id': len(tabela_simbolos), 'linha': numero_linha, 'identificador': token, 'estado': estado_final})
    return fita_saida, tabela_simbolos

# =====================================================================
# PARTE 2: ANALISADOR SINTÁTICO COM AÇÕES SEMÂNTICAS APRIMORADAS
# =====================================================================

def analisador_sintatico(fita_tokens, tabela_simbolos, tabela_slr, regras_gramatica):
    fita_tokens.append(('$', '$', -1))

    pilha = [0]
    ponteiro = 0
    codigo_intermediario = []

    print("\n--- Iniciando Análise Sintática ---")
    print(f"{'Pilha':<40} | {'Fita de Entrada':<40} | {'Ação'}")
    print("-" * 100)

    while True:
        try:
            estado_atual = pilha[-1]
            token_info = fita_tokens[ponteiro]
            tipo_token_atual = token_info[1]
            pilha_str = ' '.join(map(str, pilha))
            fita_str = ' '.join(t[1] for t in fita_tokens[ponteiro:])
            print(f"{pilha_str:<40} | {fita_str:<40} | ", end="")
            acao = tabela_slr[estado_atual][tipo_token_atual]

            if acao.startswith('s'):
                proximo_estado = int(acao[1:])
                print(f"Shift para o estado {proximo_estado}")
                pilha.append(token_info)
                pilha.append(proximo_estado)
                ponteiro += 1
            elif acao.startswith('r'):
                num_regra = int(acao[1:])
                regra = regras_gramatica[num_regra]
                cabeca, corpo = regra
                print(f"Reduce usando a regra {num_regra}: {cabeca} -> {' '.join(corpo) if corpo else 'ε'}")

                if num_regra == 3:
                    _, _, token_id = pilha[-2]
                    tabela_simbolos[token_id]['categoria'] = 'NOME_DE_TABELA_CRIADA'
                elif num_regra == 4:
                    _, _, token_id1 = pilha[-6]
                    _, _, token_id2 = pilha[-2]
                    tabela_simbolos[token_id1]['categoria'] = 'NOME_DE_VIEW_CRIADA'
                    tabela_simbolos[token_id2]['categoria'] = 'TABELA_ORIGEM_CREATE_FROM'
                elif num_regra == 5:
                    _, _, token_id = pilha[-4]
                    tabela_simbolos[token_id]['categoria'] = 'TABELA_EM_FROM'
                elif num_regra == 8:
                    _, _, token_id = pilha[-2]
                    tabela_simbolos[token_id]['categoria'] = 'IDENTIFICADOR_EM_SELECT'
                elif num_regra == 13:
                    _, _, token_id = pilha[-2]
                    tabela_simbolos[token_id]['categoria'] = 'VALOR_RESULTADO_CASE'
                elif num_regra == 14:
                    var1_token_info = pilha[-6]
                    op_token_info = pilha[-4]
                    var2_token_info = pilha[-2]

                    var1_lexema = var1_token_info[0]
                    op_lexema = op_token_info[0]
                    var2_lexema = var2_token_info[0]

                    var1_id_ts = var1_token_info[2]
                    var2_id_ts = var2_token_info[2]

                    sym1 = tabela_simbolos[var1_id_ts]
                    sym2 = tabela_simbolos[var2_id_ts]

                    if 'tipo' not in sym1:
                        sym1['tipo'] = 'NUMERIC_OR_STRING'
                    if 'tipo' not in sym2:
                        sym2['tipo'] = 'NUMERIC_OR_STRING'

                    if sym1['tipo'] != sym2['tipo']:
                        print(
                            f"ERRO SEMÂNTICO na linha {sym1['linha']}: Tipos incompatíveis na condição '{sym1['identificador']} {op_lexema} {sym2['identificador']}'. ('{sym1['tipo']}' vs '{sym2['tipo']}')")
                        return False, f"Erro semântico: Tipos incompatíveis na linha {sym1['linha']}"

                    tabela_simbolos[var1_id_ts]['categoria'] = 'IDENTIFICADOR_EM_CONDICAO'
                    tabela_simbolos[var2_id_ts]['categoria'] = 'VALOR_EM_CONDICAO'

                    label_true = f"L{len(codigo_intermediario) + 1}_TRUE"
                    label_false = f"L{len(codigo_intermediario) + 2}_FALSE"

                    if op_lexema == '=':
                        codigo_intermediario.append(f"IF_EQ {var1_lexema}, {var2_lexema} GOTO {label_true}")
                    elif op_lexema == '>':
                        codigo_intermediario.append(f"IF_GT {var1_lexema}, {var2_lexema} GOTO {label_true}")
                    elif op_lexema == '<':
                        codigo_intermediario.append(f"IF_LT {var1_lexema}, {var2_lexema} GOTO {label_true}")

                    codigo_intermediario.append(f"GOTO {label_false}")
                    codigo_intermediario.append(f"{label_true}:")

                if corpo:
                    for _ in range(2 * len(corpo)):
                        pilha.pop()
                estado_goto = pilha[-1]
                pilha.append(cabeca)
                pilha.append(tabela_slr[estado_goto][cabeca])

            elif acao == 'acc':
                print("Accept: Análise sintática concluída com sucesso.")
                print("\n--- Código Intermediário Gerado (Exemplo para CONDICAO) ---")
                if codigo_intermediario:
                    for instr in codigo_intermediario:
                        print(instr)
                else:
                    print("Nenhum código intermediário gerado para a regra demonstrada.")
                return True, "Aceito"
            else:
                raise ValueError(f"Ação inválida: {acao}")
        except (KeyError, IndexError):
            linha_erro = tabela_simbolos[ponteiro]['linha'] if ponteiro < len(tabela_simbolos) else 'desconhecida'
            token_causador = fita_tokens[ponteiro][1] if ponteiro < len(fita_tokens) else 'fim de arquivo'
            msg_erro = f"Erro sintático na linha {linha_erro}: token inesperado '{token_causador}'."
            print(f"\nERRO: {msg_erro}")
            return False, msg_erro


# =====================================================================
# PARTE 3: INTEGRAÇÃO E EXECUÇÃO
# =====================================================================

regras_gramatica = [
    ("PROGRAMA'", ["PROGRAMA"]),
    ("PROGRAMA", ["PROGRAMA", "COMANDO"]),
    ("PROGRAMA", ["COMANDO"]),
    ("COMANDO", ["create", "table", "var"]),
    ("COMANDO", ["create", "var", "from", "var"]),
    ("COMANDO", ["select", "PARTE_SELECT", "from", "var", "PARTE_WHERE"]),
    ("PARTE_SELECT", ["ELEMENTO_SELECT"]),
    ("PARTE_SELECT", ["ELEMENTO_SELECT", "PARTE_SELECT"]),
    ("ELEMENTO_SELECT", ["var"]),
    ("ELEMENTO_SELECT", ["EXP_CASE"]),
    ("EXP_CASE", ["case", "LISTA_WHEN"]),
    ("LISTA_WHEN", ["CLAUSULA_WHEN"]),
    ("LISTA_WHEN", ["CLAUSULA_WHEN", "LISTA_WHEN"]),
    ("CLAUSULA_WHEN", ["when", "CONDICAO", "then", "var"]),
    ("CONDICAO", ["var", "op", "var"]),
    ("PARTE_WHERE", ["where", "CONDICAO"]),
    ("PARTE_WHERE", ["where", "EXP_CASE", "op", "var"]),
    ("PARTE_WHERE", [])
]

tabela_slr = {
    0: {'create': 's3', 'select': 's4', 'PROGRAMA': 1, 'COMANDO': 2},
    1: {'create': 's3', 'select': 's4', '$': 'acc', 'COMANDO': 5},
    2: {'create': 'r2', 'select': 'r2', '$': 'r2'},
    3: {'table': 's6', 'var': 's7'},
    4: {'var': 's10', 'case': 's12', 'PARTE_SELECT': 8, 'ELEMENTO_SELECT': 9, 'EXP_CASE': 11},
    5: {'create': 'r1', 'select': 'r1', '$': 'r1'},
    6: {'var': 's13'},
    7: {'from': 's14'},
    8: {'from': 's15'},
    9: {'var': 's10', 'case': 's12', 'from': 'r6', 'PARTE_SELECT': 16, 'ELEMENTO_SELECT': 9, 'EXP_CASE': 11},
    10: {'var': 'r8', 'case': 'r8', 'from': 'r8', 'then': 'r8'},
    11: {'var': 'r9', 'case': 'r9', 'from': 'r9', 'then': 'r9'},
    12: {'when': 's19', 'LISTA_WHEN': 17, 'CLAUSULA_WHEN': 18},
    13: {'create': 'r3', 'select': 'r3', '$': 'r3'},
    14: {'var': 's20'},
    15: {'var': 's21'},
    16: {'from': 'r7'},
    17: {'from': 'r10', 'then': 'r10'},
    18: {'when': 's19', 'from': 'r11', 'then': 'r11', 'LISTA_WHEN': 22, 'CLAUSULA_WHEN': 18},
    19: {'var': 's24', 'CONDICAO': 23},
    20: {'create': 'r4', 'select': 'r4', '$': 'r4'},
    21: {'where': 's26', 'create': 'r17', 'select': 'r17', '$': 'r17', 'PARTE_WHERE': 25},
    22: {'from': 'r12', 'then': 'r12'}, 23: {'then': 's27'}, 24: {'op': 's28'},
    25: {'create': 'r5', 'select': 'r5', '$': 'r5'},
    26: {'var': 's24', 'case': 's12', 'CONDICAO': 30, 'EXP_CASE': 29},
    27: {'var': 's31'}, 28: {'var': 's32'}, 29: {'op': 's33'},
    30: {'create': 'r15', 'select': 'r15', '$': 'r15'},
    31: {'when': 'r13', 'from': 'r13', 'then': 'r13'},
    32: {'then': 'r14', 'create': 'r14', 'select': 'r14', '$': 'r14'},
    33: {'var': 's34'}, 34: {'create': 'r16', 'select': 'r16', '$': 'r16'}
}

mapa_estado_para_tipo = {
    'q6': 'select',
    'q10': 'from',
    'q15': 'where',
    'q21': 'create',
    'q24': 'var',
    'q28': 'case',
    'q32': 'when',
    'q36': 'then',
    'q41': 'table',
    'q43': 'op'
}

if __name__ == "__main__":
    caminho_arquivo = 'entrada.txt'
    print(f"Lendo arquivo de entrada: {caminho_arquivo}")
    fita_estados, tabela_simbolos = processar_entrada(caminho_arquivo)
    if not tabela_slr:
        print("\nERRO CRÍTICO: A variável 'tabela_slr' está vazia.")
    elif fita_estados is None:
        print("Análise interrompida devido a erro na leitura do arquivo.")
    else:
        fita_tokens = []
        erro_lexico = False
        for i, simbolo in enumerate(tabela_simbolos):
            estado = simbolo['estado']
            if estado in mapa_estado_para_tipo:
                tipo = mapa_estado_para_tipo[estado]
                lexema = simbolo['identificador']
                # Adiciona o ID único do token à fita
                fita_tokens.append((lexema, tipo, simbolo['id']))
            else:
                linha = simbolo['linha']
                token = simbolo['identificador']
                print(f"ERRO LÉXICO na linha {linha}: Token '{token}' não reconhecido.")
                erro_lexico = True
                break
        if not erro_lexico:
            sucesso, mensagem = analisador_sintatico(fita_tokens, tabela_simbolos, tabela_slr, regras_gramatica)
            print("\n--- Resultado Final da Análise ---")
            print(f"Status: {mensagem}")

            if sucesso:
                print("\n--- Tabela de Símbolos Enriquecida ---")
                print(f"{'ID':<4} {'Linha':<6} {'Token':<20} {'Categoria':<30}")
                print("-" * 64)
                for simb in tabela_simbolos:
                    categoria = simb.get('categoria', 'N/A')
                    print(f"{simb['id']:<4} {simb['linha']:<6} {simb['identificador']:<20} {categoria:<30}")
