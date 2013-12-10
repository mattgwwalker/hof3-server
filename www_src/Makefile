DEST=../www
SOURCES=$(wildcard *.m4)
HTML_TARGETS=$(patsubst %.m4,$(DEST)/%.html,$(SOURCES))


.PHONY: all
all: copy_only $(HTML_TARGETS)

.PHONY: copy_only
copy_only: clean
	ln -sr images $(DEST)
	ln -sr css $(DEST)
	ln -sr js $(DEST)
	ln -sr js_src $(DEST) # This needs to be replaced with just a single, minimized file.
	echo "The contents of this directory are generated automatically by running the makefile in ../www_src." > $(DEST)/README 


$(HTML_TARGETS) : $(DEST)/%.html : %.m4
	m4 $< > $@

.PHONY: clean
clean:
	rm -r $(DEST) 
	mkdir $(DEST)
