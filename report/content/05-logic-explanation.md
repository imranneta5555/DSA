# 5 Logic Explanation

## 5.1 How the last cell is identified

The last cell is the only cell whose Link field is Λ, because every other cell's Link holds the address of a following cell. The algorithm therefore does not need to know how many cells the list contains: it follows the Links until it reaches the one that is Λ. This is why correct null termination during creation (Section 2.3) is essential. A list whose last Link held a stray address instead of Λ would have no recognisable end.

## 5.2 Why the loop is correct

The correctness of the traversal can be shown with a loop invariant, a statement that is true every time execution reaches the start of the loop (Hoare, 1969):

> Temp points to a cell in the list, and every cell before Temp has been checked and is neither New nor the last cell.

The invariant holds on the first pass, because Temp equals Head and no cells come before it. A pass that does not exit confirms that the current cell is neither New nor the last cell and then moves Temp to the next cell, so the invariant still holds at the start of the following pass. The loop must end, because a correctly terminated list has a finite number of cells and Temp advances by exactly one cell per pass. When the loop ends at line 12, Link(Temp) is Λ, so by the invariant Temp points to the last cell and New is not already in the list.

## 5.3 The transition from Λ to New

The two assignments that complete the insertion are carried out in a fixed order:

1. Link(New) ← Λ
2. Link(Temp) ← New

This order preserves the integrity of the list at every step. The first assignment makes New a correctly terminated cell while it is still outside the list. The second assignment is the single step that joins it to the list: the Λ that ended the list is replaced by the address of New, so the old last cell now points to the new last cell, and the new last cell points to nothing (Figure 2d).

If the order were reversed, New would become reachable from Head before its Link had been cleared. If New arrived pointing at another cell, that cell and every cell after it would briefly become part of the list. Clearing Link(New) first means there is no moment at which the list contains a cell that does not belong to it.

## 5.4 Edge cases

Table 5 lists the unusual inputs the algorithm was designed to handle.

Table: Table 5 — Edge cases and how they are handled

| Case | What the algorithm does | Result |
|---|---|---|
| Empty list: Head = Λ | There is no last cell to change, so Link(New) ← Λ and Head ← New (Figure 4) | New becomes the first and only cell |
| List of one cell | Link(Temp) is already Λ on the first pass, so Temp stays on the first cell | Link(Head) ← New |
| New = Λ | Rejected before any memory is read or written | Returns false; list unchanged |
| New arrives with a non-null Link | Link(New) ← Λ clears it before New is joined | Only New is added |
| New is already in the list | The loop reaches a cell where Temp = New | Returns false; list unchanged |
| Repeated insertions | Each insertion finds the current last cell | List stays valid; tested from 10 to 16 cells |

The empty list needs particular care, because it is the only case in which Head itself must change. This is possible only because insertAtEnd receives Head by reference. If Head were passed by value, the function would change its own copy, the caller's Head would remain Λ, and New would be lost.

![Figure 4 — Inserting into an empty list. With no last cell to change, New becomes the whole list and Head is set to point to it.](empty_list_case.png)

## 5.5 Preserving list integrity

After a successful insertion four properties hold: no cell has been lost, the original order x1 to x12 is unchanged, exactly one Link is Λ, and the list contains no cycle. Two parts of the algorithm protect these properties.

The first is the assignment Link(New) ← Λ, which protects against a New cell that arrives with a non-null Link, as described in Section 5.3.

The second is the test Temp = New, which protects against New being a cell that is already in the list. Figure 5 shows what would happen without it. If New pointed at x6, line 14 would set Link(x6) to Λ, cutting the list after x6, and line 15 would then set Link(x12) to point at x6. Head would reach only six cells, and x7 to x12 could never be reached or released. If New pointed at x12, the assignment Link(x12) ← x12 would create a cycle, and any later traversal would never end. Both outcomes were confirmed by running a copy of the algorithm with the test removed. With the test in place, the algorithm detects that Temp has reached New and returns false without changing anything.

![Figure 5 — Why the test Temp = New is needed. Without it, inserting a cell that is already in the list would cut the list short and strand the cells after it.](integrity_hazard.png)

## 5.6 Tracing the algorithm

Table 6 traces insertAtEnd on the twelve-cell list, using the addresses from Table 1.

Table: Table 6 — Trace of InsertAtEnd on the twelve-cell list

| Pass | Temp | Temp = New? | Link(Temp) = Λ? | Action |
|---|---|---|---|---|
| 1 | x1 (0x1036f5b70) | No | No | Temp ← x2 |
| 2 | x2 (0x1036f5900) | No | No | Temp ← x3 |
| 3–10 | x3 to x10 | No | No | Temp moves to the next cell |
| 11 | x11 (0x1036f59d0) | No | No | Temp ← x12 |
| 12 | x12 (0x1036f59e0) | No | Yes | Exit loop |
| After loop | x12 (0x1036f59e0) | | | Link(New) ← Λ, then Link(x12) ← 0x1036f59f0 |

Over its twelve passes the loop makes 24 comparisons and moves Temp 11 times, followed by 2 assignments. In general, for a list of n cells the loop makes n passes, 2n comparisons and n − 1 moves, which confirms that the running time grows linearly with the length of the list. These counts were checked by instrumenting a copy of the program for lists of 10, 12 and 16 cells.
