all: notepad.cpp
	g++ -std=c++17 notepad.cpp -o notepad -no-pie

debug: notepad.cpp
	g++ -std=c++17 notepad.cpp -o notepad -no-pie -fsanitize=address -fno-omit-frame-pointer

poc: poc.cpp
	g++ -std=c++17 poc.cpp -o poc -no-pie

clean: 
	rm notepad poc
