import pandas as pd

class Correlation:

    @staticmethod
    def compute_matrix(data):
        return data.corr()

    @staticmethod
    def find_pairs(corr_matrix, threshold=0.8):

        pairs = []

        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):

                if corr_matrix.iloc[i,j] > threshold:

                    pairs.append(
                        (
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            corr_matrix.iloc[i,j]
                        )
                    )

        return pairs
