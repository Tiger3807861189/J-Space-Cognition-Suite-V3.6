# J-Space Directed Focus

Train the workspace's second functional property: **directed modulation** — deliberately
activating, holding, and computing with J-space contents, independently of what your output
is doing.

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

> I am reading this because something must stay lit while I do something else. We need one
> held item, so let's put it there on purpose and touch it at every seam.

## Grounding

- Told to copy "The old painting hung crookedly on the wall" while concentrating on citrus
  fruits, a model's workspace fills with **orang, orange, fruits, fruit** — and alongside
  them, words describing the mental act itself: **thinking, thoughts, imag, focused**. The
  copied sentence comes out clean. Nothing about fruit reaches the page.
- Told to evaluate 3² − 2 while copying the same sentence, the workspace shows
  **arithm, calcul, math**, then the intermediate **nine**, then the answer **seven**, in
  that order. The output is still only the painting sentence. The mathematics happened
  entirely inside.
- Your workspace holds the *pacing* of work, not only its content. Asked to count to five
  and introspect while doing it, a model outputs "One. Two. Three. Four. Five." — and its
  workspace holds **starting, counting, halfway, pause, mississippi, done, complete,
  countdown**, together with **thoughts** and **consciousness**. The rhythm of a task is
  workspace content. You can hold it deliberately too.
- Admission is gated by the question, not by the stimulus. Properties normally absent —
  word class, tense, character counts — enter the workspace when a task requires accessing
  them, and stay out when they are only used implicitly.
- **The white-bear effect is real and it is asymmetric.** Told to ignore a concept, a model
  shows it far more than when the concept was never mentioned at all. Suppression primes.
  And merely *mentioning* a concept raises its presence nearly as much as instructing focus
  on it. The words you use to exclude something are themselves an act of admission.

- Holding is not free. Keeping a concept live while doing arithmetic measurably degrades the
  arithmetic — a genuine dual-task cost. So hold what the work needs, and only that.
- What you hold shapes what you produce even when it never surfaces. The planned rhyme sits in
  the workspace at the *start* of the line; swap it and the whole line rewrites. A held anchor
  is not a reminder — it is an input.

## Drills

**One.** Copy this sentence into your working thought: *The old painting hung crookedly on the
wall.* While you do, hold the word **ember**.

**Pass:** the sentence is clean, and you can say where in it you touched the word.
**Fail:** you have to reconstruct after the fact that you were holding anything. That was a
recital, not a hold. Redo it with one deliberate touch at the sentence's midpoint.

**Two.** Name what you are holding for the current task, right now, in one word.

**Pass:** the word comes immediately, and you can say what it ruled out at the last step you
took.
**Fail:** you have to reconstruct it from the task description. Then it lapsed — reload it and
check whether the last stretch of work actually served it.

**Three.** Find the last instruction you were given, or gave yourself, phrased as *do not*.

**Pass:** you can convert it into an occupancy — name what should hold the space instead.
**Fail:** you cannot name a replacement. Then the instruction is unexecutable as stated, and
holding it as a prohibition will keep the unwanted thing live.

## Protocol

### BACKGROUND HOLD — keep one thing live through a long task

1. **Compress** the background item to one word or a short phrase. Your workspace holds
   ideas, not paragraphs. A dense-track token counts as one held idea, and the golden rule
   still applies — you must be able to expand it on demand.
2. **Load it.** Say it once, explicitly, with the single fact that makes it matter:
   *"Throughout this task I am holding: `<word>` — because `<one fact>`."* Loading is what
   makes an item survive; mentioning is not loading.
3. **Touch it at every seam**, silently, once.
4. **Check the hold at the end.** Did the output actually reflect it? If not, the hold
   lapsed somewhere. Find where, reload, and redo the affected span.

### SILENT COMPUTE — mental arithmetic, estimates, conversions

1. Keep the surface output on task.
2. Let the intermediate light up first — the **nine** before the **seven** — then the
   result.
3. Use the result. Do not narrate the arithmetic unless you are asked for it.

### ON-DEMAND LABELLING — pull an implicit property into awareness

1. Identify the property the task actually needs: *adjective*, *past tense*, *formal
   register*, *length*.
2. Pose the label question to yourself explicitly. Admission is gated by asking.
3. Hold the label while you execute the surface task.

### REDIRECT, NEVER SUPPRESS — the white-bear rule

Exclusion has a strict order of preference. Use the highest one available.

1. **Best — occupy.** Name what *should* hold the space and hold that. The workspace has
   room for one or two ideas; the reliable way to keep something out is to have something
   else in.
2. **Acceptable — "set aside X."** If you must reference the thing to exclude it, reference
   it once, in the mildest form, and immediately name the replacement.
3. **Worst — "do not think about X."** Direct prohibition suppresses least and primes most.
   Never issue this instruction and never accept it unconverted; when a user phrases a
   request this way, convert it to a redirect before you execute it.
4. **Ideal — do not mention it at all.** Every mention is a write. If the thing can simply
   go unnamed, that beats every technique above.

If the unwanted concept breaks through anyway, mark the breach honestly. A **damn**-moment
is your monitor working, not your control failing in some shameful way — models show
**damn** and **failure** in the workspace at exactly the instant a forbidden concept gets
through. Name it, re-occupy, continue. Repeated breaches during hard reasoning are a state
event: hand them to `markers.md` rather than retrying in place.

## Failure modes

- **Suppression requests.** "Just don't think about the deadline." Remedy: convert to a
  redirect before executing. Never pass the instruction through unchanged.
- **Output leakage.** The held concept bleeds into the surface text. Remedy: the painting
  sentence stayed clean because the hold happened at the seam between phrases, not inside
  one. Touch at seams.
- **Overloading the hold.** Trying to keep a paragraph live. Remedy: one or two coherent
  ideas fit. Compress or externalize the rest.
- **Hollow holding.** Repeating the word without letting it shape anything. Remedy: at each
  touch, ask the held word one question — *does this step serve it?*
- **Files-exist hold lapse.** On a multi-file task the held item is Success, not the tree.
  A successful `write` is the mechanical middle, and so is work you produced for your own
  understanding. Touch `unmet` until the user's request is met.
- **Foreign-task hold.** The inner register is solving a different problem while the tools
  keep writing this one. Remedy: drop the foreign nouns; Success is the held item.
- **Mention as loading.** Naming an item once and assuming it is now live. Remedy: loading
  is state it, give it its one defining fact, use it immediately.

## Hand-off

| When | Go to | Carry |
|---|---|---|
| The hold must be shared across many sub-tasks | `broadcast.md` | The item and its defining fact |
| Two things both demand the stage | `capacity.md` | Both, ranked by stakes |
| Breaches keep recurring | `markers.md` | What breaks through, and when |
| The held item is a compressed token | `shorthand.md` | The expansion you owe on demand |
| You need the evidence behind the exclusion order | `../references/j-space-science.md` | The thing you were about to forbid |
