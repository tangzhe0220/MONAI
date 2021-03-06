# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import skimage
from parameterized import parameterized

from monai.transforms import Resized
from tests.utils import NumpyImageTestCase2D


class TestResized(NumpyImageTestCase2D):
    @parameterized.expand([("invalid_order", "order", AssertionError)])
    def test_invalid_inputs(self, _, order, raises):
        with self.assertRaises(raises):
            resize = Resized(keys="img", spatial_size=(128, 128, 3), order=order)
            resize({"img": self.imt[0]})

    @parameterized.expand(
        [
            ((64, 64), 1, "reflect", 0, True, True, True, None),
            ((32, 32), 2, "constant", 3, False, False, False, None),
            ((256, 256), 3, "constant", 3, False, False, False, None),
        ]
    )
    def test_correct_results(
        self, spatial_size, order, mode, cval, clip, preserve_range, anti_aliasing, anti_aliasing_sigma
    ):
        resize = Resized(
            "img", spatial_size, order, mode, cval, clip, preserve_range, anti_aliasing, anti_aliasing_sigma
        )
        expected = list()
        for channel in self.imt[0]:
            expected.append(
                skimage.transform.resize(
                    channel,
                    spatial_size,
                    order=order,
                    mode=mode,
                    cval=cval,
                    clip=clip,
                    preserve_range=preserve_range,
                    anti_aliasing=anti_aliasing,
                    anti_aliasing_sigma=anti_aliasing_sigma,
                )
            )
        expected = np.stack(expected).astype(np.float32)
        self.assertTrue(np.allclose(resize({"img": self.imt[0]})["img"], expected))


if __name__ == "__main__":
    unittest.main()
