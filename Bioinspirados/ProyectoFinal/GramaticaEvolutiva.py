
"""
    <network> |= [<hiddenNeurons>][<outputNeurons>]
    <hiddenNeurons> |= <hiddenNeuron> | <hiddenNeruon>_<hiddenNeruons>
    <hiddenNeruon> |= <func> : <weight> @i0, <inputs>#<outputs>
    <outputNeurons> |= <func>: <weight> @i0_.._<func>:<weight>@i0)
    <func> |= LS | HT | SN | GS | LN | HL | LR
    <inputs> |= <input> | <input> , <inputs>
    <outputs> |= <output> | <output>, <outputs>
    <inputs> |= <weight> @ <inputID>
    <output> |= <weight> @ <outputID>
    <inputID> |= i1 | .. | iN
    <outputID> |= o1 |.. | oM
    <weight> |= <sign> <digitList>.<digitList>
    <sing> |= + | -
    <digitList> |= <digit> | <digit> <digitList>
    <digit> |= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
"""



class GramaticaEvo():
    def __init__(self, log)->None:
        self.log = log
        self.log.info("Initialized GramaticaEvo")
    
    def performMappingProcess(self):
        self.log.info("Performing mapping process")
        pass