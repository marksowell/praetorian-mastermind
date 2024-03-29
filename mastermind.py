import sys
import itertools
import multiprocessing
from functools import partial
from random import sample
import interface
import time

class RestartException(Exception):
    pass

def get_core_count():
    return multiprocessing.cpu_count()

def random_guess(alphabet, k):
    return sample(alphabet, k)

def all_solutions(alphabet, k, use_combinations=False):
    if use_combinations:
        return list(itertools.combinations(alphabet, k))
    else:
        return list(itertools.permutations(alphabet, k))

def filter_matching_result_combinations(S, w_guess, w_score):
    correct, _ = w_score
    S_pruned = []
    for s in S:
        if len(set(s) & set(w_guess)) == correct:
            S_pruned.append(s)
    return S_pruned

def score_combinations(w_1, w_2):
    correct = len(set(w_1) & set(w_2))
    return correct, 0

def best_move_combinations(S):
    if not S:
        return []
    return S[0]

def filter_wrapper(a, b, c, d):
    return filter_matching_result(d, a, b, c)

def filter_matching_result(S, w_guess, w_score, max_itr=100000000):
    S_pruned = []
    for s in S:
        if score(w_guess, s) == w_score:
            S_pruned.append(s)
    return S_pruned

def score(w_1, w_2):
    match_score = [0, 0]
    w_1_set, w_2_set = set(w_1), set(w_2)
    match_score[0] = len(w_1_set & w_2_set)
    match_score[1] = sum(a == b for a, b in zip(w_1, w_2))
    return match_score

def best_move(S):
    if not S:
        return []
    return S[0]

def run(CORES, reset_count):
    start_time = time.time()  # Start timing the execution
    iterations = -1
    level = 1
    guesses_made = 0
    S = []
    current_guess = []
    current_score = []

    state = interface.get_new_level(level)
    while True:
        iterations += 1
        for key in state:
            if key in ['message', 'roundsLeft'] or iterations == 0:
                if key == 'message':
                    print(state['message'])
                    print('')
                    level += 1

                state = interface.get_new_level(level)

                for key in state:
                    if key == 'error':
                        print(state[key])
                        c_hash = str(interface.get_hash())
                        print("Hash: " + c_hash)
                        end_time = time.time()  # End timing
                        print(f"The solver took {end_time - start_time:.2f} seconds, {guesses_made} guesses, and {reset_count} resets to solve and get the hash.")
                        with open('hash.txt', 'a+') as f:
                            f.write("\n")
                            f.write(c_hash)
                        return 0

                num_weapons = list(range(state['numWeapons']))
                num_gladiators = state['numGladiators']
                print("LEVEL: " + str(level))
                print("---------------")
                print(" A := {" + str(num_weapons)[1:-1] + "}")
                print("|A| := " + str(state["numWeapons"]))
                print("|w| := " + str(state["numGladiators"]))

                if level != 4:
                    S = all_solutions(num_weapons, num_gladiators, use_combinations=False)
                else:
                    S = all_solutions(num_weapons, num_gladiators, use_combinations=True)
                    print("|S| = " + str(len(S)))
                    print("--------")

                current_guess = random_guess(num_weapons, num_gladiators)
                print("Initial Guess: " + str(current_guess))
                state = interface.submit_guess(level, current_guess)
                break

        if 'response' in state:
            guesses_made += 1
            current_score = state['response']
            if level == 4:
                if current_score[0] == num_gladiators:  # Correct weapons found
                    print("Correct weapons found:", current_guess)
                    # Generate permutations for found weapons to find the correct order
                    S = all_solutions(current_guess, num_gladiators, use_combinations=False)
                    correct_order_found = False
                    while not correct_order_found:  # Continue until the correct order is found
                        current_guess = best_move(S)
                        state = interface.submit_guess(level, current_guess)
                        if 'response' in state:
                            current_score = state['response']
                            if current_score[1] == num_gladiators:  # Correct order found
                                print("Correct order found:", current_guess)
                                correct_order_found = True
                                # Retrieve and print the hash
                                final_hash = interface.get_hash()
                                break  # Exit the loop since the correct order has been found
                            else:
                                S = filter_matching_result(S, current_guess, current_score)
                                print("|S| reduced to " + str(len(S)))
                        else:
                            break
                else:
                    S = filter_matching_result_combinations(S, current_guess, current_score)
                    print("|S| reduced to " + str(len(S)))
                    if S:
                        current_guess = best_move_combinations(S)
                        state = interface.submit_guess(level, current_guess)
                    else:
                        print("No viable solutions left, something went wrong.")
                        break
            else:
                pool = multiprocessing.Pool(processes=CORES)
                divide_S = [S[i::CORES] for i in range(CORES)]
                p_filter = partial(filter_wrapper, current_guess, current_score, 20000)
                S = pool.map_async(p_filter, divide_S).get(10)
                pool.close()
                pool.join()
                S = [item for sublist in S for item in sublist]
                print("|S| reduced to " + str(len(S)))
                current_guess = best_move(S)
                state = interface.submit_guess(level, current_guess)
        else:
            raise RestartException

def main(CORES):
    reset_count = 0
    while True:
        try:
            interface.reset_game()
            run(CORES, reset_count)
            break
        except RestartException:
            print("Restarting due to error state...")
            reset_count += 1

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')
    total_cores = get_core_count()
    cores_to_use = max(1, total_cores - 1)
    print(f"Using CPU cores: {cores_to_use}")
    main(cores_to_use)
