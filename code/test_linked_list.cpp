// test_linked_list.cpp
// Dependency-free tests for list creation and insertAtEnd.

#include "linked_list.hpp"

#include <cstddef>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

int checksRun = 0;
int checksFailed = 0;

#define CHECK(condition)                                                        \
    do {                                                                        \
        ++checksRun;                                                            \
        if (!(condition)) {                                                     \
            ++checksFailed;                                                     \
            std::cerr << "    FAILED line " << __LINE__ << ": " #condition "\n"; \
        }                                                                       \
    } while (false)

std::vector<int> tensUpTo(int count) {
    std::vector<int> values;
    for (int i = 1; i <= count; ++i) {
        values.push_back(i * 10);
    }
    return values;
}

std::vector<int> infoValues(const Cell* Head) {
    std::vector<int> values;
    for (const Cell* Temp = Head; Temp != nullptr; Temp = Temp->Link) {
        values.push_back(Temp->Info);
    }
    return values;
}

Cell* lastCell(Cell* Head) {
    Cell* Temp = Head;
    while (Temp != nullptr && Temp->Link != nullptr) {
        Temp = Temp->Link;
    }
    return Temp;
}

Cell* cellAt(Cell* Head, std::size_t index) {
    Cell* Temp = Head;
    for (std::size_t i = 0; i < index && Temp != nullptr; ++i) {
        Temp = Temp->Link;
    }
    return Temp;
}

bool contains(const Cell* Head, const Cell* cell) {
    for (const Cell* Temp = Head; Temp != nullptr; Temp = Temp->Link) {
        if (Temp == cell) {
            return true;
        }
    }
    return false;
}

// Floyd's two-pointer check: a list with a cycle never reaches Λ, so a fast
// pointer eventually meets a slow one.
bool hasCycle(const Cell* Head) {
    const Cell* slow = Head;
    const Cell* fast = Head;
    while (fast != nullptr && fast->Link != nullptr) {
        slow = slow->Link;
        fast = fast->Link->Link;
        if (slow == fast) {
            return true;
        }
    }
    return false;
}

// ---------------------------------------------------------------- creation

void createList_buildsTwelveCellsInOrder() {
    Cell* Head = createList(tensUpTo(12));
    CHECK(Head != nullptr);
    CHECK(countCells(Head) == 12);
    CHECK(infoValues(Head) == tensUpTo(12));
    CHECK(Head->Info == 10);
    deleteList(Head);
}

void createList_nullTerminatesTheLastCell() {
    Cell* Head = createList(tensUpTo(12));
    Cell* last = lastCell(Head);
    CHECK(last != nullptr);
    CHECK(last->Info == 120);
    CHECK(last->Link == nullptr);
    CHECK(!hasCycle(Head));
    deleteList(Head);
}

void createList_acceptsTheBoundarySizes() {
    Cell* ten = createList(tensUpTo(10));
    Cell* sixteen = createList(tensUpTo(16));
    CHECK(countCells(ten) == 10);
    CHECK(countCells(sixteen) == 16);
    deleteList(ten);
    deleteList(sixteen);
}

void createList_rejectsSizesOutsideTenToSixteen() {
    for (int size : {0, 9, 17}) {
        bool threw = false;
        try {
            Cell* Head = createList(tensUpTo(size));
            deleteList(Head);
        } catch (const std::invalid_argument&) {
            threw = true;
        }
        CHECK(threw);
    }
}

// ------------------------------------------------------------- insertAtEnd

void insertAtEnd_appendsToTheTwelveCellList() {
    Cell* Head = createList(tensUpTo(12));
    const Cell* originalHead = Head;
    Cell* New = createCell(130);

    CHECK(insertAtEnd(Head, New));
    CHECK(!hasCycle(Head));                 // checked first: safe on any list
    if (hasCycle(Head)) {
        return;
    }
    CHECK(Head == originalHead);           // Head is unchanged
    CHECK(countCells(Head) == 13);
    CHECK(lastCell(Head) == New);           // New is now the last cell
    CHECK(New->Link == nullptr);            // and is null-terminated
    const Cell* oldLast = cellAt(Head, 11);  // x12, the old last cell
    CHECK(oldLast != nullptr && oldLast->Link == New);
    CHECK(infoValues(Head) == tensUpTo(13)); // order preserved
    deleteList(Head);
}

void insertAtEnd_intoAnEmptyListMakesNewTheHead() {
    Cell* Head = nullptr;
    Cell* New = createCell(130);

    CHECK(insertAtEnd(Head, New));
    CHECK(Head == New);
    CHECK(countCells(Head) == 1);
    CHECK(Head != nullptr && Head->Link == nullptr);
    if (Head != New) {
        delete New;  // not taken into the list
    }
    deleteList(Head);
}

void insertAtEnd_intoASingleCellList() {
    Cell* Head = createCell(10);
    Cell* New = createCell(20);

    CHECK(insertAtEnd(Head, New));
    CHECK(Head->Link == New);
    CHECK(New->Link == nullptr);
    CHECK(countCells(Head) == 2);
    deleteList(Head);
}

void insertAtEnd_rejectsANullNew() {
    Cell* Head = createList(tensUpTo(12));

    CHECK(!insertAtEnd(Head, nullptr));
    CHECK(countCells(Head) == 12);
    CHECK(lastCell(Head)->Link == nullptr);
    deleteList(Head);

    Cell* empty = nullptr;
    CHECK(!insertAtEnd(empty, nullptr));
    CHECK(empty == nullptr);
}

void insertAtEnd_clearsALinkThatNewArrivesWith() {
    Cell* Head = createList(tensUpTo(12));
    Cell* stray = createCell(999);
    Cell* New = createCell(130);
    New->Link = stray;  // New arrives pointing at an unrelated cell

    CHECK(insertAtEnd(Head, New));
    CHECK(New->Link == nullptr);  // the stray cell is not pulled into the list
    const bool strayAbsorbed = contains(Head, stray);
    CHECK(!strayAbsorbed);
    CHECK(countCells(Head) == 13);
    CHECK(infoValues(Head) == tensUpTo(13));
    deleteList(Head);
    if (!strayAbsorbed) {
        delete stray;  // still owned by the caller
    }
}

void insertAtEnd_refusesACellAlreadyInTheList() {
    for (std::size_t index : {std::size_t{0}, std::size_t{5}, std::size_t{11}}) {
        Cell* Head = createList(tensUpTo(12));
        Cell* existing = cellAt(Head, index);

        CHECK(!insertAtEnd(Head, existing));  // head, middle and last cell

        // A cyclic list can't be counted or freed safely, so check that first.
        const bool cyclic = hasCycle(Head);
        CHECK(!cyclic);
        if (cyclic) {
            continue;
        }
        CHECK(countCells(Head) == 12);
        CHECK(infoValues(Head) == tensUpTo(12));
        deleteList(Head);
    }
}

void insertAtEnd_repeatedInsertionsKeepTheListValid() {
    Cell* Head = createList(tensUpTo(10));
    for (int value = 110; value <= 160; value += 10) {
        CHECK(insertAtEnd(Head, createCell(value)));
    }
    CHECK(countCells(Head) == 16);
    CHECK(infoValues(Head) == tensUpTo(16));
    CHECK(lastCell(Head)->Link == nullptr);
    CHECK(!hasCycle(Head));
    deleteList(Head);
}

// -------------------------------------------------------------- deleteList

void deleteList_releasesCellsAndClearsHead() {
    Cell* Head = createList(tensUpTo(12));
    deleteList(Head);
    CHECK(Head == nullptr);

    Cell* empty = nullptr;
    deleteList(empty);  // deleting an empty list is safe
    CHECK(empty == nullptr);
}

}  // namespace

int main() {
    const std::vector<std::pair<std::string, std::function<void()>>> tests = {
        {"createList builds twelve cells in order", createList_buildsTwelveCellsInOrder},
        {"createList null-terminates the last cell", createList_nullTerminatesTheLastCell},
        {"createList accepts the boundary sizes 10 and 16", createList_acceptsTheBoundarySizes},
        {"createList rejects sizes outside 10-16", createList_rejectsSizesOutsideTenToSixteen},
        {"insertAtEnd appends to the twelve-cell list", insertAtEnd_appendsToTheTwelveCellList},
        {"insertAtEnd into an empty list makes New the Head", insertAtEnd_intoAnEmptyListMakesNewTheHead},
        {"insertAtEnd into a single-cell list", insertAtEnd_intoASingleCellList},
        {"insertAtEnd rejects a null New", insertAtEnd_rejectsANullNew},
        {"insertAtEnd clears a Link that New arrives with", insertAtEnd_clearsALinkThatNewArrivesWith},
        {"insertAtEnd refuses a cell already in the list", insertAtEnd_refusesACellAlreadyInTheList},
        {"insertAtEnd repeated insertions keep the list valid", insertAtEnd_repeatedInsertionsKeepTheListValid},
        {"deleteList releases cells and clears Head", deleteList_releasesCellsAndClearsHead},
    };

    int testsFailed = 0;
    for (const auto& [name, test] : tests) {
        const int failedBefore = checksFailed;
        test();
        const bool passed = checksFailed == failedBefore;
        std::cout << (passed ? "  PASS  " : "  FAIL  ") << name << '\n';
        if (!passed) {
            ++testsFailed;
        }
    }

    std::cout << '\n'
              << tests.size() - static_cast<std::size_t>(testsFailed) << " of " << tests.size()
              << " tests passed (" << checksRun - checksFailed << " of " << checksRun
              << " checks)\n";
    return testsFailed == 0 ? 0 : 1;
}
