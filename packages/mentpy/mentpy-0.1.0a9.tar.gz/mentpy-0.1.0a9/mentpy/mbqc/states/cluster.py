# Copyright (C) [2023] Luis Mantilla
#
# This program is released under the GNU GPL v3.0 or later.
# See <https://www.gnu.org/licenses/> for details.

# TODO: Add AKLT state class inheritance from graph state
import networkx as nx


class ClusterState(nx.Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError
