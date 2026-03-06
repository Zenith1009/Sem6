# Distributed Computing
## Assignment 6

Develop a simple RMI-based server (`CatServer`) that allows a client to read a text file line-by-line.

The server must provide the following methods:

1. `public boolean openFile(String filename)`
	- Opens a file.
	- Returns `true` if file is opened successfully, else `false`.

2. `public String nextLine()`
	- Reads and returns the next line from the currently opened file.
	- Returns `null` if end-of-file is reached or if no file has been opened.

3. `public boolean closeFile()`
	- Closes the currently opened file.
	- Returns `true` if closed successfully, else `false`.

Develop a client (`CatClient`) that connects to the server, requests file opening, and reads it line-by-line using `nextLine()`.