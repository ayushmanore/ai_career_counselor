class FOPLRule:
    """
    First-Order Predicate Logic Rule
    """
    
    def __init__(self, name, conditions, conclusion, confidence=1.0):
        self.name = name
        self.conditions = conditions  # List of predicates
        self.conclusion = conclusion  # Conclusion predicate
        self.confidence = confidence
    
    def __str__(self):
        return f"Rule {self.name}: {self.conditions} => {self.conclusion}"

class Predicate:
    """
    Represents a logical predicate
    """
    
    def __init__(self, name, args=None, negated=False):
        self.name = name
        self.args = args if args else []
        self.negated = negated
    
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        pred_str = f"{self.name}({args_str})" if self.args else self.name
        return f"¬{pred_str}" if self.negated else pred_str
    
    def matches(self, other):
        """Check if this predicate matches another"""
        return (self.name == other.name and 
                len(self.args) == len(other.args) and
                self.negated == other.negated)

class FOPLRuleEngine:
    """
    FOPL Rule Engine for career counseling
    """
    
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.rules = self._initialize_fopl_rules()
    
    def _initialize_fopl_rules(self):
        rules = []
        
        # Rule 1: High STEM scores suggest engineering careers
        rules.append(FOPLRule(
            name="STEM_Engineering_Rule",
            conditions=[
                Predicate("high_score", ["mathematics"]),
                Predicate("high_score", ["physics"]),
                Predicate("good_score", ["chemistry"])
            ],
            conclusion=Predicate("suitable_career", ["engineer"]),
            confidence=0.85
        ))
        
        # Rule 2: Computer Science + Math suggests Software Engineering
        rules.append(FOPLRule(
            name="CS_Software_Rule",
            conditions=[
                Predicate("high_score", ["computer_science"]),
                Predicate("high_score", ["mathematics"]),
                Predicate("personality_trait", ["logical"])
            ],
            conclusion=Predicate("suitable_career", ["software_engineer"]),
            confidence=0.9
        ))
        
        # Rule 3: Biology + Chemistry + Physics suggests Medicine
        rules.append(FOPLRule(
            name="Medical_Rule",
            conditions=[
                Predicate("high_score", ["biology"]),
                Predicate("high_score", ["chemistry"]),
                Predicate("good_score", ["physics"]),
                Predicate("personality_trait", ["caring"])
            ],
            conclusion=Predicate("suitable_career", ["doctor"]),
            confidence=0.88
        ))
        
        # Rule 4: Math + Economics suggests Data Science/Finance
        rules.append(FOPLRule(
            name="Data_Finance_Rule",
            conditions=[
                Predicate("high_score", ["mathematics"]),
                Predicate("good_score", ["economics"]),
                Predicate("personality_trait", ["analytical"])
            ],
            conclusion=Predicate("suitable_career", ["data_scientist"]),
            confidence=0.82
        ))
        
        # Rule 5: Creative subjects suggest design careers
        rules.append(FOPLRule(
            name="Creative_Design_Rule",
            conditions=[
                Predicate("high_score", ["art"]),
                Predicate("personality_trait", ["creative"]),
                Predicate("personality_trait", ["visual"])
            ],
            conclusion=Predicate("suitable_career", ["graphic_designer"]),
            confidence=0.8
        ))
        
        # Rule 6: Communication skills suggest teaching/journalism
        rules.append(FOPLRule(
            name="Communication_Rule",
            conditions=[
                Predicate("high_score", ["english"]),
                Predicate("personality_trait", ["communication"]),
                Predicate("good_score", ["history"])
            ],
            conclusion=Predicate("suitable_career", ["teacher"]),
            confidence=0.75
        ))
        
        return rules
    
    def evaluate_conditions(self, rule, facts):
        """Evaluate if all conditions of a rule are satisfied"""
        satisfied_conditions = 0
        total_conditions = len(rule.conditions)
        
        for condition in rule.conditions:
            if self._evaluate_predicate(condition, facts):
                satisfied_conditions += 1
        
        return satisfied_conditions / total_conditions if total_conditions > 0 else 0
    
    def _evaluate_predicate(self, predicate, facts):
        """Evaluate a single predicate against facts"""
        if predicate.name == "high_score":
            subject = predicate.args[0]
            score = facts.get(f"score_{subject}", 0)
            return score >= 75
        
        elif predicate.name == "good_score":
            subject = predicate.args[0]
            score = facts.get(f"score_{subject}", 0)
            return score >= 65
        
        elif predicate.name == "personality_trait":
            trait = predicate.args[0]
            return facts.get(f"trait_{trait}", False)
        
        elif predicate.name == "suitable_career":
            career = predicate.args[0]
            return facts.get(f"career_{career}", False)
        
        return False