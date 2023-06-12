# Node of a Huffman Tree
import streamlit as st
import json
class Nodes:
    def __init__(self, probability, symbol, left=None, right=None):
        # probability of the symbol
        self.probability = probability

        # the symbol
        self.symbol = symbol

        # the left node
        self.left = left

        # the right node
        self.right = right

        # the tree direction (0 or 1)
        self.code = ''




def CalculateProbability(the_data):
    the_symbols = dict()
    for item in the_data:
        if the_symbols.get(item) == None:
            the_symbols[item] = 1
        else:
            the_symbols[item] += 1
    return the_symbols



the_codes = dict()


def CalculateCodes(node, value=''):
    # a huffman code for the current node
    newValue = value + str(node.code)

    if node.left:
        CalculateCodes(node.left, newValue)
    if node.right:
        CalculateCodes(node.right, newValue)

    if not node.left and not node.right:
        the_codes[node.symbol] = newValue

    return the_codes





def OutputEncoded(the_data, coding):
    encodingOutput = []
    for element in the_data:
        encodingOutput.append(coding[element])

    the_string = ''.join([str(item) for item in encodingOutput])
    return the_string



def TotalGain(the_data, coding):
    # total bit space to store the data before compression
    beforeCompression = len(the_data) * 8
    afterCompression = 0
    the_symbols = coding.keys()
    for symbol in the_symbols:
        the_count = the_data.count(symbol)
        # calculating how many bits are required for that symbol in total
        afterCompression += the_count * len(coding[symbol])
    return beforeCompression, afterCompression


def HuffmanEncoding(the_data):
    symbolWithProbs = CalculateProbability(the_data)
    the_symbols = symbolWithProbs.keys()
    the_probabilities = symbolWithProbs.values()

    the_nodes = []

    # converting symbols and probabilities into Huffman tree nodes
    for symbol in the_symbols:
        the_nodes.append(Nodes(symbolWithProbs.get(symbol), symbol))

    while len(the_nodes) > 1:
        # sorting all the nodes in ascending order based on their probability
        the_nodes = sorted(the_nodes, key=lambda x: x.probability)

        # picking two smallest nodes
        right = the_nodes[0]
        left = the_nodes[1]

        left.code = 0
        right.code = 1

        # combining the 2 smallest nodes to create a new node
        newNode = Nodes(left.probability + right.probability, left.symbol + right.symbol, left, right)

        the_nodes.remove(left)
        the_nodes.remove(right)
        the_nodes.append(newNode)

    huffmanEncoding = CalculateCodes(the_nodes[0])
    beforeCompression, afterCompression = TotalGain(the_data, huffmanEncoding)
    encodedOutput = OutputEncoded(the_data, huffmanEncoding)
    return encodedOutput, the_nodes[0], beforeCompression, afterCompression


def HuffmanDecoding(encodedData, huffmanTree):
    treeHead = huffmanTree
    decodedOutput = []
    for x in encodedData:
        if x == '1':
            huffmanTree = huffmanTree.right
        elif x == '0':
            huffmanTree = huffmanTree.left
        try:
            if huffmanTree.left.symbol is None and huffmanTree.right.symbol is None:
                pass
        except AttributeError:
            decodedOutput.append(huffmanTree.symbol)
            huffmanTree = treeHead

    string = ''.join([str(item) for item in decodedOutput])
    return string

def main():
    st.title("Huffman Coding")

    option = st.sidebar.selectbox("Choose an option", ("Encode and Decode", "Decode Only"))

    if option == "Encode and Decode":
        the_data = st.text_input("Enter the data:", "AAAAAAABBCCCCCCDDDEEEEEEEEE")
        encoding, the_tree, beforeCompression, afterCompression = HuffmanEncoding(the_data)
        st.write("Encoded Output: ", encoding)
        st.write("Decoded Output: ", HuffmanDecoding(encoding, the_tree))
        
    elif option == "Decode Only":
        encoded_data = st.text_input("Enter the encoded data:")
        huffman_tree = st.text_input("Enter the Huffman tree (in JSON format):")
        try:
            huffman_tree = json.loads(huffman_tree)
            decoded_output = HuffmanDecoding(encoded_data, huffman_tree)
            st.write("Decoded Output: ", decoded_output)
        except json.JSONDecodeError:
            st.write("Invalid Huffman tree format. Please enter a valid JSON string.")


if __name__ == '__main__':
    main()
