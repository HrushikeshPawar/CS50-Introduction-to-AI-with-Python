import csv
import itertools
import sys

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

    # A function to calculate number of genes of given person
    def num_gene(person, one_gene=one_gene, two_genes=two_genes):
        if person in two_genes:
            return 2
        
        elif person in one_gene:
            return 1
        
        else:
            return 0

    # A function to calculate probability of interitence of gene
    def probability_genes(num_of_genes, is_inherited):

        # If parent has two copies gene
        if num_of_genes == 2:
            
            # Has trait
            if is_inherited:
                return 1 - PROBS["mutation"]
            
            # No trait
            else:
                return PROBS["mutation"]
        
        # If parent has only one gene then there 50/50 chance whether they pass it on
        elif num_of_genes == 1:
            return 0.5
        
        # If parent has no gene, then only to pass on the gene is through mutation
        else:
            if is_inherited:
                return PROBS["mutation"]
            else:
                return 1 - PROBS["mutation"]

    #Define a list to store all family probabilities
    fam_prob = 1

    #Loop through all peoples in the family
    for person in people:
        
        # Get number of genes in give person
        num_of_genes = num_gene(person)

        # Does the person have the trait
        has_trait = person in have_trait
        old = fam_prob

        #If person has no parents
        if (people[person]["mother"] is None) and (people[person]["father"] is None):
            
            # Use un-conditional probabilities
            fam_prob *= PROBS["gene"][num_of_genes] * PROBS["trait"][num_of_genes][has_trait]
        
        #If person has parents
        else:
            
            # Number of genes in parents
            num_of_genes_mom = num_gene(people[person]["mother"])
            num_of_genes_dad = num_gene(people[person]["father"])

            # If child has two genes then both parents have to contribute
            if num_of_genes == 2:
                fam_prob *= probability_genes(num_of_genes_mom, True) * probability_genes(num_of_genes_dad, True)
            
            # If child has one gene, then two ways to inherit, 1 mom 0 dad or vice-versa
            elif num_of_genes == 1:
                prob1 = probability_genes(num_of_genes_mom, True) * probability_genes(num_of_genes_dad, False)
                prob2 = probability_genes(num_of_genes_mom, False) * probability_genes(num_of_genes_dad, True)
                fam_prob *= (prob1 + prob2)
                #print()
                #print(num_of_genes_mom, people[person]["mother"] in have_trait, num_of_genes_dad, people[person]["father"] in have_trait, num_of_genes, has_trait, fam_prob/old)
            
            # If child has zero genes, then only one way is possible
            else:
                fam_prob *= probability_genes(num_of_genes_mom, False) * probability_genes(num_of_genes_dad, False)

            # Finally multiply with the probility of having trait
            fam_prob *= PROBS["trait"][num_of_genes][has_trait]
            
    # Return probability
    return fam_prob

        
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
            probabilities[person]["gene"][2] += p
        
        elif person in one_gene:
            probabilities[person]["gene"][1] += p

        else:
            probabilities[person]["gene"][0] += p

        # Update the trait probability
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for person in probabilities:
        const_genes = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        const_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        
        for value in probabilities[person]['gene']:
            probabilities[person]["gene"][value] /= const_genes
        
        for char in probabilities[person]['trait']:
            probabilities[person]["trait"][char] /= const_trait



if __name__ == "__main__":
    main()
