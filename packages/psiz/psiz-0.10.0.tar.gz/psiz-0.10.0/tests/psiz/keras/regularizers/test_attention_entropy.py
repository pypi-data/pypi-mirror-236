# -*- coding: utf-8 -*-
# Copyright 2021 The PsiZ Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Test constraints module."""

import tensorflow as tf

from psiz.keras.regularizers import AttentionEntropy


def test_all():
    """Test all methods."""
    # Initialize.
    rate = 0.1
    reg = AttentionEntropy(rate=rate)

    # Check get_config.
    config = reg.get_config()
    assert config["rate"] == rate

    # Check call.
    w = tf.constant([[0.5], [1.2], [1.3]])
    output = reg(w)
    tf.debugging.assert_equal(output, tf.constant(0.03425057))
