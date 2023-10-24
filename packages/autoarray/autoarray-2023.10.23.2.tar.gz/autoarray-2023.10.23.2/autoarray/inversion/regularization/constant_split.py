from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from autoarray.inversion.linear_obj.linear_obj import LinearObj

from autoarray.inversion.regularization.constant import Constant

from autoarray.inversion.regularization import regularization_util


class ConstantSplit(Constant):
    def __init__(self, coefficient: float = 1.0):
        """
        A constant regularization scheme which splits every source pixel into a cross of four regularization points
        (regularization is described in the `Regularization` class above) and interpolates to these points in order
        to apply smoothing on the solution of an `Inversion`.

        The size of this cross is determined via the size of the source-pixel, for example if the source pixel is a
        Voronoi pixel the area of the pixel is computed and the distance of each point of the cross is given by
        the area times 0.5.

        For this regularization scheme, there is only 1 regularization coefficient that is applied to
        all neighboring pixels. This means that the matrix B only needs to regularize pixels in one direction
        (e.g. pixel 0 regularizes pixel 1, but NOT visa versa). For example:

        B = [-1, 1]  [0->1]
            [0, -1]  1 does not regularization with 0

        Note that for this scheme the indexes of entries in the regularization matrix are not the source pixel indexes
        but the indexes of each source pixel index cross.

        A small numerical value of 1.0e-8 is added to all elements in constant regularization matrix, to ensure that
        it is positive definite.

        Parameters
        ----------
        coefficient
            The regularization coefficient which controls the degree of smooth of the inversion reconstruction.
        """

        super().__init__(coefficient=coefficient)

    def regularization_matrix_from(self, linear_obj: LinearObj) -> np.ndarray:
        """
        Returns the regularization matrix of this regularization scheme.

        Parameters
        ----------
        linear_obj
            The linear object (e.g. a ``Mapper``) which uses this matrix to perform regularization.

        Returns
        -------
        The regularization matrix.
        """
        pix_sub_weights_split_cross = linear_obj.pix_sub_weights_split_cross

        (
            splitted_mappings,
            splitted_sizes,
            splitted_weights,
        ) = regularization_util.reg_split_from(
            splitted_mappings=pix_sub_weights_split_cross.mappings,
            splitted_sizes=pix_sub_weights_split_cross.sizes,
            splitted_weights=pix_sub_weights_split_cross.weights,
        )

        pixels = int(len(splitted_mappings) / 4)
        regularization_weights = np.full(fill_value=self.coefficient, shape=(pixels,))

        return regularization_util.pixel_splitted_regularization_matrix_from(
            regularization_weights=regularization_weights,
            splitted_mappings=splitted_mappings,
            splitted_sizes=splitted_sizes,
            splitted_weights=splitted_weights,
        )
