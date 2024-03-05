import pandas as pd
import numpy as np
from mdp import run as run_mdp
import random

printer = run_mdp(path = "correct_ex.mdp", return_printer=True, print_transactions=True)

def gerar_preferencias_acoes(df, estados, acoes, modo="input"):
    preferencias = {}

    for estado in estados:
        acoes_possiveis = df[df['Origin'] == estado]['Action'].unique()
        
        # Filtrar ações possíveis que não sejam 'NA', caso existam
        acoes_validas = [acao for acao in acoes_possiveis if acao != "NA"]
        
        if modo == "input":
            # Se houver apenas uma ação válida ou a ação é 'NA', seleção automática
            if len(acoes_validas) <= 1:
                preferencias[estado] = acoes_validas if acoes_validas else ["NA"]
            else:
                print(f"\nCurrent State: {estado}")
                print("Possible Actions: " + ", ".join(acoes_validas))
                preferencia_str = input(f"Type in the actions in preferred order for the State {estado} (separate with commas): ")
                preferencia_lista = [acao.strip() for acao in preferencia_str.split(",") if acao.strip() in acoes_validas]
                preferencias[estado] = preferencia_lista

        elif modo == "random":
            random.shuffle(acoes_validas)
            preferencias[estado] = acoes_validas
            
    return preferencias


def simular_random_walk(p):
    # "p" is a printer object
    
    df = p.transactions_prob

    print("\n" + "="*20 + " # " + "="*20)
    adversaire_mode = input(
        "Let us build an Adversaire to decide the actions. \n"
        "You can choose between: \n"
        "- 'input' to input your preferences \n"
        "- 'random' to have a random permutation of the possible actions: ")
    num_transitions = int(input("\n Please choose the number of transitions for this random walk: "))


    preferencias = gerar_preferencias_acoes(df, p.declared_states,p.declared_actions, modo=adversaire_mode)
    print("Here are the prefered actions for each state :", preferencias, "\n")

    estado_atual = p.first_state

    caminho = estado_atual  # Iniciar o registro do caminho com o estado inicial
    probabilidade_acumulada = 1

    print(f"Inicial State: {estado_atual}" + "\n")

    for _ in range(num_transitions):
        df_estado_atual = df[df['Origin'] == estado_atual]
        acao_selecionada = None
        probabilidade_escolhida = None

        if df_estado_atual.iloc[0]['Action'] == "NA":
            probabilidades = df_estado_atual.iloc[0, 2:].astype(float).values
            acao_selecionada = "NA"
        else:
            for acao_preferida in preferencias[estado_atual]:
                df_acao_preferida = df_estado_atual[df_estado_atual['Action'] == acao_preferida]
                if not df_acao_preferida.empty:
                    probabilidades = df_acao_preferida.iloc[0, 2:].astype(float).values
                    acao_selecionada = acao_preferida
                    break

        probabilidades = probabilidades / np.sum(probabilidades)
        estados_possiveis = df_estado_atual.columns[2:]
        proximo_estado = np.random.choice(estados_possiveis, p=probabilidades)
        probabilidade_escolhida = probabilidades[np.where(estados_possiveis == proximo_estado)[0][0]]
        
        probabilidade_acumulada *= probabilidade_escolhida
        estado_passado = estado_atual
        estado_atual = proximo_estado
        caminho += f" -> {estado_atual}"  # Atualizar o caminho

        print(f"{estado_passado} -> {estado_atual}; action: {acao_selecionada}, probability of step  {probabilidade_escolhida:.3f}; path's total probability {probabilidade_acumulada:.5f}, path: {caminho}," + "\n")

    print(f"Complete Path: {caminho}")

simular_random_walk(printer)