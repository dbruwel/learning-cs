import numpy as np


def floyd_warshall(dist_matrix):
    """Finds the shortest path between every two points in a graph.

    Parameters
    ----------
    dist_matrix : np.ndarray
        The distance matrix of the graph

    Returns
    -------
    tuple[np.ndarray, dict]
        The distance matrix, and the dictionary of the next best direction used to reconstruct the path.
    """
    n = len(dist_matrix)
    dist_mat = dist_matrix.copy()

    next_best = {
        i: {j: j for j in range(n) if dist_matrix[i][j] < np.inf} for i in range(n)
    }

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_mat[i][j] > dist_mat[i][k] + dist_mat[k][j]:
                    dist_mat[i][j] = dist_mat[i][k] + dist_mat[k][j]
                    next_best[i][j] = next_best[i][k]

    return dist_mat, next_best


def main():
    dist_matrix = np.array(
        [
            [0.0, 4.0, 2.0, np.inf, np.inf],
            [4.0, 0.0, np.inf, 5.0, 10.0],
            [2.0, np.inf, 0.0, np.inf, 3.0],
            [np.inf, 5.0, np.inf, 0.0, 1.0],
            [np.inf, 10.0, 3.0, 1.0, 0.0],
        ]
    )

    dist_mat, next_best = floyd_warshall(dist_matrix)
    print(dist_mat, next_best)
