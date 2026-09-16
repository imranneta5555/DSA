# 3 The Insertion Algorithm: Processes and Techniques

## 3.1 The algorithm

The complete algorithm, written in the notation of the brief, is:

```text
Algorithm InsertAtEnd(Head, New)
1   if New = Λ then
2       return false
3   if Head = Λ then
4       Link(New) ← Λ
5       Head ← New
6       return true
7   Temp ← Head
8   loop
9       if Temp = New then
10          return false
11      if Link(Temp) = Λ then
12          exit loop
13      Temp ← Link(Temp)
14  Link(New) ← Λ
15  Link(Temp) ← New
16  return true
```

The algorithm returns true if the cell was inserted and false if it was refused, so that the calling code knows whether New now belongs to the list. It consists of four processes, described below and illustrated in Figure 2.

## 3.2 Process 1: validating New (lines 1–2)

The algorithm first checks that there is a cell to insert. If New is Λ it holds no address, and any attempt to write to Link(New) would access invalid memory. The algorithm returns false and leaves the list unchanged.

## 3.3 Process 2: handling an empty list (lines 3–6)

If Head is Λ, the list has no cells, so there is no last cell whose Link can be changed. In this case New becomes the whole list: its Link is set to Λ and Head is set to point to it. This is the only situation in which Head itself changes, which is why the C++ function receives Head by reference (Section 4.2).

## 3.4 Process 3: finding the last cell (lines 7–13)

The last cell cannot be reached directly, because the list only records the address of its first cell. It has to be found by traversal. A pointer called Temp starts at the first cell (line 7). On each pass through the loop the algorithm tests whether Link(Temp) is Λ (line 11). If it is not, Temp is moved forward by copying into it the address held in its own cell's Link field (line 13). When Link(Temp) is Λ, Temp is on the last cell and the loop ends (line 12).

This technique is a linear traversal, a form of sequential search: each cell is visited once, in order, until one that satisfies the condition is found (Levitin, 2012). Repeatedly replacing a pointer with the Link of the cell it points to is known as following, or chasing, pointers. On the twelve-cell list the loop makes twelve passes and moves Temp eleven times.

The loop also makes a second test (line 9): whether Temp has reached New itself. This detects the case where New is already part of the list, which is explained in Section 5.5.

## 3.5 Process 4: re-linking (lines 14–16)

Once Temp points to the last cell, two assignments complete the insertion. Line 14 sets Link(New) to Λ, so that New is a valid last cell. Line 15 then overwrites the Λ in Link(Temp) with the address of New. At that moment New becomes reachable from Head and the list has grown by one cell. No data is moved or copied: the whole insertion is achieved by changing a single address, which is the main advantage of linked allocation over sequential storage (Knuth, 1997). The order of the two assignments matters, as Section 5.3 explains.

![Figure 2 — The four stages of insertAtEnd on the twelve-cell list: (a) Temp starts at Head; (b) Temp moves from cell to cell; (c) the loop stops at x12, whose Link is Λ; (d) the Λ in x12 is replaced by the address of New.](insertion_steps.png)

## 3.6 Justification of the approach

The chosen algorithm is iterative, uses one extra pointer and works on the list exactly as the brief defines it, with only a Head pointer. Table 2 compares it with the alternatives that were considered.

Table: Table 2 — Alternative techniques considered

| Technique | Time | Reason it was not chosen |
|---|---|---|
| Keep a Tail pointer with the list | O(1) | Fastest, but the list in the brief records only Head. Every operation that changes the list would also have to keep Tail correct, adding a second pointer that could fall out of step with the list. |
| Recursive traversal | O(n) | Each cell adds a function call to the stack, so memory use grows with the list and a very long list could overflow the stack. The loop needs only one pointer. |
| Dummy head (sentinel) cell | O(n) | Removes the empty-list special case, but changes the structure given in the brief, where Head points to the first data cell (Cormen et al., 2022). |
| `std::list` from the C++ library | O(1) | Correct and efficient, but it hides the pointer manipulation that the task asks to be shown and explained. |
| `std::unique_ptr` for Link | O(n) | Releases memory automatically, but each re-link becomes a transfer of ownership, and destroying a long chain releases its cells recursively. |

The iterative traversal runs in O(n) time, because each of the n cells is visited once, and needs O(1) extra space, because only Temp is added however long the list becomes (Sedgewick and Wayne, 2011). For a list of 10 to 16 cells the difference between O(n) and O(1) is negligible, while keeping to the structure in the brief makes the algorithm simpler to verify.
