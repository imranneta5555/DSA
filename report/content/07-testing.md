# 7 Implementation and Testing

The program was compiled with Apple Clang 21 using the C++17 standard and strict warning settings, under which any compiler warning stops the build. Twelve automated tests, containing 63 individual checks, covered list creation, every edge case in Table 5 and repeated insertion. All of the tests passed, as Table 8 shows.

Table: Table 8 — Test results

| Test | Result |
|---|---|
| Creates twelve cells in order | Pass |
| Null-terminates the last cell | Pass |
| Accepts the boundary sizes 10 and 16 | Pass |
| Rejects sizes outside 10 to 16 | Pass |
| Appends a cell to the twelve-cell list | Pass |
| Empty list: New becomes the Head | Pass |
| Inserts into a single-cell list | Pass |
| Rejects a null New | Pass |
| Clears a Link that New arrives with | Pass |
| Refuses a cell already in the list | Pass |
| Repeated insertions keep the list valid | Pass |
| deleteList releases the cells and clears Head | Pass |

Three further checks gave confidence beyond the tests themselves. The tests were run under AddressSanitizer and UndefinedBehaviorSanitizer, which detect invalid memory access and undefined behaviour, and no errors were reported. The macOS leaks tool confirmed that both the tests and the demonstration program finished with no leaked memory, so every cell created with `new` was released with `delete`. Finally, the tests themselves were checked by deliberately introducing seven faults into the algorithm, such as removing the assignment Link(New) ← Λ or re-linking from Head instead of Temp. Six faults were reported as failing tests, and the seventh, removing the check on New, caused an immediate crash, so every fault was detected.
