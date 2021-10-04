import numpy as np
import json

def run_markov_chain(start_link, trans_mat, num_iters):
    with open ('link_ids.json', 'r') as fin:
        link_ids = json.load(fin)

    state_vector = np.zeros((len(trans_mat)))
    state_vector[link_ids[start_link]] = 1

    for _ in range(num_iters):
        state_vector = np.matmul(trans_mat, state_vector)

        likely_site = np.argmax(state_vector)
        state_vector = np.zeros(len(state_vector))
        state_vector[likely_site] = 1

    link_ids_inverted = {value: key for key, value in link_ids.items()}
    return link_ids_inverted[likely_site]

def diagonalize(trans_mat): # P is noninvertible, cannot diagonalize
    eigval, eigvec = np.linalg.eig(trans_mat)

    for i in range(len(eigval)):
        if np.iscomplex(eigval[i]):
            np.delete(eigval, i)
            np.delete(eigvec, i, 0)

    P = eigvec.T
    D = np.eye(len(eigval))
    for i in range(len(eigval)):
        D[i, i] = eigval[i]

    return P, D, np.linalg.inv(P)

def main():
    START_LINK = 'https://github.com'
    trans_mat = np.loadtxt('transition_matrix.out')

    result = run_markov_chain(START_LINK, trans_mat, 1000)
    print(result)


if __name__ == '__main__':
    main()
