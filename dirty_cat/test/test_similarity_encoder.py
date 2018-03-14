import numpy as np
import Levenshtein as lev
from jellyfish import jaro_distance

from dirty_cat import similarity_encoder, target_encoder


def test_similarity_encoder():
    X = np.array(['aa', 'aaa', 'aaab']).reshape(-1, 1)
    X_test = np.array([['aa', 'aaa', 'aaa', 'aaab', 'aaac']]).reshape(-1, 1)

    similarity_types = [
        'levenshtein-ratio',
        'jaro-winkler'
        ]

    for similarity_type in similarity_types:
        model = similarity_encoder.SimilarityEncoder(
            similarity_type=similarity_type, handle_unknown='ignore')

        encoder = model.fit(X).transform(X_test)

        if similarity_type == 'levenshtein-ratio':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = lev.ratio(x_t, x)
            assert np.array_equal(encoder, ans)

        if similarity_type == 'jaro-winkler':
            ans = np.zeros((len(X_test), len(X)))
            for i, x_t in enumerate(X_test.reshape(-1)):
                for j, x in enumerate(X.reshape(-1)):
                    ans[i, j] = jaro_distance(x_t, x)
            assert np.array_equal(encoder, ans - 1)