import numpy as np
import json

def main():
    START_LINK = 'https://atom.io'

    trans_mat = np.loadtxt('transition_matrix.out')
    with open ('link_ids.json', 'r') as fin:
        link_ids = json.load(fin)

    state_vector = np.zeros((len(trans_mat)))
    state_vector[link_ids[START_LINK]] = 1

    for _ in range(100):
        state_vector = np.matmul(trans_mat, state_vector)

        likely_site = np.argmax(state_vector)
        state_vector = np.zeros(len(state_vector))
        state_vector[likely_site] = 1

    link_ids_inverted = {value: key for key, value in link_ids.items()}
    print(likely_site, link_ids_inverted[likely_site])

if __name__ == '__main__':
    main()
