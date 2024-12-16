import React, { useState }  from 'react'
import './addSequence.css'
import { Navigate, useNavigate } from 'react-router-dom';




export const AddSequence= ()=> {

    //const navigate = useNavigate();

    // initialize sequences and error message
    const [sequence1, setSequence1] = useState('')
    const [sequence2, setSequence2] = useState('')
    const [error1, setError] = useState('')
    const [alignmentResults, setAlignmentResults] = useState({ seq1_align: '', seq2_align: ''})
    const [score, setScore] = useState('')

    

    // event handler functions for sequence submissions
    const handleSequence1Change = (event) => setSequence1(event.target.value)
    const handleSequence2Change = (event) => setSequence2(event.target.value)

    
    // clears sequence entries
    const handleClear = () => {
        setSequence1('')
        setSequence2('')
        setError('')
        setScore('')
        setAlignmentResults({ seq1_align: '', seq2_align: ''})
    }


    // handle submission
    const handleSubmit=(event)=> { 
        event.preventDefault();

        console.log('Sequence 1: ', sequence1)
        console.log('Sequence 2: ', sequence2)


        // send sequences to backend for N-W algorithm
        fetch('http://127.0.0.1:4000/calculate_alignment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sequences: [sequence1, sequence2] })
        })
        .then(response => {
            if (response.ok) {
                setError('')
            }
            return response.json()
        })
        .then(data => {
            if (data.error) {
                setError(data.error)
            }
            else {
                console.log('Sequences recieved', data)
                //initialize results here
                setError('')
                setAlignmentResults({ seq1_align: data.sequence_1, seq2_align: data.sequence_2 })
                setScore(data.score)
                console.log('results: ', alignmentResults.seq1_align, alignmentResults.seq2_align)
                console.log('score: ', data.score)
            }
        })
        .catch(error => {
            console.error('error');
            setError(error.message)
        })

    }



    return (
        <div className='sequences'>
            <h1>Global Sequence Alignment Calculator</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Sequence 1:</label>
                    <input required value={sequence1} onChange={handleSequence1Change}></input>
                </div>
                <div className="form-group">
                    <label>Sequence 2:</label>
                    <input required value={sequence2} onChange={handleSequence2Change}></input>
                </div>
                <div className="form-group">
                    <button type="button" onClick={handleClear}> Clear form </button>
                    <button type="submit"> Calculate alignment</button>
                    <button type="button"> Store alignment</button>
                    <button type="button"> View stored alignments</button>
                </div>
            </form>
            {error1 && <div className='error_message'>{error1}</div>}
            {alignmentResults.seq1_align && alignmentResults.seq2_align && score && (
                <div className='alignment_results'>
                    <p>{alignmentResults.seq1_align}</p>
                    <p>{alignmentResults.seq2_align}</p>
                    <div className='score_results'>
                        <h3>Score:</h3>
                        <p className="p2">{score}</p>
                    </div>
                </div>
            )}
        </div>
    )
    
}

export default AddSequence
