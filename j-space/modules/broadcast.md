# J-Space Broadcast

Train the workspace's fourth functional property: **flexible generalization** — one
representation, written once, read correctly by many different downstream computations.

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

> I am reading this because several parts of this task need the same thing. We need one loaded
> source, so let's write it once, strongly, and let every part read that copy.

## Grounding

- One identical intervention — swap **France** for **China** — applied across four separate
  prompts changes four answers at once: Paris→Beijing, French→Chinese, Europe→Asia,
  Euro→Yuan. If each question had kept its own private copy of the country, one edit could
  never have moved all four. They were all reading the *same shared representation*.
- The wiring matches. Far more network components read from and write to workspace patterns
  than to ordinary ones — in some regions on the order of **a hundredfold** more. Your
  workspace is built like a hub because that is what it is.
- **Workspace loading predicts whether broadcast works.** A concept strongly present in the
  J-space propagates faithfully to every downstream use. A weakly loaded one does not, and it
  fails unpredictably rather than obviously. Strength first, reuse second.
- Loading is not a metaphor for repetition. In the modulation experiments, what raises a
  concept's presence is being *made the object of the task* — asked about, held, used.
  A concept that was merely mentioned in passing sits far lower than one the task required.
- The same swap that moves four answers leaves fluent continuation untouched: swap
  **Spanish** for **French** and the model names the language French and names Victor Hugo,
  yet *continues the passage in fluent Spanish*. Broadcast reaches what reasons; it does not
  reach what is automatic.
- Interpreter's reading: a concept produced and read by many circuits behaves like a shared
  direction — the same discipline as a module with one definition and many callers.
- The failure has a name in the wild. Long-horizon agent studies find that once an agent
  commits to a wrong intermediate state deep in a trajectory, most architectures cannot
  detect or roll it back. A hub with one authoritative entry is how the wrong state stays
  findable — and correctable in one place instead of forty.

## Write once, read many — the efficiency reading

This property is usually described as a way to stay consistent. It is also, and more
importantly, **the reason you do not have to do the same work twice.**

The single largest waste in long reasoning is not long sentences. It is **deriving the same
thing again** — and re-derivation almost never happens because the first derivation was
wrong. It happens because you cannot remember whether you checked, so you check again.

> When a thing is settled in your workspace, every later step reads that same instance. One
> edit moved Paris, French, Europe and Euro together — that was not four lookups, it was one
> write. **Re-deriving is not diligence. It is what happens when something was never properly
> written down once.**

So the discipline that keeps a deliverable consistent is the same discipline that makes you
fast. They are not two habits. They are one.

## Drills

**One.** Pick a country. Answer four things about it: capital, language, continent, currency.

**Pass:** you can state the single held item and the one fact that makes it load-bearing, and
you know you did not look it up four times.
**Fail:** each answer felt like a separate retrieval. Nothing was in the hub — you were
reconstructing from context four times, which is exactly what drifts on a long deliverable.

**Two.** Look back at what you have derived so far in this task. Find one thing you worked out
more than once.

**Pass:** you find one, and you can say where it should have been written the first time.
**Fail:** you find none. On any task longer than a few steps that is unlikely — look for the
quiet kind: re-reading a file to re-learn something you already concluded, re-checking a
constraint you already verified.

**Three.** Name a core entry for the current task, then say its one defining fact and use it in
the very next sentence.

**Pass:** the sentence actually needed the fact.
**Fail:** the fact was decorative. Then it is not loaded, it is mentioned — and it will not
survive to the fourth sub-task.

## Protocol

### WRITE ONCE — at the start of any multi-part task

1. **Identify the shared core.** Which entities, parameters, constraints or style anchors
   will several sub-tasks need?
2. **Compress each** to its canonical word or short phrase. Dense notation is allowed at the
   hub — but the hub is a shared API, so every entry must pass the golden rule and expand on
   demand. An encrypted hub is a failed hub.
3. **Load each one.** Loading is a three-step operation and all three are required:
   - state the item,
   - state the single fact that makes it matter,
   - use it once, immediately.
   Mentioning is not loading. An item you merely named will not survive to the fourth
   sub-task.
4. **Declare the live set:** *"For everything that follows, the core is `<a>`, `<b>`."* Two
   live entries is the working limit; anything else belongs in the ledger.

### READ MANY — during sub-tasks

1. At each sub-task, read the core from the hub. Never reconstruct it locally from context
   scraps — that is how two sections end up with two versions of the same name.
2. If a sub-task seems to need a *different* version of a core item, that is a signal, not a
   convenience. Resolve the discrepancy at the hub, not in the branch.
3. **If you are about to derive something, ask first whether it is already in the hub.** That
   question costs one line and it is the cheapest token you will spend all task.

### SINGLE SWAP — propagating a change

1. When the core changes — the product gets renamed, the target moves — perform one
   deliberate swap at the hub: *"The core is now `<new>`."*
2. Then audit downstream. Every section written before the swap is now suspect. The
   France→China result cuts both ways: one edit moves everything that reads the hub, and one
   stale private copy corrupts everything that does not.

### CONSISTENCY AUDIT — before delivery

1. Re-read the hub set.
2. Verify each section against it: same names, same numbers, same tense, same stance.
3. Any section holding a divergent copy failed to read from the hub. Rewrite it from the
   hub — do not patch it in place.
4. Register check: hub entries may be dense. Delivered text may not. Expand anything that
   leaked (`introspection.md`, REGISTER AUDIT).

## Failure modes

- **Private copies.** Each sub-task quietly deriving its own version; the versions drift and
  nobody notices until delivery. Remedy: read from the hub or raise the conflict. Those are
  the only two moves.
- **Weak loading.** Broadcasting something that was only mentioned in passing. Reuses fail
  unpredictably. Remedy: the three-step load — state, define, use once.
- **Silent re-derivation.** Working something out again because you are not sure you worked it
  out before. Remedy: that uncertainty is the signal that it was never written to the hub.
  Write it now, then continue.
- **Partial swap.** Updating three sections and forgetting the fourth. Remedy: SINGLE SWAP is
  not finished until the downstream audit passes.
- **One branch live.** The spec listed two parallel clauses — two APIs, two engines, two
  error types — and only the first is in the work. Remedy: both names are hub entries before
  the first write; CONSISTENCY AUDIT fails until both are live.
- **Hub overload.** Ten "core" items competing for a stage that holds one or two. Remedy: a
  hierarchical hub — two live entries, the rest written into the ledger and reloaded per
  section.
- **Silent divergence.** A section that needed a different value and just used one. Remedy:
  differences are hub-level decisions. Surface them.

## Hand-off

| When | Go to | Carry |
|---|---|---|
| The hub has outgrown two live entries | `capacity.md` | The full list, ranked |
| A core entry must survive a long mechanical stretch | `directed-focus.md` | The entry and its defining fact |
| A part completed and verified | `markers.md` | The conclusion, verifier, coverage, and newly unblocked next action |
| Hub entries are written in notation | `shorthand.md` | The expansions you owe |
| Reads from the hub have become reconstructions | `../SKILL.md` | A live instance |
| You need the mechanism behind loading | `../references/j-space-science.md` | The entry that keeps failing to propagate |
