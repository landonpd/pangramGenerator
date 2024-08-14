FILE=main.py
TESTFILE=test.py
all:
	clear
	python3 $(FILE)
test:
	clear
	python3 $(TESTFILE)
