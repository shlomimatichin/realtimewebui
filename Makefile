all: check_convention

check_convention:
	pep8 . --max-line-length=109
