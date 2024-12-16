import os
import numpy as np


# scoring system for matches and mismatches
def score(nuc1: str, nuc2: str, score_matrix, i, j) -> int:
    if nuc1 == nuc2:
        print(f"match of {nuc1} and {nuc2}")
        print("i: ", i)
        print("j: ", j)
        score_matrix[i][j] = 1
        print("score_matrix: \n", score_matrix, "\n")
        return 1
    else:
        print(f"mismatch of {nuc1} and {nuc2}")
        print("i: ", i)
        print("j: ", j)
        score_matrix[i][j] = -1
        print("score_matrix: \n", score_matrix, "\n")
        return -1


   


# backtrace after calculating score matrix to find optimal alignment(s)
def find_alignment(seq1, seq2, gap_penalty, alignment_matrix, score_matrix):
    seq1_alignment = ""
    seq2_alignment = ""

    i = len(seq1)
    j = len(seq2)

    # keep track of score for alignment
    tot_score = 0
    
    while (i > 0 or j > 0):
        # if match or mismatch
        if (i > 0 and j > 0 and alignment_matrix[i][j] == alignment_matrix[i-1][j-1] + score_matrix[i-1][j-1]):
            seq1_alignment = seq1[i-1] + seq1_alignment
            seq2_alignment = seq2[j-1] + seq2_alignment
            tot_score += score_matrix[i-1][j-1]
            i -= 1
            j -= 1
            print("score matrix: ", score_matrix[i-1][j-1])
            print("tot_score:", tot_score)
        # if gap for sequence 2
        elif (i > 0 and alignment_matrix[i][j] == alignment_matrix[i-1, j] + gap_penalty):
            seq1_alignment = seq1[i-1] + seq1_alignment
            seq2_alignment = "_" + seq2_alignment
            i -= 1
            tot_score += gap_penalty
            print(f"score matrix{i}{j}: ", score_matrix[i-1][j-1])
            print()
            print("tot_score:", tot_score)
        # if gap for sequence 1
        else:
            seq1_alignment = "_" + seq1_alignment
            seq2_alignment = seq2[j-1] + seq2_alignment
            j -= 1
            tot_score += gap_penalty
            print("score matrix: ", score_matrix[i-1][j-1])
            print("tot_score:", tot_score)
    
    return seq1_alignment, seq2_alignment, tot_score


# prob need to define what's returned later
def calculate_aligment_matrix(sequence1: str, sequence2: str, gap_penalty, score_matrix):

    
    # intialize sequence 1
    seq1 = sequence1
    # initialize sequence 2
    seq2 = sequence2

    print("seq1: ", seq1)
    print("seq2: ", seq2)

    print("seq 1 length: ", len(seq1))
    print("seq 2 length: ", len(seq2))



    # initialize scoring matrix, double check if lengths are correct
    alignment_matrix = np.zeros((len(seq1) + 1, len(seq2) + 1))

    for i in range(len(seq1) + 1):
        alignment_matrix[i][0] = gap_penalty * i
    for j in range(len(seq2) + 1):
        alignment_matrix[0][j] = gap_penalty * j

    print("alignment matrix: \n", alignment_matrix)



    # calculate score, match/mistmatch +1, -1 for now
    for i in range(0, len(seq1)):
        for j in range(0, len(seq2)):
           print(f"nuc1: {seq1[i]}, nuc2: {seq2[j]}")
           match = alignment_matrix[i, j] + score(seq1[i], seq2[j], score_matrix, i, j)
           print("match: ", match)
           delete = alignment_matrix[i, j+1] + gap_penalty
           print("delete: ", delete)
           insert = alignment_matrix[i+1, j] + gap_penalty
           [print("insert: ", insert)]
           alignment_matrix[i+1, j+1] = max(match, delete, insert)
           print("alignment matrix: \n", alignment_matrix)
    

    return alignment_matrix



if __name__ == "__main__":
    seq1 = 'GATTACA'
    seq2 = 'GCATGCG'
    gap_penalty = -1

    # initialize score_matrix
    score_matrix = np.zeros((len(seq1), len(seq2)))
    print("score_matrix: \n", score_matrix, "\n")

    alignment_matrix = calculate_aligment_matrix(seq1, seq2, gap_penalty, score_matrix)
    seq1_align, seq2_align, tot_score = find_alignment(seq1, seq2, gap_penalty, alignment_matrix, score_matrix)
    
    print(seq1_align)
    print(seq2_align)
    print("tot_score:", tot_score)
