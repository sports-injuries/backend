style:
	flake8 backend

types:
	mypy backend

check:
	make -j3 style types
