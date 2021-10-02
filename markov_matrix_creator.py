import numpy as np

def create_trans_mat(freq_mat):
    row_sums = np.sum(freq_mat, axis=1)

    for i in range(len(row_sums)): # normalize into probabilities
        if row_sums[i] != 0:
            freq_mat[i] /= row_sums[i]
        else:
            freq_mat[i, i] = 1 # assume our sample represents the entire web

    print(np.sum(freq_mat, axis=1))
    return freq_mat

def main():
    freq_mat = np.loadtxt('freq_mat.out')
    trans_mat = create_trans_mat(freq_mat)
    np.savetxt('transition_matrix.out', trans_mat)

if __name__ == '__main__':
    main()

