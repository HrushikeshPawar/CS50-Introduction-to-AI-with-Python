import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    one_gene = {"Harry"}
    two_genes = {"James"}
    have_trait = {"James"}

    #Define a list to store all family probabilities
    fam_prob = list()

    #Probabilities of getting genes from parents
    def parents_gene(n):
        mom = people[person]['mother']
        dad = people[person]['father']
        mut = PROBS["mutation"]

        if ((mom in two_genes) and (dad in two_genes)):
            if n == 2:
                return (1-mut)*(1-mut)
            if n == 1:
                return (1-mut)*mut*2
            if n == 0:
                return mut*mut
        if (((mom in two_genes) and (dad in one_genes)) or ((mom in one_gene) and (dad in two_genes))):
            if n == 2:
                return (1-mut)*0.5
            if n == 1:
                return (1-mut)*0.5 + 0.5*mut
            if n == 0:
                return 0.1*0.1
        if ((mom in two_genes) or (dad in two_genes)):
            if n == 2:
                return (1-mut)*mut
            if n == 1:
                return (1-mut)*(1-mut) + mut*mut
            if n == 0:
                return mut*(1-mut)
        if ((mom in one_gene) and (dad in one_gene)):
            if n == 2:
                return 0.5*0.5
            if n == 1:
                return 2*0.5*0.5
            if n == 0:
                return 0.5*0.5
        if ((mom in one_gene) or (dad in one_gene)):
            if n == 2:
                return 0.5*mut
            if n == 1:
                return 0.5*(1-mut) + 0.5*mut
            if n == 0:
                return 0.5*(1-mut)
        else:
            if n == 2:
                return mut*mut
            if n == 1:
                return (1-mut)*mut + mut*(1-mut)
            if n == 0:
                return (1-mut)*(1-mut)
    

    #Loop through all peoples in the family
    for person in people:
        
        #Let probability at start be 0 for everyone
        prob = 0

        #If person has no parents
        if (people[person]['mother'] is None):
            #Check if the person has 2 genes
            if person in two_genes and person in have_trait:
                prob = PROBS["gene"][2] * PROBS["trait"][2][True]
                
            elif person in two_genes and person not in have_trait:
                prob = PROBS["gene"][2] * PROBS["trait"][2][False]
            
            elif person in one_gene and person in have_trait:
                prob = PROBS["gene"][1] * PROBS["trait"][1][True]

            elif person in one_gene and person not in have_trait:
                prob = PROBS["gene"][1] * PROBS["trait"][1][False]

            elif person in have_trait:
                prob = PROBS["gene"][0] * PROBS["trait"][0][True]
            
            else:
                prob = PROBS["gene"][0] * PROBS["trait"][0][False]
        
        #If person has parents
        else:

            if person in two_genes and person in have_trait:
                prob = parents_gene(2) * PROBS["trait"][2][True]

            elif person in two_genes and person not in have_trait:
                prob = parents_gene(2) * PROBS["trait"][2][False]
            
            elif person in one_gene and person in have_trait:
                prob = parents_gene(1) * PROBS["trait"][1][True]

            elif person in one_gene and person not in have_trait:
                prob = parents_gene(1) * PROBS["trait"][1][False]
                
            elif person in have_trait:
                prob = parents_gene(0) * PROBS["trait"][0][True]
            
            else:
                prob = parents_gene(0) * PROBS["trait"][0][False]
    
        #Add the probability to the list
        fam_prob.append(prob)
    
   
    return math.prod(fam_prob)

        
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    #Update probabilities of each person
    for person in probabilities:

        #Update the genes probability
        if person in two_genes:
            probabilities[person]["gene"][2] = p
        
        elif person in one_gene:
            probabilities[person]["gene"][1] = p

        else:
            probabilities[person]["gene"][0] = p

        # Update the trait probability
        if person in have_trait:
            probabilities[person]["trait"] = p
        else:
            probabilities[person]["trait"] = p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
