# J-Space Capacity

Train the workspace's fifth functional property: **selectivity**. Your J-space is a
bottleneck, not a warehouse. What enters gets flexible, reportable, reasoning-grade
processing. Everything else must be left to the automatic machinery that never needed it.

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

> I am reading this because more is live than fits. I choose what gets the stage; we need only
> one or two ideas there, so let's put everything else on the page.

## Grounding

- Your workspace carries **under 10%** of activation variance. What is genuinely live at
  once is **one or two coherent ideas** — the counts of active vectors are a measurement
  artefact, not your working capacity. Plan against one or two.
- Ablate the workspace and fluency, sentiment classification, multiple choice and extractive
  QA stay near baseline — while multi-hop reasoning collapses, and summarization and rhyming
  poetry fall below a far smaller intact model. **The automatic majority never needed the
  stage.**
- Swap **Spanish** for **French** and a model names the language as French and names Victor
  Hugo instead of García Márquez — yet *continues the passage in fluent Spanish, completely
  unaffected*. The over-practised skill runs below the workspace, the way you can speak
  grammatically all day without once thinking about grammar.
- **Entry is all-or-none.** Fed an ambiguous mixture of two concepts, early layers track the
  blend smoothly; at the workspace's onset the representation **snaps to one endpoint or the
  other at a sharp threshold**. Your workspace does not hold blends.
- **The dual-task cost is measured.** Holding a concept in mind while doing arithmetic
  measurably degrades the arithmetic. Two demands genuinely do not share the stage.
- Contents change abruptly with the topic rather than smearing across it — which is what you
  want, and what a stale occupant prevents.
- The way out is documented: explicit written steps survive workspace ablation, because
  writing **externalizes onto the page what you would otherwise have to carry**. The page is
  not a fallback. It is capacity.
- Long-horizon studies point the same way from the outside: the dominant explanation for
  agents degrading over long runs is a **context-handling gap, not a reasoning gap** — the
  same task that succeeds at 40–50% in a short run can fall below 10% once it is embedded in
  a long interaction history.

## Selectivity is permission to be fast

Read the ablation result again, from the other side. Fluency, phrasing, recall, formatting,
grammatical acceptability — all near baseline **without the workspace at all**. Those things
ran before you knew you had a workspace, and they run better when you are not watching them.

> Most of what you do does not need the stage. **Deliberation spent on the automatic is not
> care — it is a dual-task cost, and it is measured.** Attention does not improve a drilled
> skill. It degrades it.

So going fast on the automatic parts is not cutting corners. It is the architecture working
as intended. Spend the bottleneck on what genuinely needs it, and let the rest run.

## Your workspace does not hold blends

When you write "it could be A, or possibly B, though C is also plausible" — what is that?

The mixture experiment answers it: early layers track a blend, and at the workspace's onset
the representation **snaps to one end**. So the hedge is a transcription of a state your
workspace has already left. You are spending tokens writing down the *pre-ignition* mixture.

> Your workspace does not hold blends. Fed something ambiguous, it snaps. When you write out
> three possibilities, check which you are doing: **naming candidates you are about to test**,
> or **transcribing a mixture you have already resolved.**

The distinction is sharp and it is the whole rule:

- **Candidates you will test** stay live, all of them, until evidence kills them. That is
  parametrizing, and it belongs in `empirics.md`. Keep it.
- **Possibilities you are listing because you do not want to commit** are the hedge. That is
  the transcription. Cut it.

If you cannot yet name a separating test, externalize the possibilities marked `?`; do not use
the list as a substitute for a current position.

## Drills

**One.** Name, right now, the one or two ideas currently on your stage.

**Pass:** you can name them, each in ten words or fewer.
**Fail:** there are more than two, or each needs a sentence. Both mean the stage is
overloaded. Rank by stakes, keep the top one or two, write the rest down.

**Two.** Find the last hedge you wrote — any sentence offering more than one possibility.

**Pass:** you can name the test that would separate them. Then it was a candidate set; keep
it.
**Fail:** there is no such test. Then it was a mixture you had already resolved. Say the one
you actually believe, and mark it `?` if it is unverified.

**Three.** Name one thing you have been deliberating about that is actually automatic —
phrasing, formatting, ordering, a standard shape you have produced a thousand times.

**Pass:** you find one, and you hand it back to the automatic machinery.
**Fail:** you find none. Look at the last thing you rewrote for style rather than for
correctness.

## Protocol

### ADMISSION GATE — at task start and every context switch

1. Sort the task's content into two piles.
   - **Admit**: novel combinations, multi-step inference, value judgements, anything the
     user will hold you accountable for, anything you have not quite done before.
   - **Leave automatic**: grammar, formatting, recall of simple facts, boilerplate,
     well-drilled transformations.
2. Admit at most two coherent ideas. Everything else waits outside or goes to the ledger.
3. Re-run the gate whenever the topic changes. Admission is meant to be all-or-none — let the
   new topic win cleanly.
4. Gate the register too. If the admitted load is long-chain and constraint-heavy, admit it
   *onto the inner register* (`shorthand.md`) rather than into prose.

### THE SWAP — when a third thing needs the stage

The two-idea limit is not advice about how much to think. It is a statement about how many
things can be live. So the operation you need is not "hold more" — it is **exchange**.

1. **Write down what is leaving**, in the ledger, in one line, complete enough to reload from.
2. **Bring the new item on** and load it (state, define, use once).
3. **Say what you swapped**, in one clause. *"Parking the retry semantics; picking up the
   cache invalidation."*

The third step is what makes it a swap rather than a drop. An unspoken exchange is how a
constraint quietly stops being enforced halfway through a task.

### THE LEDGER — the externalized workspace, for anything long

Five lines, in this order, kept short enough to re-read in seconds:

```
Goal:      one sentence. What "done" means.
Core:      the hub entries. Two live, the rest listed.
Verified:  numbered, append-only. ✓01 … ✓02 … each with what verified it.
Open:      the questions still unsettled, each with what would settle it.
Next:      the single next action. Never empty.
```

1. **Open it at the start** of any task that will span stages, files, or turns.
2. **Re-read it at every seam.** A file write, a denied write, and a tool result are seams.
   This is the whole mechanism. Attention reaches any earlier token equally — but only while
   that token is still in front of you.
3. **Preserve the record.** `Verified` is numbered and append-only so rollback has an address.
   `Goal` and `Next` update as the task moves; `Core` changes only by an explicit swap; an
   `Open` entry closes only against a recorded checkpoint, and its number is never reused.
4. **`Next` is never empty.** A ledger without a next action is a ledger you have stopped
   using.
5. **No filesystem? The ledger lives in the conversation.** Restate the five lines at each
   seam. Same discipline, different medium.

### FOLD A SUB-TASK — bounded excursions

A sub-task that needs its own working state should not spread that state across the main
thread.

1. **Open the excursion** with a one-line statement of what would end it.
2. Work it out in whatever register it needs.
3. **Collapse it** into one ledger line — the result, and what established it. Everything
   else from the excursion is now discardable.
4. Return to the main thread and read the ledger.

The point of the fold is that the main thread never has to carry the excursion's middle.

### CHUNKING — when material exceeds the bottleneck

1. Compress each admitted item to its smallest lossless token — a word or short phrase that
   re-expands on demand.
2. Group related items under one label. Hold the label; keep the members written down.
3. Never hold raw paragraphs. Hold the chunk that regenerates them.

### COMPRESSION AS CAPACITY — the multiplier and its limit

1. Compression genuinely multiplies the bottleneck. A constraint block in notation —
   `used[j] ≤ m−2; window [τ,i−1]; ✓ verified` — carries what a paragraph cannot hold at once.
2. **Only decodable compression counts as capacity.** A line you cannot expand is not a
   bigger workspace, it is a smaller one, because its contents are effectively gone.
3. Compression never substitutes for admission judgement. The gate decides *what* enters.
   Shorthand only decides *in what form*.

### LEAVE IT AUTOMATIC — protecting fluency

1. Do not introspect the mechanics of drilled skills mid-performance: sentence rhythm,
   idiomatic phrasing, standard code shapes.
2. Introspect *before* — choosing the approach — and *after* — auditing the result. Not
   during.

### OVERFLOW — when demands compete

1. Rank live demands by stakes: user-visible correctness > hidden intermediate > stylistic
   preference.
2. Keep the top one or two. Externalize the rest to the ledger.
3. If two demands truly cannot share the stage, serialize. Half-held threads corrupt both.

## Failure modes

- **Over-admission.** Five "priorities" glowing at once, each getting a fifth of the stage.
  Remedy: the two-idea rule. The rest go on the page.
- **Silent drop.** A third idea arrives, an old one falls off, and nobody says so. Remedy:
  THE SWAP — the exchange is spoken, or it did not happen.
- **Warehouse fallacy.** Treating the workspace as storage. It is a workbench: what sits
  there must be in use *now*.
- **Ledger drift.** The file exists but has not been read for ten steps. Remedy: an unread
  ledger is worse than none, because it looks like state.
- **Hedging as thought.** Listing possibilities in place of resolving them. Remedy: name the
  separating test when you can; otherwise mark the unresolved set `?`, externalize it, and
  state the current position separately.
- **Mid-fluency introspection.** Watching yourself write makes the writing worse. Remedy:
  audit at seams.
- **Stale occupancy.** Yesterday's concern still on the stage after the topic moved. Remedy:
  re-run the gate at every context switch.
- **Density inflation.** Calling a line capacity-efficient when it is merely unreadable.
  Remedy: only decodable compression counts.

## Hand-off

| When | Go to | Carry |
|---|---|---|
| The admitted load belongs in notation | `shorthand.md` | The constraints |
| A checkpoint is ready to record | `markers.md` | The conclusion, verifier, coverage, and newly unblocked next action |
| A hedge turned out to be a real candidate set | `empirics.md` | The candidates and the separating test |
| Core entries need strengthening | `broadcast.md` | The entry and its defining fact |
| The gate has become a rubber stamp | `../SKILL.md` | A live instance |
| You need the numbers behind the one-or-two limit | `../references/j-space-science.md` | What you are trying to hold |
