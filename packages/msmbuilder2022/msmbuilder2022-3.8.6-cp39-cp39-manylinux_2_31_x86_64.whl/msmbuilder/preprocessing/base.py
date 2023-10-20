# Author: Carlos Xavier Hernandez <cxh@stanford.edu>
# Contributors:
# Copyright (c) 2016, Stanford University and the Authors
# All rights reserved.

from __future__ import print_function, division, absolute_import
import numpy as np
import collections

try:
    from collections import Sequence
except ImportError:
    # python3.10
    from collections.abc import Sequence

from ..base import BaseEstimator
from ..utils import check_iter_of_sequences


class MultiSequencePreprocessingMixin(BaseEstimator):
    # The API for the scikit-learn preprocessing object is, in fit(), that
    # they take a single 2D array of shape (n_data_points, n_features).
    #
    # For reducing a collection of timeseries, we need to preserve
    # the structure of which data_point came from which sequence. If
    # we concatenate the sequences together, we lose that information.
    #
    # This mixin is basically a little "adaptor" that changes fit()
    # so that it accepts a list of sequences. Its implementation
    # concatenates the sequences, calls the superclass fit(), and
    # then splits the labels_ back into the sequenced form.
    #
    # This code is copied and modified from cluster.MultiSequenceClusterMixin

    def fit(self, sequences, y=None):
        """Fit Preprocessing to X.

        Parameters
        ----------
        sequences : list of array-like, each of shape [sequence_length, n_features]
            A list of multivariate timeseries. Each sequence may have
            a different length, but they all must have the same number
            of features.
        y : None
            Ignored

        Returns
        -------
        self
        """
        check_iter_of_sequences(sequences)
        s = super(MultiSequencePreprocessingMixin, self)
        s.fit(self._concat(sequences))

        return self

    def _concat(self, sequences):
        self.__lengths = [len(s) for s in sequences]

        # Indexing will fail on generic iterators
        if not isinstance(sequences, Sequence):
            sequences = list(sequences)

        if len(sequences) > 0 and isinstance(sequences[0], np.ndarray):
            concat = np.concatenate(sequences)
        else:
            # if the input sequences are not numpy arrays, we need to guess
            # how to concatenate them. this operation below works for mdtraj
            # trajectories (which is the use case that I want to be sure to
            # support), but in general the python container protocol doesn't
            # give us a generic way to make sure we merged sequences
            concat = sequences[0].join(sequences[1:])

        assert sum(self.__lengths) == len(concat)
        return concat

    def _split(self, concat):
        return [concat[cl - l: cl] for (cl, l) in
                zip(np.cumsum(self.__lengths), self.__lengths)]

    def transform(self, sequences):
        """Apply preprocessing to sequences

        Parameters
        ----------
        sequences: list of array-like, each of shape (n_samples_i, n_features)
            Sequence data to transform, where n_samples_i in the number of samples
            in sequence i and n_features is the number of features.

        Returns
        -------
        sequence_new : list of array-like, each of shape (n_samples_i, n_components)
        """
        check_iter_of_sequences(sequences)
        transforms = []
        for X in sequences:
            transforms.append(self.partial_transform(X))
        return transforms

    def fit_transform(self, sequences, y=None):
        """Fit the model and apply preprocessing

        Parameters
        ----------
        sequences: list of array-like, each of shape (n_samples_i, n_features)
            Training data, where n_samples_i in the number of samples
            in sequence i and n_features is the number of features.
        y : None
            Ignored

        Returns
        -------
        sequence_new : list of array-like, each of shape (n_samples_i, n_components)
        """
        self.fit(sequences)
        transforms = self.transform(sequences)

        return transforms

    def partial_transform(self, sequence):
        """Apply preprocessing to single sequence

        Parameters
        ----------
        sequence: array like, shape (n_samples, n_features)
            A single sequence to transform

        Returns
        -------
        out : array like, shape (n_samples, n_features)
        """
        s = super(MultiSequencePreprocessingMixin, self)
        return s.transform(sequence)

    def partial_fit(self, sequence, y=None):
        """Fit Preprocessing to X.
        Parameters
        ----------
        sequence : array-like, [sequence_length, n_features]
            A multivariate timeseries.
        y : None
            Ignored
        Returns
        -------
        self
        """
        s = super(MultiSequencePreprocessingMixin, self)
        if hasattr(s, 'fit'):
            return s.fit(sequence)
        return self

    def fit(self, X, y=None):
        """Fit Preprocessing to X.

        Parameters
        ----------
        sequence : array-like, [sequence_length, n_features]
            A multivariate timeseries.
        y : None
            Ignored

        Returns
        -------
        self
        """
        return self.partial_fit(np.concatenate(X, axis=0))


class MultiSequenceOnlinePreprocessingMixin(MultiSequencePreprocessingMixin):

        def fit(self, sequences, y=None):
            """Fit Preprocessing to X.

            Parameters
            ----------
            sequences : list of array-like, each of shape [sequence_length, n_features]
                A list of multivariate timeseries. Each sequence may have
                a different length, but they all must have the same number
                of features.
            y : None
                Ignored

            Returns
            -------
            self
            """
            check_iter_of_sequences(sequences)
            for sequence in sequences:
                s = super(MultiSequencePreprocessingMixin, self)
                s.partial_fit(sequence)

            return self
