# vim: set encoding=utf-8

#  Copyright (c) 2016 Intel Corporation 
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

""" Tests label propagation, community detetction by association"""
import unittest

from sparktkregtests.lib import sparktk_test


class LbpGraphx(sparktk_test.SparkTKTestCase):

    def test_label_propagation(self):
        """label propagation on plus sign, deterministic, not conververgent"""
        vertex_frame = self.context.frame.create(
                          [["vertex1"],
                           ["vertex2"],
                           ["vertex3"],
                           ["vertex4"],
                           ["vertex5"]],
                          [("id", str)])
        edge_frame = self.context.frame.create(
                          [["vertex2", "vertex3"],
                           ["vertex2", "vertex1"],
                           ["vertex2", "vertex4"],
                           ["vertex2", "vertex5"]],
                          [("src", str), ("dst", str)])

        graph = self.context.graph.create(vertex_frame, edge_frame)
        baseline = { 4: [u'vertex4', u'vertex5', u'vertex1', u'vertex3'],
                     1: [u'vertex2']}


        community = graph.label_propagation(3)
        communities = community.to_pandas(5).groupby("label")

        self.assertEqual(2, len(communities))
        for (label, group) in communities:
            group_vals = list(group['id'])
            self.assertItemsEqual(group_vals, baseline[len(group_vals)])

        community = graph.label_propagation(11)
        communities = community.to_pandas(5).groupby("label")

        self.assertEqual(2, len(communities))
        for (label, group) in communities:
            group_vals = list(group['id'])
            self.assertItemsEqual(group_vals, baseline[len(group_vals)])


if __name__ == '__main__':
    unittest.main()
