class Sentence:
    """Base class representing a logical sentence."""
    
    def evaluate(self, model):
        raise NotImplementedError("Subclasses must implement evaluate()")


class Symbol(Sentence):
    """Represents a propositional variable (e.g., 'P', 'Q')."""
    
    def __init__(self, name):
        self.name = name

    def evaluate(self, model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise ValueError(f"No truth value assigned to symbol {self.name}")


class Not(Sentence):
    """Represents a logical NOT (Negation)."""
    
    def __init__(self, operand):
        self.operand = operand

    def evaluate(self, model):
        return not self.operand.evaluate(model)


class And(Sentence):
    """Represents a logical AND (Conjunction)."""
    
    def __init__(self, *operands):
        self.operands = operands

    def evaluate(self, model):
        return all(op.evaluate(model) for op in self.operands)


class Or(Sentence):
    """Represents a logical OR (Disjunction)."""
    
    def __init__(self, *operands):
        self.operands = operands

    def evaluate(self, model):
        return any(op.evaluate(model) for op in self.operands)


class Implication(Sentence):
    """Represents a logical IMPLICATION (P => Q)."""
    
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model):
        # P => Q is logically equivalent to (not P) or Q
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)


# --- Your Exact Requested Recursive Model Checker ---

def check_all(knowledge, query, symbols, model):
    """
    Recursively checks all truth assignments for the symbols.
    
    If model has an assignment for each symbol (The logic below might be a little 
    confusing: we start with a list of symbols. The function is recursive, and 
    every time it calls itself it pops one symbol from the symbols list and 
    generates models from it. Thus, when the symbols list is empty, we know 
    that we finished generating models with every possible truth assignment of symbols.)
    """
    if not symbols:
        # If knowledge base is true in model, then query must also be true
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:
        # Choose one of the remaining unused symbols
        remaining = symbols.copy()
        p = remaining.pop()
        
        # Create a model where the symbol is true
        model_true = model.copy()
        model_true[p] = True
        
        # Create a model where the symbol is false
        model_false = model.copy()
        model_false[p] = False
        
        # Ensure entailment holds in both models
        return (check_all(knowledge, query, remaining, model_true) and 
                check_all(knowledge, query, remaining, model_false))


def tt_entails(knowledge, query, symbols):
    """Wrapper function to initialize the recursive model check with an empty model."""
    return check_all(knowledge, query, symbols, {})


# --- Verification & Example Execution ---

if __name__ == "__main__":
    # Define our atomic symbols
    P = Symbol("P")
    Q = Symbol("Q")
    R = Symbol("R")

    # 1. Define Knowledge Base (KB)
    # Scenario: "If it is Tuesday (P) and not raining (not Q), Harry runs (R)"
    # AND "It is Tuesday (P)" AND "It is not raining (not Q)"
    kb = And(
        Implication(And(P, Not(Q)), R),
        P,
        Not(Q)
    )

    # 2. Define our Query
    query = R

    # 3. Provide the list of unique symbol names used
    symbols_list = ["P", "Q", "R"]

    # Run the model checker
    entails = tt_entails(kb, query, symbols_list)
    print(f"Does the KB logically entail the query? {entails}")
