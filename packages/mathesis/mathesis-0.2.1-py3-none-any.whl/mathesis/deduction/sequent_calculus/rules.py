from itertools import count

from mathesis.deduction.tableau import signed_rules


class StructuralRule:
    pass


NegationLeft = signed_rules.PositiveNegationRule
NegationRight = signed_rules.NegativeNegationRule

ConditionalLeft = signed_rules.PositiveConditionalRule
ConditionalRight = signed_rules.NegativeConditionalRule

DisjunctionLeft = signed_rules.PositiveDisjunctionRule

class WeakeningLeft(StructuralRule):
    def apply(self, target, tips, counter=count(1)):
        target.weakened = True
        # left = [v for v in target.sequent_node.sequent[0] if v != target]
        # right = target.sequent_node.sequent[1]
        # sequent_node = Node(
        #     "{} ⇒ {}".format(
        #         ", ".join(map(lambda x: f"{x.name}", left)),
        #         ", ".join(map(lambda x: f"{x.name}", right)),
        #     ),
        #     sequent=[left, right],
        #     parent=target.sequent_node,
        # )
        return {
            "queue_items": [[]],
            "counter": counter,
        }


class WeakeningRight(StructuralRule):
    def apply(self, target, tips, counter=count(1)):
        target.weakened = True
        # target.sequent_node.sequent[1].remove(target)
        return {
            "queue_items": [[]],
            "counter": counter,
        }
