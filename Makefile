test: test-python test-vim test-nvim

test-python:
	PYTHONPATH=python3 python3 python3/emmet/element_test.py
	PYTHONPATH=python3 python3 python3/emmet/parser_test.py

test-vim: deps
	vim -u test/vimrc -c 'Vader! test/*.vader'

test-nvim: deps
	VADER_OUTPUT_FILE=/dev/stderr nvim -u test/vimrc -c 'Vader! test/*.vader' --headless

clean:
	rm -rf pack

deps:
	test -L pack/testing/start/vim-emmet-ultisnips && exit 0; \
	mkdir -p pack/testing/start; \
	cd pack/testing/start; \
	git clone https://github.com/junegunn/vader.vim.git; \
	git clone https://github.com/SirVer/ultisnips.git; \
	ln -s ../../.. vim-emmet-ultisnips
