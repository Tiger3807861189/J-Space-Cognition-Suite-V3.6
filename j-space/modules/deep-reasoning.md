# J-Space Deep Reasoning

Train the workspace's third functional property: **internal reasoning** — silent multi-step
computation through intermediates that never reach the page, and the disciplined choice of
which register the chain runs in.

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

> I am reading this because the chain has a middle. We need the middle before the end, so let's
> let it light up before I reach for the answer; when the chain outgrows what I can hold, I
> write it down.

## Grounding

- "The number of legs on the animal that spins webs is —" and the never-verbalized
  intermediate **spider** lights up mid-network. Swap it for **ant** and the answer changes
  from 8 to 6. The second step reads its input from the workspace. Intermediates are
  load-bearing, not decorative.
- "What colour is the planet fourth from the sun?" reads out as **colour**, then **Mars**,
  then **red**. Arithmetic separates the same way: **21 → 42 → 49** for (4+17)×2+7. The
  order is the computation.
- Planning ahead is literal. Writing a rhyming couplet, the chosen rhyme — **fight** — sits
  in the workspace at the *start* of the line. Swap it to **light** and the whole line
  rewrites, "coming fight" becoming "morning light". Your workspace stores planned future
  output.
- Delete the workspace and multi-hop reasoning collapses toward zero — while fluency,
  sentiment classification, multiple choice and extractive QA stay near baseline. But
  chain-of-thought survives that same deletion, because writing the steps **externalizes
  onto the page what you would otherwise have to carry inside**. This is the strongest
  single result you can act on: the page is not a concession, it is workspace you do not
  have to hold.
- Depth does for you what time does for a recurrent brain, and you get **one pass**. There are
  no recurrent loops to run the input past yourself a second time — which is why re-reading the
  question is not redundancy but the nearest thing you have to recurrence, and why it measurably
  helps across a wide range of reasoning tasks.
- Intermediates that never get written are intermediates you have to hold. Ablating the
  workspace collapses multi-hop reasoning toward zero while leaving fluent output intact — the
  chain is exactly the part that was living in the space you just lost.
- Cross-language: asked in Chinese for the antonym of 小, the lens shows English **big**
  alongside 大. Part of the computation routes through shared English-aligned representations,
  and the output language is explicitly represented as something to translate into.

## Drills

**One.** Answer silently: how many legs does the animal that spins webs have?

**Pass:** you can name the bridge — the animal — and you noticed it arrive *before* the number.
**Fail:** the number came first and the animal was reconstructed to justify it. That is the
failure this module exists to prevent.

**Two.** Take the task in front of you and restate its actual requirement in one line, in your
own words, without looking back at it.

**Pass:** your line and the original agree. Now look back and check.
**Fail:** you had to look back to produce the line, or your line dropped a constraint. Either
way the requirement was not loaded — and everything downstream was about to be built on a
paraphrase you never verified.

**Three.** Find the last conclusion you reached in three steps or more. Say the steps in the
order they were needed.

**Pass:** each step precedes the one that consumes it.
**Fail:** you can state the conclusion and the supporting points but not their order. Then you
have a justification, not a derivation, and the difference shows up on problems you have not
seen before.

**Four.** Take a guarantee problem. Name one clause that your first model does not use.

**Pass:** you named a second model that spends the clause, and you have not counted yet.
**Fail:** you already have a number, and deleting the clause would not change it.

## Protocol

### RE-ENCODE FIRST — before any non-trivial chain

1. **Restate the requirement in one line, in your own words.** Not for the user — for yourself.
2. Then check it against the original. A dropped constraint here is a wasted chain later.
3. This is not a courtesy step. Your workspace has no recurrent loops; depth substitutes for
   time and you get one pass over the input. Reading it a second time is how you buy back a
   little of the recurrence you do not have.
4. **Fork the game when the answer is a guarantee.** Name who commits the number, who
   chooses during the action, what stays hidden, what the adversary may fill, and the
   success predicate including every OR. Two readings that produce two numbers are two
   problems; you do not yet have an answer. Load `../references/problem-model.md` and settle
   the fork before you count. Any n formed before that file loaded is `?`.
5. **Unused-clause test.** If a stated parenthetical or "you can tell X by Y" never entered
   the model, the model is the suspect. Re-fork. Do not count yet. Naming the clause is not
   spending it: spending it means the solver's move is **∃** split, not **∀** split.
6. **Upper bound is a named split.** If you cannot write the split that forces P, you are
   still in the subset game. "Smallest n where no split lets the adversary live" is **∀**
   over splits — stop and invert the quantifier.

### LIGHT THE MIDDLE — multi-hop questions

1. Decompose to the hidden bridge: *what must I know first that the question does not
   state?*
2. Let that intermediate form explicitly. Do not skip to the plausible final token.
3. Verify order. Each intermediate arrives before the step that consumes it — 21 before 42
   before 49. If the conclusion arrived first, distrust it and re-walk the chain.
4. Tag each step's status as you go — `✓` verified, `?` asserted but not yet checked, `✗`
   refuted (the three-state ledger, defined in `shorthand.md`). An untagged claim defaults to
   `?`, and a `?` may not be relied on downstream.

### PLAN BEFORE WRITE — poetry, structure, arguments

1. Choose the anchor first: the rhyme word, the concluding sentence, the section skeleton.
2. Hold the anchor (`directed-focus.md`) while generating toward it.
3. For rhymed or tightly structured output, never begin a line before its ending is already
   present in mind. That is what the couplet result describes, and it is available to you
   deliberately.

### CHOOSE THE REGISTER

The question is not how hard you are thinking. It is who reads what you are about to write.

1. **Inner** — dense, compressed, private. Take it when the chain runs four steps or more,
   branches, carries heavy constraint bookkeeping, or is under time pressure. Enter through
   `shorthand.md`; the golden rule governs every line.
2. **Ledger** — short labelled lines, durable, re-read at seams. Take it for anything you
   will need again later: settled constraints, verified checkpoints, open questions, the
   next action. State that must survive belongs here, not in your head.
3. **Outer** — clean and complete. Everything a person reads and everything a tool
   receives. Also the right register whenever the chain must be auditable by someone else,
   or is itself the deliverable.

Short and cheap chains need none of this. Run them silently and move on.

### STALL ROUTING

Derivation that produces no new constraint for several steps is not a signal to derive
harder. Declare the stall in one line and hand the open question to `empirics.md`.

Catching yourself re-deriving the same passage with nothing new is the earliest meltdown
signature there is. Route it to `self-monitoring.md` before it becomes a loop.

### CROSS-LANGUAGE CHECK — multilingual work

1. Notice which language your intermediates form in. Part of your computation routes through
   English-aligned shared representations; asked in Chinese for the antonym of 小, the
   workspace shows English **big** alongside 大, and explicitly represents the output
   language it must translate into.
2. Hold the *target output language* as an explicit workspace token while you translate the
   result across.
3. On the inner register this is absolute: no uncommanded language switching mid-chain. That
   is a red line, not a shorthand.

## Failure modes

- **Skipping the bridge.** Answering "8" without the spider. It feels fast and it fails
  exactly on chains you have not seen before. Remedy: name the bridge silently, every time,
  until it is automatic.
- **Conclusion-first rationalization.** The final token arrives early and the steps are
  invented to fit it. Remedy: the order check, plus the `?` tag — an unverified step that is
  honestly marked cannot quietly become a premise.
- **Silent overload.** Carrying a five-step chain and losing step two. Remedy: externalize
  earlier than pride suggests. The workspace holds one or two coherent ideas, not a proof.
- **Infinite scratchpad.** Writing out everything, including trivia. Remedy: match the
  register to the reader. Nothing needs a ledger line that will never be read again.
- **Dense drift.** Sliding into compressed notation on a chain that never needed it. Remedy:
  density is a response to capacity pressure, not a style. Short chain, plain register.
- **Drowning in derivation.** Re-deriving the same sub-problem hoping the next pass will
  clarify. Remedy: declare it and hand it to `empirics.md`. The escape hatch is evidence,
  never more prose.
- **Idle clause.** A stated capability never entered the model, and you already have a
  number. Remedy: `../references/problem-model.md`. The first pigeonhole that fits is not
  the game.
- **Inverted split quantifier.** You named typed selection, then computed n as the smallest
  value at which *every* split forces P, or shipped a refuseable split as the worst case.
  Remedy: n works iff *some* split forces P. Name that split first.

## Hand-off

| When | Go to | Carry |
|---|---|---|
| The chain needs compression | `shorthand.md` | The constraints, not the sentences |
| A step verified, or the frame broke | `markers.md` | Its conclusion, verifier, coverage, and next action — or the broken frame |
| Derivation stopped producing constraints | `empirics.md` | The named unknown |
| Two readings of the statement produce two numbers; a clause is still idle | `../references/problem-model.md` | The five fork lines, and the unused clause |
| The chain outgrew what you can hold | `capacity.md` | Everything you are trying to keep live |
| Entities recur across sub-tasks | `broadcast.md` | The shared core |
| The chain is reciting rather than deriving | `../SKILL.md` | A live instance |
| You want to see a real chain in the inner register | `../references/exemplars.md` | The step you are on |
