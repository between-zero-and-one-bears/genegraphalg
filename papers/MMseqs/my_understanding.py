### my reconstruction of their algorithm follows


## module (i): prefilter

# get background similarity & stdev for z-scores later; probably acquired some other exact way. doesn't matter rn
background_similarity = []
for sample in random_samples_of_data():
    background_similarity.append(internal_similarity(sample))
background_similarity, background_similarity_stdev = mean_and_stdev(background_similarity)


precalculated_index_table_of_matching_targets_per_modified_kmer = {modified_kmer: [target1, target7, target93, ...], ...:[...], }
for query in queries:
    similarities_to_calculate = {}
    for kmer in query:
        similar_kmers = somehowgeneratesimilarsequences(kmer)
        for (similar_kmer, similarity_score_to_original_kmer) in similar_kmers:
            for matching_sequence in precalculated_index_table_of_matching_targets_per_modified_kmer[similar_kmer]:
                similarities_to_calculate[matching_sequence] += similarity_score_to_original_kmer
    for sequence in similarities_to_calculate.keys():
        similarities_to_calculate[sequence] -= background_similarity
        similarities_to_calculate[sequence] /= background_similarity_stdev

## module (ii): alignment
# yeah man i don't get how this works
## module (iii): clustering
    