"""Module for loading the dataset from csv files."""
import os
import pandas as pd
import numpy as np

from .Dataset import Dataset


class DatasetCSV(Dataset):
    """Dataset composed by data matrix and labels vector.

    Matrices are stored in two CSV files.
    """

    def load_dataset(self, base_path):
        r"""Read data matrix and labels vector from files.

        Parameters
        ----------

        base_path : string
            The base path relative to which files are stored.

        Returns
        -------

        data : ndarray
            The :math:`n \\times p` data matrix .

        labels : ndarray
            The :math:`n`-dimensional vector containing labels.

        feature_names : list
            The list containing the names of the features

        """
        data_path = os.path.join(base_path, self.get_file('data'))
        labels_path = os.path.join(base_path, self.get_file('labels'))

        ##################
        # DATA
        ##################
        poslab = self._dataset_options.pop('positive_label', None)
        samples_on = self._dataset_options.pop('samples_on', 'col')
        pd_data = pd.read_csv(data_path, **self._dataset_options)

        if samples_on == 'col':
            print(pd_data)
            pd_data = pd_data.transpose()

        # Retrieve feature names from the column names of the DataFrame
        feature_names = pd_data.columns

        # if not self.get_option('data_preprocessing') is None:
        # ### TODO Check!!!
        #     # if rank == 0:
        #         # print("Preprocessing data...")
        #
        #     self.get_option('data_preprocessing').load_data(pd_data)
        #     pd_data = self.get_option('data_preprocessing').process()

        ##################
        # LABELS
        ##################
        # For labels, remove parameters that were likely specified for data
        # only.
        self._dataset_options.pop('usecols', None)
        pd_labels = pd.read_csv(labels_path, **self._dataset_options)

        if poslab is None:
            uv = np.sort(np.unique(pd_labels.values))
            if len(uv) != 2:
                raise Exception("More than two unique values in the labels "
                                "array.")
            poslab = uv[0]

        # Auxiliary function required to convert the labels to
        # -1/+1
        def _to_plus_minus(x):
            """Convert values in the labels."""
            return +1. if x == poslab else -1.

        # Convert labels to -1/+1
        pd_labels_mapped = pd_labels.applymap(_to_plus_minus)

        data = pd_data.as_matrix()
        labels = pd_labels_mapped.as_matrix().ravel()

        print(feature_names)

        return data, labels, feature_names
