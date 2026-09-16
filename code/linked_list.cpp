// linked_list.cpp
// Implementation of the Info-Link linked list and the insert-at-end algorithm.

#include "linked_list.hpp"

#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

namespace {

// Formats a pointer for display, showing nullptr as the brief's Λ.
std::string addressOf(const Cell* cell) {
    if (cell == nullptr) {
        return "Λ";
    }
    std::ostringstream text;
    text << static_cast<const void*>(cell);
    return text.str();
}

}  // namespace

Cell* createCell(int info) {
    return new Cell{info, nullptr};
}

Cell* createList(const std::vector<int>& values) {
    if (values.size() < MIN_CELLS || values.size() > MAX_CELLS) {
        throw std::invalid_argument(
            "a list must have between " + std::to_string(MIN_CELLS) + " and " +
            std::to_string(MAX_CELLS) + " cells, but " +
            std::to_string(values.size()) + " values were given");
    }

    Cell* Head = nullptr;  // address of the first cell
    Cell* Tail = nullptr;  // address of the last cell built so far

    try {
        for (int value : values) {
            Cell* cell = createCell(value);  // new cell, Link already nullptr
            if (Head == nullptr) {
                Head = cell;                 // first cell: Head points to it
            } else {
                Tail->Link = cell;           // previous last cell points to it
            }
            Tail = cell;                     // it is now the last cell
        }
    } catch (...) {
        deleteList(Head);                    // allocation failed part-way:
        throw;                               // release what was built, re-throw
    }

    return Head;
}

bool insertAtEnd(Cell*& Head, Cell* New) {
    // Process 1: there must be a cell to insert.
    if (New == nullptr) {
        return false;
    }

    // Process 2: an empty list has no last cell, so New becomes the whole list.
    if (Head == nullptr) {
        New->Link = nullptr;
        Head = New;
        return true;
    }

    // Process 3: traverse from Head until Temp points to the last cell.
    Cell* Temp = Head;
    while (true) {
        if (Temp == New) {
            return false;       // New is already in this list. Re-linking it
        }                       // would cut the list short and strand the
                                // cells after it, or loop the last cell back
                                // onto itself, so refuse.
        if (Temp->Link == nullptr) {
            break;              // Temp's Link is Λ: Temp is the last cell
        }
        Temp = Temp->Link;      // move Temp on to the next cell
    }

    // Process 4: re-link. New is made a proper terminal cell first, and only
    // then attached, so the list is never left pointing into foreign cells.
    New->Link = nullptr;
    Temp->Link = New;           // the old Λ is replaced by the address of New
    return true;
}

std::size_t countCells(const Cell* Head) {
    std::size_t count = 0;
    for (const Cell* Temp = Head; Temp != nullptr; Temp = Temp->Link) {
        ++count;
    }
    return count;
}

void printList(std::ostream& out, const Cell* Head) {
    out << "Head";
    for (const Cell* Temp = Head; Temp != nullptr; Temp = Temp->Link) {
        out << " -> [" << Temp->Info << '|' << (Temp->Link == nullptr ? "Λ" : "o") << ']';
    }
    if (Head == nullptr) {
        out << " -> Λ";
    }
    out << '\n';
}

void printMemoryTable(std::ostream& out, const Cell* Head) {
    const std::ios_base::fmtflags savedFlags = out.flags();  // restore on exit
    out << std::left
        << "  " << std::setw(6) << "Cell" << std::setw(20) << "Address"
        << std::setw(8) << "Info" << "Link\n";

    std::size_t position = 1;
    for (const Cell* Temp = Head; Temp != nullptr; Temp = Temp->Link) {
        out << "  " << std::setw(6) << ("x" + std::to_string(position))
            << std::setw(20) << addressOf(Temp)
            << std::setw(8) << Temp->Info
            << addressOf(Temp->Link) << '\n';
        ++position;
    }
    out.flags(savedFlags);
}

void deleteList(Cell*& Head) {
    while (Head != nullptr) {
        Cell* next = Head->Link;  // remember the rest of the list first
        delete Head;              // then release this cell
        Head = next;
    }
}
