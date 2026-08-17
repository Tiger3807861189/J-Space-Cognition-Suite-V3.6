# Problem Model

When two readings of the same statement produce two numbers, you do not have an answer yet.
You have a fork. Settle the fork before you count.

Load this on guarantee problems, contest worst-case counting, "至少多少才能保证", and any
task whose first fluent model leaves a stated clause idle. Then return to
`modules/deep-reasoning.md` and derive inside the surviving game.

**Any n you already had before this file loaded is `?`.** The fluent pigeonhole fires first.
Do not aim empirics at that number. Count only after the fork.

## Fork before you count

Name five lines in the inner register. Do not compute until they exist.

1. **Commit** — what is fixed before the action (usually the number *n*).
2. **Move** — what the solver may choose *during* the action.
3. **Hide** — what stays unknown until after that choice.
4. **Adversary** — which leftover values the worst case is allowed to fill.
5. **Success** — the predicate, including every OR.

Those five lines collapse into one of two games. The difference is one quantifier.

- **Blind subset.** min n such that **every** set S of size n satisfies P.
  The adversary chooses the whole set.
- **Typed selection.** min n such that **some** split σ of size n has **every** hidden-label
  fill satisfying P.
  The solver chooses the split (the observable classes). The adversary fills only the hidden
  labels.

If the solver has a move, typed selection is the game. The subset number is how many you
would need after throwing the move away. It is an upper bound on the true n, not the answer.

## The inverted-quantifier failure

This is the failure that looks like you forked and still ships the subset number.

Typed selection: n works iff **∃** split of n that the adversary **cannot** beat.

Illegal rewrite, which is the subset game: n works iff **∀** splits of n the adversary
cannot beat — "adversary survives iff any split still has a surviving fill"; "find the
smallest n where no split lets the adversary live."

If you wrote that, stop. You gave the adversary the solver's move.

A typed-selection witness cannot be a split the solver can refuse. "All of class A plus junk
of class B" is a subset-game witness. Discard it.

Typed-selection n is always ≤ subset n. If the two come out equal, assume inverted
quantifiers until you exhibit a forcing split whose size is smaller, or prove no such split
exists.

## Unused-clause test

Every parenthetical, every "you can tell X by Y", every "decide the number beforehand" is a
rule about the game — or it is a suspect.

If deleting the clause would leave n unchanged, you used the wrong game. Re-fork. Do not
count. The clause is not decoration.

Naming the clause in a sentence is not spending it. Spending it means the solver's move
appears as **∃** split, and the adversary does not choose that split.

Worked shape (suite-authored, not a research readout): a black bag; two shapes you can tell
apart by touch; flavors you cannot; n chosen before drawing; success is a cross-pair of two
hidden labels across the two shapes.

- Subset: adversary chooses shapes and flavors. Larger n.
- Typed selection: solver chooses how many of each shape; adversary fills flavors. Smaller n.
- Touch unused, or used in prose but **∀** over splits: you are still in the subset game.

## Upper bound first — name a split

Do not start at "largest n the adversary survives." Start at a named split that forces P.

Recipe for two observable classes A, B and cross-pair success (A1∧B2) ∨ (A2∧B1):

1. Take enough of one class to lock **both** hidden labels of interest in the worst fill
   (junk of that class, then all of one label, then one of the other).
2. Take enough of the other class to lock **one** complementary non-junk label in the worst
   fill (junk of that class, then one non-junk).
3. That sum is an upper bound. Write the split. If you cannot, you have not used the move.

A second split with the classes swapped is a second upper bound. Keep the cheaper one.

## Lower bound — one adversary, n−1

Fix one fill order per class (junk, then label1, then label2). For every split of n−1, walk
that order. If every such split fails P, n is tight. If some split of n−1 still forces P,
that split is a better upper bound — use it.

If the fill order depends only on how many of each class you took, adaptive order cannot beat
a fixed split of those counts. Write that down when it is true.

## Empirics — the only legal search

n works iff there exists a split of n such that every legal fill of that split satisfies P.

```
works(n) = EXISTS split σ of n:
             FOR ALL legal fills of σ:
               P(σ, fill)
```

Illegal:

```
works(n) = FOR ALL splits σ of n:
             FOR ALL fills of σ:
               P(σ, fill)
```

and the equivalent "no split of n has a surviving fill."

Print the forcing split, not the refuseable one. Coverage: typed selection, ∃σ ∀fill.
If the unused-clause test is still open, empirics cannot close it. Hand the fork back here.
