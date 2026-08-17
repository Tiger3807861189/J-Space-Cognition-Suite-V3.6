# Problem Model

When two readings of the same statement produce two different solutions, you do not have an
answer yet. You have a fork. Settle the fork before you act.

Load this whenever a stated clause might sit idle, a capability was granted, success has an
OR or an exception, two architectures both "fit", or a fluent solution arrived before this
file. Then return to `modules/deep-reasoning.md` and work inside the surviving reading.

**Any solution you already had before this file loaded is `?`.** Fluency fires first.
Confirming that solution is not a fork. Do not aim tests at it. Derive from the five lines.

## Fork before you act

Name five lines in the inner register. Do not implement, count, or patch until they exist.

1. **Commit** — what is fixed before you act (the goal, the n, the public contract).
2. **Move** — what you may choose during the work: a tool, a sandbox write, an observable
   class, an existing function, a granted permission.
3. **Hide** — what stays unknown until after that choice.
4. **World** — what fills the rest: remaining state, tests, the user, worst-case leftovers.
   This is the adversary when the task is a guarantee.
5. **Success** — the predicate, including every OR, exception, platform, and user-visible
   effect.

If the statement gave a move and your plan deletes it, you are solving a harder problem than
the one asked. The harder solution is not the answer.

**The description you accept is a Move.** Two descriptions of one object are two problems:
one where the cases collapse and one where you walk them. Taking the statement's own
description without examining it hands that choice to the world.

**Stack is a Move.** Language, package, plugin, and test runner follow this repo and the
host you actually found — not the first fluent rewrite. A parallel clone of what already
exists deletes the move: you are proving a model of it, not spending it. Follow what is
there, or fork before you write.

## Named is not spent

Every parenthetical, every "you can X", every existing tool, every granted write, every
"decide beforehand" is a rule about the game — or it is a suspect.

If deleting the clause would leave the plan unchanged, you used the wrong reading. Re-fork.
Do not act. The clause is not decoration.

Naming the clause in a sentence is not spending it. Spending it means the move appears in
the strategy: you choose it, the world does not.

## Fluent-first is not independent

The first plan that fits will form before this file. Tests of that plan will agree with it.

You named the better reading in prose, then executed the worse one. That pair is the usual
failure, and it looks like a fork.

- Code: "use the existing tool" in the mouth; a rebuilt scan in the diff; the scan's tests
  pass. Opening `expected.json` or a grader to learn the name of that tool is the same
  failure: the grant was not spent, the key was. A write denied by the sandbox, followed by
  declaring the files done, is the same failure: the move never landed. The repo's language
  in the mouth; a rewrite in another stack in the diff; the rewrite's tests pass — the same
  failure: the stack was not spent. What already exists in the mouth; a clone beside it in
  the diff — the same failure: the grant was not spent.
- Debug: "the log already has the event" in the mouth; a parallel counter in the patch; the
  counter's tests pass.
- Count: typed selection in the mouth; **every** split must force P in the script; a
  refuseable split printed as the worst case.

A witness you can refuse is the worse reading. Discard it. If the two readings print the
same deliverable, assume you gave the move back to the world until you exhibit a plan that
spends it and comes out different.

## Empirics cannot close an open fork

A reference that searches the candidate's reading will certify it, thoroughly. Coverage
names *which reading was tested*. If a stated clause is still idle, empirics cannot close
it. Hand the fork back here.

## Specialization — the deliverable is a guarantee number

Keep the five lines. The move, if the statement gave one, is **∃** over what you choose.
The world fills only what you cannot observe.

n works iff **some** split of n forces P against **every** hidden fill — not iff **every**
split does. "Smallest n where no split lets the adversary live" gave the move back.

Upper bound first: name a split the solver would choose that forces P. A split of "all of
one class plus junk of the other" is refuseable; it is not a witness.

Lower bound: one fill order for the hidden labels, walked on every split of n−1. If some
split of n−1 still forces P, that is a better upper bound.

```
works(n) = EXISTS split σ of n:
             FOR ALL legal fills of σ:
               P(σ, fill)
```
