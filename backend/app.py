from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import numpy as np
from alignment import *


app = Flask(__name__)
CORS(app, resources={r"/calculate_alignment": {"origins": "http://localhost:3000"}})


# adjust options for CORS
@app.route('/calculate_alignment', methods=['OPTIONS'])
def handle_preflight():
    response = jsonify({'message': 'preflight request successful'})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


# calculate N-W alignment score endpoint, post request for calculations
@app.route('/calculate_alignment', methods=['POST'])
def calculate_aligment():
    data = request.json

    if data is None:
        return jsonify({"error": "No data received"}), 400
    
    # get sequences
    sequences = data.get('sequences')
    if sequences is None:
        return jsonify({"error": "sequences are missing"}), 400
    
    
    # intialize sequence 1
    seq1 = sequences[0]
    seq1 = seq1.upper()
    # initialize sequence 2
    seq2 = sequences[1]
    seq2 = seq2.upper()

    print("seq1: ", seq1)
    print("seq2: ", seq2)

    gap_penalty = -2

    # check if sequences are valid
    valid_letters = {'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'}
    valid_set = set(valid_letters)

    for char in seq1:
        if char not in valid_set:
            return jsonify({"error": "Sequence 1 contains invalid characters"})
    
    for char in seq2:
        if char not in valid_set:
            return jsonify({"error": "Sequence 2 contains invalid characters"})
    


    #calculate alignment

    gap_penalty = -1

    # initialize score_matrix
    score_matrix = np.zeros((len(seq1), len(seq2)))
    print("score_matrix: ", score_matrix, "\n")

    alignment_matrix = calculate_aligment_matrix(seq1, seq2, gap_penalty, score_matrix)
    seq1_align, seq2_align, tot_score = find_alignment(seq1, seq2, gap_penalty, alignment_matrix, score_matrix)
    
    print(seq1_align)
    print(seq2_align)
    print(tot_score)



    # return sequences to frontend

    return jsonify({"sequence_1": seq1_align, "sequence_2": seq2_align, "score": tot_score})
    
    


    

# might need to debug this later
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)  
    