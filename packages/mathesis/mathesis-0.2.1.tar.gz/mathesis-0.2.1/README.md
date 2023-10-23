# Mathesis

[![PyPI](https://img.shields.io/pypi/v/mathesis.svg)](https://pypi.org/project/mathesis/)
[![Documentation Status](https://readthedocs.org/projects/mathesis/badge/?version=latest)](http://mathesis.readthedocs.io/en/latest/?badge=latest)
<!-- [![PyPI downloads](https://img.shields.io/pypi/dm/mathesis.svg)](https://pypistats.org/packages/mathesis) -->

[Mathesis](//github.com/ozekik/mathesis) is a Python library for computational formal logic, semantics, and theorem proving.
It is suitable for, for example:

- Students who learn logic and teachers who teach logic
- Researchers in logic, philosophy, linguistics, computer science, and any other areas

**Documentation:** <https://mathesis.readthedocs.io/>

## Key features

- Interactive theorem proving for humans (proof assistant)
- Automated theorem proving (automated reasoning)
- Define models and check validity of inferences in the models
- JupyterLab/Jupyter Notebook support
- Output formulas/proofs in LaTeX
- Customizable ASCII/Unicode syntax (like `A -> B`, `A → B`, `A ⊃ B`)

## Installation

```bash
pip install mathesis
```

## Supported logics

### Propositional logics

- **Classical propositional logic**
    - [x] Tableaux, Sequent calculi
    - [x] Truth tables
- **Many-valued logics**
    - [x] Truth tables
- **Modal logics**
- **Intuitionistic logic**
- **Fuzzy logics**
- **Substructural logics**

### Quantified logics (first-order or predicate logics)

- **Classical first-order logic**
- **Many-valued logics**
- **Modal logics**
- **Intuitionistic logic**
- **Fuzzy logics**
- **Substructural logics**
- **Higher-order logics**

## Development status

### Proof theories

- **Tableaux** (semantic tableaux, analytic tableaux)
    * [x] Unsigned tableaux
    * [x] Signed tableaux
- **Hilbert systems**
    * [ ] Hilbert systems
- **Natural deduction**
    * [ ] Gentzen-style natural deduction
    * [ ] Fitch-style natural deduction
- **Sequent calculi** (Gentzen-style sequent calculi)
    - [x] Two-sided sequent calculi
    - [ ] Hilbert systems in sequent calculi
    - [ ] Natural deduction in sequent calculi

### Semantics

- [x] Truth tables
- [x] Set-theoretic models
- [ ] Possible world semantics (Kripke semantics)
- [ ] Algebraic semantics
- [ ] Game-theoretic semantics
- [ ] Category-theoretic semantics

## Internals

- Parsing with [lark](https://github.com/lark-parser/lark)
- Trees with [anytree](https://github.com/c0fec0de/anytree)

## Todos

- [ ] Hilbert systems
- [ ] Natural deduction
- [ ] Boolean algebra
- [ ] Type theory
- [ ] Metatheorems
