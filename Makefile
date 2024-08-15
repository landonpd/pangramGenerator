FILE=main.py
TESTFILE=test.py
ANALYZEFILE=analyze.py
all:
	clear
	python3 $(FILE)
test:
	clear
	python3 $(TESTFILE)
analyze:
	clear
	python3 $(ANALYZEFILE)
