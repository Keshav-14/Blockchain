import blockchain as bl
from flask import Flask, jsonify

# Creating the Web App
app = Flask(__name__)

# Creating the Blockchain
blockchain_object = bl.Blockchain()

# Mining a New Block
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    
    '''
    * Function for mining the Block 
    * 1st find the proof of work for the current block
    * then create the block and add it to the chain
    * here this function return the actually mined block in json format and a http success code 
    * this is just for ui interaction
    '''
    
    previous_block = blockchain_object.getPreviousBlock()
    previous_proof = previous_block['proof']
    proof = blockchain_object.proofOfWork(previous_proof)
    previous_hash = blockchain_object.hash(previous_block)
    mined_block = blockchain_object.createBlock(proof, previous_hash)
    response = {
        'message' : 'Congratulations, You just mined a block!',
        'index' : mined_block['index'],
        'timestamp' : mined_block['timeStamp'],
        'proof' : mined_block['proof'],
        'previousHash' : mined_block['previousHash'],
    }
    
    return jsonify(response), 200 #(HTTP success code)
    
# Getting the Full Blockchain to display in the postman User Interface
@app.route('/getChain', methods=['GET'])
def getChain():
    response = {
        'Chain' : blockchain_object.chain,
        'Length of Chain' :  len(blockchain_object.chain)
    }
    return jsonify(response), 200

# Checking whether the chain is valid or not!
@app.route('/isValid', methods=['GET'])
def isValid():
    is_valid = blockchain_object.isChainValid(blockchain_object.chain)
    response = {}
    if is_valid:
        response['message'] = "The BlockChain is Valid!"
    else:
        response['message'] = "The Blockchain is Not Valid"
    return jsonify(response), 200

# Running the App
app.run(host='0.0.0.0', port=5000)
