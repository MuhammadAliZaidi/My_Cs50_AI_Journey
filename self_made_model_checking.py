class Sentence:
    def evaluate(self,model):
        raise NotImplementedError("The subclass must use evaluate()")

class Symbol(Sentence):
    def __init__(self,name):
        self.name=name
    def evaluate(self,model):
        try:
            return bool(model[self.name])
        except KeyError:
            raise ValueError(f"No value assigned to {self.name}")
            
class Not(Sentence):
    def __init__(self,operand):
        self.operand = operand
    def evaluate(self, model):
        return not self.operand.evaluate(model)
        
class And(Sentence):
    def __init__(self,*operands):
        self.operands = operands
    def evaluate(self,model):
        result=[]
        for op in self.operands:
            result.append(op.evaluate(model))
        return all(result)
        
class Or(Sentence):
    def __init__(self,*operands):
        self.operands = operands
    def evaluate(self,model):
        return any(op.evaluate(model) for op in self.operands)
        
class Implication(Sentence):
    def __init__(self,antecedent,consequent):
        self.antecedent= antecedent
        self.consequent= consequent
    def evaluate(self,model):
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)
           
# Model Checking Algorithm
def model_checking(knowledge,query,symbols,model):
    if not symbols:
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:
        remaining=symbols.copy()
        p=remaining.pop()
        
        model_true=model.copy()
        model_true[p]=True
        
        model_false=model.copy()
        model_false[p]=False
        
        return model_checking(knowledge,query,remaining,model_true) and model_checking(
            knowledge,query,remaining,model_false
            )

def entails_tt(knowledge,query,symbols):
    """Wrapper function to initialize the recursive model check with an empty model."""
    return model_checking(knowledge, query, symbols, {})

if __name__=='__main__':
    P=Symbol('P')
    Q=Symbol('Q')
    R=Symbol('R')
    # 1. Define Knowledge Base (KB)
    # Scenario: "If it is Tuesday (P) and not raining (not Q), Harry runs (R)"
    # AND "It is Tuesday (P)" AND "It is not raining (not Q)"
    knowledge=And(
        Implication(And(P,Not(Q)),R),
        P,
        Not(Q)
        )
    query=R
    symbols_list=['P','Q','R']
    entails=entails_tt(knowledge,query,symbols_list)
    print(f"Does the Kb logically entails the query? {entails}")
    
