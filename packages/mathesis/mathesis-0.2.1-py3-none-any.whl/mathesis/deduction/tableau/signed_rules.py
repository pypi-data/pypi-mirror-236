from anytree import Node
from itertools import count

from mathesis import forms
from mathesis.deduction.tableau import sign


class Rule:
    pass


class PositiveNegationRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        assert target.sign == sign.POSITIVE
        subfml = target.fml.sub
        node = Node(
            str(subfml), sign=sign.NEGATIVE, fml=subfml, parent=tip, n=next(counter)
        )
        return {
            "queue_items": [[node]],
            "counter": counter,
        }


class NegativeNegationRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        assert target.sign == sign.NEGATIVE
        subfml = target.fml.sub
        node = Node(
            str(subfml), sign=sign.POSITIVE, fml=subfml, parent=tip, n=next(counter)
        )
        return {
            "queue_items": [[node]],
            "counter": counter,
        }


class NegationRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        if target.sign == sign.POSITIVE:
            return PositiveNegationRule().apply(target, tip, counter=counter)
        elif target.sign == sign.NEGATIVE:
            return NegativeNegationRule().apply(target, tip, counter=counter)


class ConjunctionRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        conj1, conj2 = target.fml.subs
        node1 = Node(
            str(conj1), sign=target.sign, fml=conj1, parent=tip, n=next(counter)
        )
        node2 = Node(
            str(conj2), sign=target.sign, fml=conj2, parent=node1, n=next(counter)
        )
        return {
            "queue_items": [node1, node2],
        }


class NegatedConjunctionRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        conj1, conj2 = target.fml.sub.subs
        nconj1, nconj2 = map(lambda v: forms.Negation(v), [conj1, conj2])
        nodeL = Node(
            str(nconj1), sign=target.sign, fml=nconj1, parent=tip, n=next(counter)
        )
        nodeR = Node(
            str(nconj2), sign=target.sign, fml=nconj2, parent=tip, n=next(counter)
        )
        return {
            "queue_items": [nodeL, nodeR],
            "counter": counter,
        }


class PositiveDisjunctionRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        disj1, disj2 = target.fml.subs
        nodeL = Node(
            str(disj1), sign=target.sign, fml=disj1, parent=tip, n=next(counter)
        )
        nodeR = Node(
            str(disj2), sign=target.sign, fml=disj2, parent=tip, n=next(counter)
        )
        return {
            "queue_items": [[nodeL], [nodeR]],
            "counter": counter,
        }


class NegativeDisjunctionRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        disj1, disj2 = target.fml.sub.subs
        ndisj1, ndisj2 = map(lambda v: forms.Negation(v), [disj1, disj2])
        node1 = Node(
            str(ndisj1), sign=target.sign, fml=ndisj1, parent=tip, n=next(counter)
        )
        node2 = Node(
            str(ndisj2), sign=target.sign, fml=ndisj2, parent=node1, n=next(counter)
        )
        return {
            "queue_items": [[node1, node2]],
            "counter": counter,
        }


class DisjunctionRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        if target.sign == sign.POSITIVE:
            return PositiveDisjunctionRule().apply(target, tip, counter=counter)
        elif target.sign == sign.NEGATIVE:
            return NegativeDisjunctionRule().apply(target, tip, counter=counter)


class PositiveConditionalRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        assert target.sign == sign.POSITIVE
        antec, desc = target.fml.subs
        nodeL = Node(
            str(antec), sign=sign.NEGATIVE, fml=antec, parent=tip, n=next(counter)
        )
        nodeR = Node(
            str(desc), sign=sign.POSITIVE, fml=desc, parent=tip, n=next(counter)
        )
        return {
            "queue_items": [[nodeL], [nodeR]],
            "counter": counter,
        }


class NegativeConditionalRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        assert target.sign == sign.NEGATIVE
        antec, desc = target.fml.subs
        node1 = Node(
            str(antec), sign=sign.POSITIVE, fml=antec, parent=tip, n=next(counter)
        )
        node2 = Node(
            str(desc), sign=sign.NEGATIVE, fml=desc, parent=node1, n=next(counter)
        )
        return {
            "queue_items": [[node1, node2]],
            "counter": counter,
        }


class ConditionalRule(Rule):
    def apply(self, target, tip, counter=count(1)):
        if target.sign == sign.POSITIVE:
            return PositiveConditionalRule().apply(target, tip, counter=counter)
        elif target.sign == sign.NEGATIVE:
            return NegativeConditionalRule().apply(target, tip, counter=counter)
