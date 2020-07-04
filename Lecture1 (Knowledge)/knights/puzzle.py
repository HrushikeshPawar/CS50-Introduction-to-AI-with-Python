from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# symbols
symbols = [[AKnight, AKnave], [BKnight, BKnave], [CKnight, CKnave]]

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
Or(AKnight, AKnave),                            #A is Knight or Knave
Implication(AKnight, And(AKnight, AKnave)),     #If A is Knight then statement is True
Implication(AKnave, Not(And(AKnight, AKnave)))  #If A is Knave then statement is False
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
Or(AKnight, AKnave),                            #A is Knight or Knave
Or(BKnight, BKnave),                            #B is Knight or Knave
Implication(AKnave, Not(And(AKnave, BKnave))),  #If A is Knave then statement is False
Implication(AKnight, And(AKnave, BKnave))       #If A is Knight then statement is True
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
Or(AKnight, AKnave),                            #A is Knight or Knave
Or(BKnight, BKnave),                            #B is Knight or Knave
Implication(AKnave, Not(And(AKnave, BKnave))),  #If A is Knave then statement is False
Implication(AKnight, And(AKnight, BKnight)),    #If A is Knight then statement is True
Implication(BKnave, Not(And(AKnight, BKnave))), #If B is Knave then statement is False
Implication(BKnight, And(BKnight, AKnave))      #If B is Knight then statement is True
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
Or(AKnight, AKnave),                            #A is Knight or Knave
Or(BKnight, BKnave),                            #B is Knight or Knave
Or(CKnight, CKnave),                            #C is Knight or Knave
Implication(AKnight, Or(AKnight, AKnave)),      #If A is Knight then statement is True
Implication(AKnave, Not(Or(AKnight, AKnave))),  #If A is Knave then statement is False
Implication(BKnight, And(AKnave, CKnave)),      #If B is Knight then statements are True
Implication(BKnave, Not(And(AKnave, CKnave))),  #If B is Knave then statements are False
Implication(CKnight, AKnight),                  #If C is Knight the statement is True
Implication(CKnave, Not(AKnight))               #If C is Knave the statement is False
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
