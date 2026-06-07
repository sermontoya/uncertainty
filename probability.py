from itertools import combinations

PROBS = {
    "gene":     { 2: 0.01, 1: 0.03, 0: 0.96 },
    "trait":    { 2: {True: 0.65, False: 0.35},
                   1: {True: 0.56, False: 0.44},
                   0: {True: 0.01, False: 0.99} },
    "mutation": 0.01
}


def powerset(s):
    """
    Return a list of all possible subsets of set s.

    Input:
        powerset({1, 2, 3})

    Output:
        [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
    """
    if s == set():
        return [set()]
    result = []
    for r in range(len(s) + 1):
        for combination in combinations(s, r):
            result.append(set(combination))
    return result

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set one_gene has one copy of the gene, and
        * everyone in set two_genes has two copies of the gene, and
        * everyone not in one_gene or two_gene does not have the gene, and
        * everyone in set have_trait has the trait, and
        * everyone not in set` have_trait` does not have the trait.

    Input:
        people = {
            "Harry": {"name": "Harry", "mother": None, "father": None, "trait": None}
        }
        one_gene = set()
        two_genes = {"Harry"}
        have_trait = {"Harry"}

    Output:
        0.0065
    """
    probability = 1
    for person in people:
        genes = 2 if person in two_genes else 1 if person in one_gene else 0
        has_trait = person in have_trait
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        if mother is None and father is None:
            gene_probability = PROBS["gene"][genes]
        else:
            passes = []
            for parent in [mother, father]:
                parent_genes = 2 if parent in two_genes else 1 if parent in one_gene else 0
                if parent_genes == 2:
                    pass_prob = 1 - PROBS["mutation"]
                elif parent_genes == 1:
                    pass_prob = 0.5
                else:
                    pass_prob = PROBS["mutation"]
                passes.append(pass_prob)
            if genes == 2:
                gene_probability = passes[0] * passes[1]
            elif genes == 1:
                gene_probability = passes[0] * (1 - passes[1]) + (1 - passes[0]) * passes[1]
            else:
                gene_probability = (1-passes[0]) * (1-passes[1])
        probability *= gene_probability * PROBS["trait"][genes][has_trait]
    return probability

                
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to probabilities a new joint probability p.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in have_gene and have_trait, respectively.

    Input:
        probabilities = {
            "Harry": {
                "gene": {2: 0, 1: 0, 0: 0},
                "trait": {True: 0, False: 0}
            }
        }
        one_gene = {"Harry"}
        two_genes = set()
        have_trait = {"Harry"}
        p = 0.5

    Output:
        {
            "Harry": {
                "gene": {2: 0, 1: 0.5, 0: 0},
                "trait": {True: 0.5, False: 0}
            }
        }
    """          
    
    for person in probabilities:
        genes =  2 if person in two_genes else 1 if person in one_gene else 0
        has_trait = person in have_trait
        
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][has_trait] += p

def normalize(probabilities):
    """
    Update probabilities such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).

    Input:
        probabilities = {
            "Harry": {
                "gene": {2: 2, 1: 2, 0: 6},
                "trait": {True: 1, False: 3}
            }
        }

    Output:
        {
            "Harry": {
                "gene": {2: 0.2, 1: 0.2, 0: 0.6},
                "trait": {True: 0.25, False: 0.75}
            }
        }
    """
    for person in probabilities:
        for field in ["gene", "trait"]:
            total = sum(probabilities[person][field].values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total
    
    
def calculate_probabilities(people):
    """
    Calculate normalized gene and trait probability distributions for each person.

    Input:
        people = {
            "Person": {"mother": None, "father": None, "trait": None}
        }

    Output:
        {
            "Person": {
                "gene": {2: 0.01, 1: 0.03, 0: 0.96},
                "trait": {True: 0.0329, False: 0.9671}
            }
        }
    """
    
    probabilities = { person: { "gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0} }
                      for person in people }
    names = set(people)
    for have_trait in powerset(names):
        if any(
        people[person]["trait"] is not None and
        people[person]["trait"] != (person in have_trait)
        for person in names
        ):
            continue
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    normalize(probabilities)
    return probabilities
        
    
