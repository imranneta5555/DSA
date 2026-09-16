# 2 Creating the Linked List

## 2.1 The cell structure

Each cell is defined as a C++ structure with two members:

```cpp
struct Cell {
    int   Info;
    Cell* Link;
};
```

Info is an integer holding the value of the cell. Link is a pointer to another Cell, which means it holds that cell's memory address. Because the structure refers to its own type through Link, cells can be chained together. On the 64-bit system used for this work, one Cell occupies 16 bytes: 4 bytes for Info, 4 bytes of padding added by the compiler so that Link starts on an 8-byte boundary, and 8 bytes for Link. These sizes were measured with `sizeof` and `offsetof` rather than assumed (Appendix B).

The list as a whole is reached through one more pointer, declared as `Cell* Head`. Head is not a cell: it is an 8-byte variable holding the address of the first cell, or Λ when the list is empty.

## 2.2 The list created

The brief requires a list of between 10 and 16 cells. Twelve cells were used, holding the values x1 = 10, x2 = 20 and so on up to x12 = 120, as shown in Figure 1. Twelve was chosen deliberately: after the new cell is inserted the list has thirteen cells, so it stays within the permitted range both before and after the insertion.

![Figure 1 — The twelve-cell list built by createList. Head points to x1, each Link points to the next cell, and the Link of x12 is Λ.](list_of_twelve.png)

## 2.3 The initialisation algorithm

The list is built by the function createList, which receives the twelve values in order and returns the address of the first cell:

```text
Algorithm CreateList(values)
1   Head ← Λ;  Tail ← Λ
2   for each value v in values
3       P ← address of a new cell
4       Info(P) ← v;  Link(P) ← Λ
5       if Head = Λ then Head ← P
6       else Link(Tail) ← P
7       Tail ← P
8   return Head
```

Every new cell is created with its Link already set to Λ (line 4). When the first cell is created, Head is set to point to it (line 5). Each later cell is attached by writing its address into the Link field of the previous last cell, which is tracked by the pointer Tail (line 6). Because a Link stays Λ until the next cell is attached, the list has a valid end at every stage of its construction.

Tail keeps construction to O(n) time. Without it, adding each cell would require a walk from Head to the end of the list, making the construction O(n²) (Cormen et al., 2022).

## 2.4 Validation and error handling

Two safeguards make the initialisation error-free. First, createList checks the number of values before allocating any memory and throws `std::invalid_argument` if it is outside the range 10 to 16, so a list of the wrong size can never be created. Second, if memory allocation fails part-way through, `new` throws `std::bad_alloc`. createList catches the exception, releases every cell already built by calling deleteList, and then passes the exception on. The program therefore never leaves a partly built list or unreleased memory behind.

## 2.5 The list in memory

Table 1 shows the list as it exists in memory, taken from the output of the program. Head holds the address of x1, each Link holds the address of the following cell, and the Link of x12 is Λ.

Table: Table 1 — The twelve-cell list in memory

| Cell | Address | Info | Link |
|---|---|---|---|
| x1 | 0x1036f5b70 | 10 | 0x1036f5900 |
| x2 | 0x1036f5900 | 20 | 0x1036f5910 |
| x3 | 0x1036f5910 | 30 | 0x1036f5960 |
| x4 | 0x1036f5960 | 40 | 0x1036f5970 |
| x5 | 0x1036f5970 | 50 | 0x1036f5980 |
| x6 | 0x1036f5980 | 60 | 0x1036f5990 |
| x7 | 0x1036f5990 | 70 | 0x1036f59a0 |
| x8 | 0x1036f59a0 | 80 | 0x1036f59b0 |
| x9 | 0x1036f59b0 | 90 | 0x1036f59c0 |
| x10 | 0x1036f59c0 | 100 | 0x1036f59d0 |
| x11 | 0x1036f59d0 | 110 | 0x1036f59e0 |
| x12 | 0x1036f59e0 | 120 | Λ |

The addresses are not consecutive. The cell x1 lies in a different region of memory from x2 to x12, and x4 is 80 bytes after x3 rather than 16. This shows the defining property of a linked list: unlike the elements of an array, its cells do not need to be stored next to one another, because each cell records where the next one is (Weiss, 2014). The exact addresses change from one run to the next, because the operating system varies where memory is allocated.
