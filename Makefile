#
# Just a dummy Makefile, albeit working ;)
#

default:
	@echo 'This is just a dummy (but working) Makefile.'
	@echo 'It could be used as an input file for the makefile2dot visualizer'
	@echo 'Type "make all" to generate example output.png' 

ALL := output.dot output.png

all: output.png

output.png: output.dot
	dot -Tpng < $< > $@

output.dot: Makefile makefile2dot.py
	./makefile2dot.py < $< >$@


clean:
	rm -f $(ALL)
