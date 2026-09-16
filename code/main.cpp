// main.cpp
// Demonstrates the assignment: builds a 12-cell list, inserts a 13th cell at
// the end with insertAtEnd, and prints the list and its memory before and after.

#include "linked_list.hpp"

#include <cstddef>
#include <iostream>
#include <vector>

int main() {
    // Info values x1..x12 = 10, 20, ..., 120.
    std::vector<int> values;
    for (int i = 1; i <= 12; ++i) {
        values.push_back(i * 10);
    }

    std::cout << "Cell layout in memory\n"
              << "  sizeof(Cell)         = " << sizeof(Cell) << " bytes\n"
              << "  sizeof(Cell*)        = " << sizeof(Cell*) << " bytes\n"
              << "  offsetof(Cell, Info) = " << offsetof(Cell, Info) << "\n"
              << "  offsetof(Cell, Link) = " << offsetof(Cell, Link) << "\n\n";

    Cell* Head = createList(values);
    std::cout << "Step 1: list created with " << countCells(Head) << " cells\n";
    printList(std::cout, Head);
    printMemoryTable(std::cout, Head);

    Cell* New = createCell(130);  // x13
    std::cout << "\nStep 2: New cell allocated at " << static_cast<const void*>(New)
              << " with Info = " << New->Info << " and Link = Λ\n";

    const bool inserted = insertAtEnd(Head, New);
    if (!inserted) {
        delete New;  // not taken into the list, so it is still ours to free
    }
    std::cout << "\nStep 3: insertAtEnd returned " << (inserted ? "true" : "false")
              << "; the list now has " << countCells(Head) << " cells\n";
    printList(std::cout, Head);
    printMemoryTable(std::cout, Head);

    deleteList(Head);
    std::cout << "\nStep 4: list deleted; Head is " << (Head == nullptr ? "Λ" : "not null")
              << '\n';
    return 0;
}
