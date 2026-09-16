# 1 Introduction

A linked list stores a sequence of values in separate cells that are joined by memory addresses rather than by their position in memory. Each cell has two fields: Info, which holds the data, and Link, which holds the address of the next cell. A variable called Head holds the address of the first cell, and the Link of the last cell holds a special null value, written Λ, meaning that no cell follows (Knuth, 1997).

This report addresses the task set in the assignment brief. Given a list pointed to by Head, and a separate cell pointed to by New whose Info field holds the value X(n+1), the algorithm must change the Link field of the last cell of the list so that it points to New. The effect is to insert a new cell at the end of the list.

The work was implemented in C++17. The language was chosen because its raw pointers make every step of the algorithm visible: Head, New and Temp are genuine memory addresses, `nullptr` plays the role of Λ, and cells are created and released explicitly with `new` and `delete` (Stroustrup, 2013).

The report follows the five requirements of the brief. Section 2 creates a list of twelve cells. Section 3 describes the processes and techniques used by the insertion algorithm. Section 4 documents every variable, pointer and command, and Section 5 explains the logic, including its edge cases. Section 6 presents and explains the flowchart. Section 7 summarises the testing and Section 8 concludes. The full source code and program output are given in the appendices.

In the pseudocode, Info(P) and Link(P) mean the Info and Link fields of the cell whose address is held in P, and ← means assignment. In C++ these are written `P->Info`, `P->Link` and `=`.
