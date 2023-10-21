# A workflow for determining statistically significant sub sampling from the null distribution of a design space
# 
# 1. Given a candidate "pattern", the search graph, and a set of successful terminal nodes, compute 
#     the number of successful assembly paths w/w/o that pattern
#       - Initialize two counters (successes_with_pattern, successes_without_pattern)
#       - For every successful terminal node
#           - Count the number of paths between the root and the terminal node 
#               - it may be possible to derive this number analytically - that would have to take symmetry into account
#               - This may generate paths that were not traversed during the search
#               - this takes into account the inherent bias of assembly-based sampling!
#           - If it has the motif, add the number to the with_pattern counter, else add to without_pattern
#       - Compute n_paths = successes_with_pattern + successes_without_pattern
# 2. Using the same grammar and root node, sample from the reference distribution of assembly paths
#       - Initialize the same counters (random_with_pattern, random_without_pattern)
#       - For n_paths iterations:
#           - choose random actions until a terminal node is reached
#           - Compute if it has the motif and add to the appropriate counter
#               - (If this becomes prohibitively expensive, cache path intermediates and use dynamic programming)
# 
# 3. Now we ask the question:
# 
#       Does this pattern occur more frequently in the successful circuits found 
#       during the search than in circuits found by random assembly?
# 
#    Perform a chi-squared (if all > 5) or Barnard's exact test (or Boschloo??) on the contingency table:
#
#                     |  All possible successful   |  Randomly chosen 
#                     |  assembly paths            |  assembly paths
#   ---------------------------------------------------------------------
#      Has pattern    |                            |  
#   ---------------------------------------------------------------------
#      Lacks pattern  |                            |  
#
# 4. Report the p-value
# 

from typing import Any
import numpy as np
from .circuitree import CircuiTree, CircuitGrammar


class NullTreeSampler:
    def ___init__(
        self,
        grammar: CircuitGrammar,
        root: str,
    ):
        self.grammar = grammar

        # Supply the number of terminal nodes and samples per node

    def select_and_expand(self) -> Any:
        pass

    def is_success(self, node: Any) -> bool:
        pass

    def sample(self, n_samples: int):
        pass
