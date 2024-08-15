FILE=main.py
TESTFILE=analyze.py
all:
	clear
	python3 $(FILE)
test:
	clear
	python3 $(TESTFILE)
