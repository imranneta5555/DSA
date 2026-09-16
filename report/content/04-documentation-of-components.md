# 4 Documentation of Components

## 4.1 Where the data is stored

The program uses two regions of memory, shown in Figure 3. The pointer variables Head, New and Temp are local variables with automatic storage, held on the stack. Each occupies 8 bytes and contains nothing but an address. The cells are created with `new` and have dynamic storage on the heap, also called the free store, where they remain until they are released with `delete` (Stroustrup, 2013). A pointer on the stack gives access to a cell on the heap, and the Link inside that cell gives access to the next one.

![Figure 3 — Memory during the final step of the insertion, using addresses from the program run. The pointers are on the stack; the cells are on the heap. The Link of x12 now holds 0x1036f59f0, the address of New.](memory_model.png)

## 4.2 Variables and pointers

Table 3 documents every variable and pointer used, the type it has in C++, where it is stored in memory and the part it plays in the algorithm.

Table: Table 3 — Variables and pointers

| Name | C++ type | Stored in | Role |
|---|---|---|---|
| Head | `Cell*`, received by insertAtEnd as `Cell*&` | Stack | Holds the address of the first cell, or Λ when the list is empty. insertAtEnd receives it by reference so that it can change the caller's Head when the list is empty. |
| New | `Cell*` | Stack | Holds the address of the cell to be inserted. The algorithm reads and writes that cell through New but never changes New itself. |
| Temp | `Cell*` | Stack | The traversal pointer. It starts with the value of Head and moves one cell at a time until it holds the address of the last cell. |
| Tail | `Cell*` | Stack | Used only in createList, to hold the address of the most recently created cell. |
| P, called `cell` in C++ | `Cell*` | Stack | In createList, holds the address of the cell just allocated until it is linked in. |
| v, called `value` in C++; `info` | `int` | Stack | The value for the cell being created. createList passes it to createCell, which stores it in Info. |
| next | `Cell*` | Stack | In deleteList, saves Link(Head) before that cell is deleted, so the rest of the list stays reachable. |
| Info | `int`, 4 bytes | Heap, offset 0 in each cell | The data value of a cell. The insertion never reads or changes it. |
| Link | `Cell*`, 8 bytes | Heap, offset 8 in each cell | The address of the next cell, or Λ. It is the only field the insertion changes. |
| Λ | `nullptr` | Not stored separately | The null pointer, meaning "no cell". It marks the end of a list and an empty list. |
| MIN_CELLS, MAX_CELLS | `constexpr std::size_t` | Fixed when compiled | The limits 10 and 16 from the brief, checked by createList. |
| values | `const std::vector<int>&` | Stack, as a reference | The Info values passed to createList by reference, so they are not copied. |

## 4.3 Instructions and commands

Table 4 documents every instruction and command used in the implementation, with its meaning and its effect on memory.

Table: Table 4 — Instructions and commands

| Instruction | Meaning | Effect on memory |
|---|---|---|
| `struct Cell { ... };` | Declares the cell type | Defines the 16-byte layout of every cell but allocates nothing |
| `new Cell{info, nullptr}` | Creates a cell | Allocates 16 bytes on the heap, stores Info and a null Link, and returns the address |
| `delete P` | Destroys the cell at address P | Returns the 16 bytes to the heap. P still holds the old address, so it must not be used afterwards |
| `P->Info`, `P->Link` | Access to a field through a pointer | Reads or writes a field of the cell at address P; written Info(P) and Link(P) in the pseudocode |
| `=` | Assignment, written ← in the pseudocode | Copies a value or an address into a variable or field |
| `==`, `!=` | Comparison | Compares two addresses without changing memory |
| `if`, `else` | Selection | Chooses which statements run; createList uses `else` to link every cell after the first |
| `while (true)` with `break` | A loop whose exit test is inside it | Repeats the traversal; `break` leaves the loop once the last cell is found |
| `while (Head != nullptr)` | A loop tested before each pass | deleteList repeats it until every cell has been released |
| `for (int value : values)` | Range-based loop | Visits each value once, so createList allocates exactly one cell per value |
| `sizeof`, `offsetof` | Size and position operators, fixed when compiled | Measure the 16-byte cell and the offsets of Info (0) and Link (8) |
| `return false`, `return true` | Ends the function with a result | Reports whether New was inserted |
| `Cell*&` | Reference to a pointer | Lets insertAtEnd assign directly to the caller's Head variable |
| `throw`, `try`, `catch` | Exception handling | Used by createList to reject a wrong size and to release cells if allocation fails |

## 4.4 How the components work together

The insertion writes to memory in only two places: the Link field of New, which is set to Λ, and the Link field of the last cell, which changes from Λ to the address of New. In the program run shown in Figure 3, Temp holds 0x1036f59e0, the address of x12, and the Link field of x12 changes from Λ to 0x1036f59f0, the address held in New. insertAtEnd itself creates, moves and deletes no cells. Creating New is the responsibility of the calling code, and releasing every cell afterwards is the responsibility of deleteList, which saves the address in each cell's Link before deleting that cell, so that the rest of the list is not lost.
