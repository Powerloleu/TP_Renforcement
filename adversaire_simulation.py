import pandas as pd
import numpy as np
from mdp import run as run_mdp
import random

printer = run_mdp(path = "correct_ex.mdp", return_printer=True)

def gerar_preferencias_acoes(estados, acoes, modo="input"):
    preferencias = {}

    for estado in estados:
        if modo == "input":
            print(f"\nCurrent State: {estado}")
            print("Possible Actions " + ", ".join(acoes))
            preferencia_str = input(f"Type in the actions in prefered order for the State {estado} (separate with commas): ")
            preferencia_lista = [acao.strip() for acao in preferencia_str.split(",") if acao.strip() in acoes]
            preferencias[estado] = preferencia_lista

        elif modo == "random":
            acoes_aleatorias = list(acoes)
            random.shuffle(acoes_aleatorias)
            preferencias[estado] = acoes_aleatorias
            
        else:
            print("Choose a mode between: 'input' or 'random'.")
            return {}

    return preferencias


def simular_random_walk(p):
    # "p" is a printer object
    
    df = p.transactions_prob

    print("\n="*20 + " # " + "="*20)
    adversaire_mode = input("\n Let us build and Adversaire to decide the actions, you can choose between 'input' to input your preferences or 'random' to have a random permuatation of the possible actions: ")
    num_transitions = int(input("\n Please choose the number of transitions for this random walk: "))


    preferencias = gerar_preferencias_acoes(p.declared_states, p.declared_actions, modo=adversaire_mode)
    print("Preferências de ações (modo random):", preferencias, "\n")

    estado_atual = p.first_state

    caminho = estado_atual  # Iniciar o registro do caminho com o estado inicial
    probabilidade_acumulada = 1

    print(f"Inicial State: {estado_atual}")

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

        print(f"Origin: {estado_passado}, Action: {acao_selecionada}, Destiny: {estado_atual}, Prob of next step: {probabilidade_escolhida:.3f}, Prob path up to here: {probabilidade_acumulada:.5f}, Path: {caminho}," + "\n")

    print(f"Complete Path: {caminho}")

simular_random_walk(printer)