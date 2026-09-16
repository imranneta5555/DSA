# 6 Flowchart and Explanation

## 6.1 The flowchart

![Figure 6 — Flowchart of the InsertAtEnd algorithm. The main path runs down the centre, the cases that end early branch to the right, and the traversal loop returns along the left to the junction point above S9.](flowchart.png)

Figure 6 presents the insertion algorithm as a flowchart drawn with the symbols defined in ISO 5807 (International Organization for Standardization, 1985). Rounded terminals mark the start and each possible end; rectangles are processes, here assignments; diamonds are decisions, each with a Yes and a No exit; and arrowed flow lines show the order of execution. A filled junction point marks where the loop returns. Every symbol is labelled S1 to S15 so that it can be matched to the pseudocode and the C++ code in Table 7.

## 6.2 Explanation of each step

The flowchart reads from top to bottom along its main path, with side branches for the cases that finish early.

S1 is the start, with the two inputs Head and New. Decision S2 checks whether New is Λ; if it is, terminal S3 ends the algorithm with false. Decision S4 checks for an empty list. Its Yes branch runs down the right-hand side: S5 clears Link(New), S6 sets Head to point to New, and S7 ends with true.

On the main path, S8 sets Temp to Head and the flow reaches the junction point. The loop is made up of S9, S11 and S12. Decision S9 checks whether Temp has reached New, and ends at S10 with false if it has. Decision S11 checks whether Temp is on the last cell. If it is not, the No branch leads to S12, which moves Temp to the next cell, and the flow line returns along the left-hand side to the junction and back into S9. The loop appears as a closed path because it is the only part of the algorithm that repeats.

When the answer at S11 is Yes, the loop is finished. S13 clears Link(New), S14 performs the re-link that completes the insertion, and S15 ends with true.

## 6.3 From flowchart to code

Table 7 shows how each flowchart symbol corresponds to a line of pseudocode and a statement in the C++ function.

Table: Table 7 — Flowchart, pseudocode and C++ correspondence

| Step | Symbol | Pseudocode line | C++ statement |
|---|---|---|---|
| S1 | Terminal | InsertAtEnd(Head, New) | `bool insertAtEnd(Cell*& Head, Cell* New)` |
| S2 | Decision | 1: if New = Λ | `if (New == nullptr)` |
| S3 | Terminal | 2: return false | `return false;` |
| S4 | Decision | 3: if Head = Λ | `if (Head == nullptr)` |
| S5 | Process | 4: Link(New) ← Λ | `New->Link = nullptr;` |
| S6 | Process | 5: Head ← New | `Head = New;` |
| S7 | Terminal | 6: return true | `return true;` |
| S8 | Process | 7: Temp ← Head | `Cell* Temp = Head;` |
| Junction | Connector | 8: loop | `while (true) {` |
| S9 | Decision | 9: if Temp = New | `if (Temp == New)` |
| S10 | Terminal | 10: return false | `return false;` |
| S11 | Decision | 11–12: if Link(Temp) = Λ, exit loop | `if (Temp->Link == nullptr) { break; }` |
| S12 | Process | 13: Temp ← Link(Temp) | `Temp = Temp->Link;` |
| S13 | Process | 14: Link(New) ← Λ | `New->Link = nullptr;` |
| S14 | Process | 15: Link(Temp) ← New | `Temp->Link = New;` |
| S15 | Terminal | 16: return true | `return true;` |

Every symbol in the flowchart corresponds to one line of pseudocode and one statement of C++, and every statement in the function appears in the flowchart. The diagram is therefore a complete and exact picture of the algorithm as implemented, rather than a simplified outline of it.
