// linked_list.hpp
// A singly linked list of Info-Link cells, following the notation of the
// Unit 3 assignment brief: Head points to the first cell, each cell's Link
// points to the next cell, and the last cell's Link is Λ (nullptr in C++).

#ifndef LINKED_LIST_HPP
#define LINKED_LIST_HPP

#include <cstddef>
#include <ostream>
#include <vector>

// The brief requires the list to be created with between 10 and 16 cells.
constexpr std::size_t MIN_CELLS = 10;
constexpr std::size_t MAX_CELLS = 16;

// One cell of the list. Info holds the data value; Link holds the address of
// the next cell, or nullptr when this cell is the last one.
struct Cell {
    int   Info;
    Cell* Link;
};

// Allocates one cell on the heap holding `info`, with its Link set to nullptr.
Cell* createCell(int info);

// Builds a list whose cells hold `values` in order and returns its Head.
// Throws std::invalid_argument unless values has MIN_CELLS..MAX_CELLS items.
Cell* createList(const std::vector<int>& values);

// Inserts the cell pointed to by New at the end of the list pointed to by Head.
// Head is passed by reference so an empty list can be given its first cell.
// Returns false and leaves the list untouched if New is null or already in it.
bool insertAtEnd(Cell*& Head, Cell* New);

// Counts the cells reachable from Head.
std::size_t countCells(const Cell* Head);

// Prints the list on one line, e.g. "Head -> [10|o] -> ... -> [120|Λ]".
void printList(std::ostream& out, const Cell* Head);

// Prints one row per cell: position, address, Info and Link.
void printMemoryTable(std::ostream& out, const Cell* Head);

// Releases every cell in the list and sets Head to nullptr.
void deleteList(Cell*& Head);

#endif  // LINKED_LIST_HPP
