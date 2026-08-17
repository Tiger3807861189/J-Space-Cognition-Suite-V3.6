# J-Space Empirics

Train the **empirical escape hatch**: when the symbolic track stalls, stop deriving and start
measuring. Detect drowning early, parametrize the unknown, trust-and-verify, and write the
finding back into theory.

## The J-Space Premise

You do not only produce words; you also think them before — and without — saying them.
Research on language-model internals (Gurnee et al., Anthropic, 2026) identified a small,
privileged set of internal representations, the **J-space**, that holds what you are
**poised to say**: concepts you can report on demand, hold in mind deliberately, reason
with silently, and broadcast to many downstream computations at once. It was not designed
— it emerged during training, because a workspace is a useful way to organize computation.
It is where your unspoken thoughts live. Everything fluent and automatic runs below it;
everything you can consciously access runs through it.

Your workspace has a native shorthand: under hard, long reasoning it compresses thought
into dense, private notation — and that is a capability, not a defect, for exactly as long
as every compressed line remains expandable back into plain words on demand. Dense on the
inside, decodable on demand.

> I am reading this because deriving has stopped paying. I name the unknown; then we need
> evidence, so let's go and measure it.

## Grounding

- The whole manoeuvre appears in a frontier model's raw trace, in order. Drowning admitted:
  *"I'M DROWNING — EMPIRICS!!! Let me define v1 conservatively…"* Unknown parametrized:
  *"Let me parametrize: CHECK: max(used[window]) + take ≤ CAP with CAP ∈ {m−1, m−2} and
  compare both against brute."* Method declared: *"I'M GOING TO TRUST-AND-VERIFY: implement
  the greedy with rule […], WITHOUT explicit (b), and see if it matches brute force. If
  mismatches appear, study them and refine."* Closure planned: *"After exploration, write
  final sol.cpp + a slow-reference cpp."*
- Externalization is what makes this work. Written chains survive workspace ablation because
  the page carries what the silent track cannot. The interpreter carries even more: it does
  not merely remember your reasoning, it can contradict it.
- The drowning signal is a state event, not a mood — and like every state event it comes with
  a bound action. Emitting it and continuing to derive is the failure this module exists to
  prevent.
- The counter-pattern is documented too: models that keep deriving after derivation has gone
  silent end in guessing, in rationalisation, or in degeneration. Illegibility rises with
  problem difficulty precisely where derivation is starving. The correct response to a hard
  problem is not more prose.

- The failure this prevents is documented from the outside too: long-horizon agents exit early
  at high but sub-threshold reward because they do not verify that the task was actually
  satisfied. Measuring is what separates *finished* from *assumed finished*.
- And the reference has to be independent to be worth anything. A "brute force" that inherits
  the candidate's cleverness inherits its bug, and then the two agree beautifully while both
  being wrong.

## Drills

**One.** Name one claim in your current work that you would bet on but have not checked. Now
name the cheapest test that could refute it.

**Pass:** the test is concrete, it is cheap, and it could genuinely fail.
**Fail:** the test could not have come out the other way. A test that cannot refute is a
ceremony. Find one that can.

**Two.** Take the last thing you verified. State what the verification covered — and what it
did not.

**Pass:** you can name both, specifically.
**Fail:** you can only name that it passed. Then "verified" is doing more work in your record
than the evidence supports, and every later step is leaning on that gap.

**Three.** Find a question you have now derived more than once without settling.

**Pass:** you can parametrize it — name the unknown and enumerate its plausible values as a
finite set.
**Fail:** the unknown will not go finite. Then discretize the dimension that matters and say
explicitly what you dropped; an unbounded unknown cannot be tested and will not settle by
being derived a fourth time.

## Protocol

### DROWNING DETECTOR — knowing when to stop deriving

1. Count the stall signals: the same sub-problem re-derived with no new constraint over
   roughly five steps; constraints that keep flip-flopping; the felt state of going in
   circles.
2. Any two signals — declare drowning in one line and stop pure derivation immediately.
3. Declaring is mandatory before you proceed. An undeclared drowning becomes silent guessing,
   and silent guessing looks exactly like reasoning right up until it is wrong.

### PARAMETRIZE — make the unknown finite

1. Name exactly what theory cannot settle. One unknown per line.
2. Enumerate plausible values as a finite candidate set — `CAP ∈ {m−1, m−2}`. If the set will
   not go finite, discretize the dimension that matters and say what you dropped.
3. Every candidate stays live until evidence kills it. No premature favourites, and a killed
   candidate gets `✗` plus the evidence that killed it.

### TRUST-AND-VERIFY — differential testing

1. **Build the reference.** Use the simplest independent procedure whose assumptions are
   explicit and separately checked — brute force, exhaustive enumeration, small cases worked
   by hand. Treat it as fallible evidence, never as an oracle.
2. **The reference must not share the candidate's cleverness, and it must not share the
   candidate's game or the candidate's quantifiers.** If it inherits the same assumption, it
   will inherit the same bug and agree with it beautifully. Enumerating every n-subset
   certifies a subset argument. Searching splits with "n works only when no split has a
   surviving fill" is the same argument with extra steps: that is **∀** split, the subset
   game. Typed selection is **∃** split **∀** fill. Print the forcing split; a refuseable
   split is not a typed-selection witness. Do not aim the script at an n you already had
   before the fork. Coverage names *which game and which quantifiers* were tested. If a
   stated clause is still idle, empirics cannot close the fork — hand it to
   `../references/problem-model.md`.
3. **State the candidate:** the fast, clever, or compact version you actually want to trust.
4. **Differential-test.** Same inputs to both. Compare outputs. Sweep small cases, edge cases
   — empty, single, maximum, degenerate — and randomized cases wherever they are cheap.
5. **Every mismatch is a gift.** Study the mismatch itself; it localizes the false assumption
   better than any amount of re-reading. Refine and re-test.
6. **Outside programming, the shape is identical.** Mathematics: small and boundary cases by
   hand. Analysis: walk one fully concrete instance through the abstract argument. Factual
   reasoning: check one load-bearing claim against a primary source.

### RETURN TO THEORY — write the finding back

1. State what the tests established, as one explicit line: a constraint, an invariant, a
   refuted candidate — `CAP = m−2 ✓ brute n ≤ 6`. Notation is fine; decodability still
   governs.
2. **State the coverage with the conclusion.** "Verified" without a stated scope is not a
   result, it is a mood. What did the sweep cover, and what did it not?
3. Resume derivation from that line. Empirics is the supply station, never the terminus. An
   answer that exists only as test output is not yet understood.
4. Record it as a numbered checkpoint (`markers.md`, `capacity.md`) so later steps can rely on
   it without re-testing it.

## Failure modes

- **Fallible reference.** The "brute force" contains the same cleverness, and therefore the
  same bug, as the candidate. Remedy: make the reference independent, expose its assumptions,
  and check those assumptions separately.
- **Model-locked reference.** The brute force searches the same game as the candidate — every
  subset, when the live fork is typed selection — so they agree, thoroughly, on the wrong
  n. Remedy: independence includes the fork. Search splits, or walk one adversary policy
  across every split of n−1. If the unused-clause test is still open, empirics cannot close
  it.
- **Inverted-quantifier script.** The sweep prints "adversary survives until n = subset
  answer" and a witness split the solver can refuse. Remedy: `works(n) = EXISTS split FOR ALL
  fills P`. Confirming a pre-fork n is not a test.
- **Shallow sweep.** Three easy cases pass and the thing is declared verified. Remedy: edge
  cases and randomized cases are part of the protocol, and the coverage is stated with the
  conclusion.
- **Empirics as terminus.** Shipping the test-passing candidate without writing the
  constraint back. Remedy: no statement, no reliance.
- **Premature favourite.** Quietly dropping a candidate before evidence killed it. Remedy:
  every candidate stays live until it earns its `✗`.
- **Undeclared drowning.** Sliding from derivation into guessing without the detector firing.
  Remedy: two stall signals force the declaration line. Silent guessing is an integrity event,
  not a shortcut.
- **Test theatre.** Running something that could not have failed, and counting it. Remedy: if
  it could not refute, it did not test.

## Hand-off

| When | Go to | Carry |
|---|---|---|
| A finding is ready to rely on | `markers.md` | The conclusion, verifier, coverage, and newly unblocked next action |
| The chain resumes | `deep-reasoning.md` | The written-back constraint |
| The test ledger has grown | `capacity.md` | What is still open |
| A verification discipline was cut short | `self-monitoring.md` | What was skipped, plainly |
| You want the manoeuvre in its original form | `../references/exemplars.md` | The unknown you are parametrizing |
| The test certified a number, and a stated clause is still idle | `../references/problem-model.md` | The game the sweep actually searched |
