---
type: book
status: structured
quality:
topics: [spaced-repetition, software-engineering]
source: ""
created: 2024-12-26
published:
author: ""
flashcards: none
updated: 2024-12-30
---
- feeding my markdown notes into O1 and asking for flashcard questions


# 1 Chapter 1: Generators
## 1.1 Flashcard 1

**Q**: **What is the difference between an _iterable_ and an _iterator_ in Python?**  
**A**:

- An **iterable** is any object you can pass to `iter()` to produce an iterator (it usually implements `__iter__()` or `__getitem__()`). Examples include lists, tuples, strings.
- An **iterator** is the object returned by calling `iter(iterable)`; it knows how to fetch the _next_ item (via `__next__()`) and raises `StopIteration` when exhausted.

---

## 1.2 Flashcard 2

**Q**: **How does a generator function differ from a regular function, and what role does `yield` play?**  
**A**:

- A **generator function** uses `yield` instead of `return`, returning a _generator object_ that produces values **lazily** (on demand).
- Each `yield` acts like a **checkpoint**: the function’s state (local variables and execution position) is paused, then resumes exactly where it left off the next time you request a value.

---

## 1.3 Flashcard 3

**Q**: **Why is lazy evaluation with generators often more memory-efficient than building a full list?**  
**A**:

- **Lazy evaluation** means a generator only computes the _next_ item when needed, rather than building all items upfront. This avoids creating and storing large intermediate lists in memory, making it more scalable for large data or streaming scenarios.

---

## 1.4 Flashcard 4

**Q**: **What happens when you call `next()` on an exhausted iterator or generator?**  
**A**:

- It raises a **`StopIteration`** exception, indicating there are no more items to retrieve. In a `for` loop, Python automatically catches this exception to end the loop.

---

## 1.5 Flashcard 5

**Q**: **What is “scalable composability” in the context of Python, and how do generators enable it?**  
**A**:

- **Scalable composability** is the practice of writing small, reusable functions that you can assemble to tackle larger or more complex tasks without rewriting code.
- **Generators** enable this by providing _lazy outputs_ that can be chained, filtered, or mapped in sequence—each step is a standalone component that easily plugs into bigger workflows.


# 2 Chapter 2: Collections + Comprehensions


# 3 Chapter 3
# 4 Chapter 4
# 5 Chapter 5
# 6 Chapter 6
# 7 Chapter 7