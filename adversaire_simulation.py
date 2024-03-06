import pandas as pd
import numpy as np
from mdp import run as run_mdp
import random

printer = run_mdp(path = "prof_examples//simu-mc.mdp", return_printer=True, print_transactions=True)

def gerar_preferencias_acoes(df, estados, acoes, modo="input"):
    """
    Generates a dictionary mapping each state to a list of preferred actions.

    This function allows for the specification of action preferences for each state
    within a Markov Decision Process (MDP), either through direct user input or
    by generating a random order of actions.

    Parameters:
    - df (pandas.DataFrame): A DataFrame containing the transition probabilities for each state-action pair.
    - estados (list): A list of all states declared in the MDP.
    - acoes (list): A list of all actions declared in the MDP.
    - modo (str): The mode of preference generation, either 'input' for user-defined preferences or 'random' for automatically generated preferences.

    Returns:
    - dict: A dictionary where keys are states and values are lists of actions, ordered by preference.
    """
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
                preferred = input(f"Type in the preferred action for {estado} \n").strip()
                while preferred not in acoes_validas:
                    preferred = input(f"he inputed action {preferred} isn't available for this state, choose one in {acoes_validas} \n").strip()
                preferencias[estado] = [preferred]

        elif modo == "random":
            random.shuffle(acoes_validas)
            preferencias[estado] = acoes_validas
            
    return preferencias


def simular_random_walk(p):
    """
    Simulates a random walk through an MDP based on action preferences and transition probabilities.

    This function simulates traversing through a Markov Decision Process, making decisions at each state
    based on predefined or user-specified action preferences. It illustrates the potential path an agent
    might take, considering the MDP's transition probabilities for each action.

    Parameters:
    - p: An object containing the MDP structure, including its states, actions, transition probabilities, and other relevant data.

    Returns:
    - None: This function does not return a value but prints the simulation results, including the traversed path, actions taken, probabilities of transitions, and the total path probability.
    """
        
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
        if df_estado_atual.empty:
            print("Stopped at a end of graph state")
            return
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