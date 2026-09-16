# Builds and checks the Unit 3 linked-list code.
#   make run       build and run the demonstration
#   make test      build and run the tests
#   make sanitize  rerun both under AddressSanitizer and UndefinedBehaviorSanitizer
#   make leaks     check both for memory leaks with the macOS leaks tool
#   make check     all of the above

CXX      := clang++
CXXFLAGS := -std=c++17 -Wall -Wextra -Werror -pedantic -g
SANFLAGS := -fsanitize=address,undefined -fno-omit-frame-pointer
BUILD    := build
LIB      := linked_list.cpp linked_list.hpp

.PHONY: all run test sanitize leaks check clean

all: $(BUILD)/demo $(BUILD)/tests

$(BUILD):
	mkdir -p $@

$(BUILD)/demo: main.cpp $(LIB) | $(BUILD)
	$(CXX) $(CXXFLAGS) main.cpp linked_list.cpp -o $@

$(BUILD)/tests: test_linked_list.cpp $(LIB) | $(BUILD)
	$(CXX) $(CXXFLAGS) test_linked_list.cpp linked_list.cpp -o $@

$(BUILD)/demo-san: main.cpp $(LIB) | $(BUILD)
	$(CXX) $(CXXFLAGS) $(SANFLAGS) main.cpp linked_list.cpp -o $@

$(BUILD)/tests-san: test_linked_list.cpp $(LIB) | $(BUILD)
	$(CXX) $(CXXFLAGS) $(SANFLAGS) test_linked_list.cpp linked_list.cpp -o $@

run: $(BUILD)/demo
	./$(BUILD)/demo

test: $(BUILD)/tests
	./$(BUILD)/tests

sanitize: $(BUILD)/demo-san $(BUILD)/tests-san
	./$(BUILD)/tests-san
	./$(BUILD)/demo-san > /dev/null
	@echo "sanitizers: no errors reported"

leaks: $(BUILD)/demo $(BUILD)/tests
	leaks --atExit -- ./$(BUILD)/tests > $(BUILD)/leaks-tests.txt 2>&1 || (cat $(BUILD)/leaks-tests.txt; exit 1)
	leaks --atExit -- ./$(BUILD)/demo > $(BUILD)/leaks-demo.txt 2>&1 || (cat $(BUILD)/leaks-demo.txt; exit 1)
	@grep -h "leaks for" $(BUILD)/leaks-tests.txt $(BUILD)/leaks-demo.txt

check: test sanitize leaks

clean:
	rm -rf $(BUILD)
