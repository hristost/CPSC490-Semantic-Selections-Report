all: main.pdf

aux/main.tex: main.md meta.yaml swift.xml
	mkdir -p aux
	pandoc \
		--template template.tex \
	    -s -F pandoc-crossref --biblatex meta.yaml -N \
		--syntax-definition swift.xml \
		-f markdown -t latex+raw_tex -o $@ main.md

TARGETS = aux/main.pdf
DEPS_DIR = .deps
LATEXMK = latexmk \
      -recorder \
      -output-directory="./aux" \
      -use-make \
      -deps \
      -e 'warn qq(In Makefile, turn off custom dependencies\n);' \
      -e '@cus_dep_list = ();' \
      -e 'show_cus_dep();'
      
$(foreach file,$(TARGETS),$(eval -include $(DEPS_DIR)/$(file)P))
$(DEPS_DIR) :
	mkdir $@

       
%.pdf : %.tex
	echo "making $@"
	if [ ! -e $(DEPS_DIR) ]; then mkdir $(DEPS_DIR); fi
	mkdir -p $(DEPS_DIR)/aux
	$(LATEXMK) -pdf -dvi- -ps- -deps-out=$(DEPS_DIR)/$@P $<
	
main.pdf: aux/main.pdf
	cp aux/main.pdf ./$@
           
# Make constituency trees from parser outputs
parses/tex/%.tex: parses/parsed/%.txt
	bin/qtree $^ > $@

# Generate parser outputs
parse:
	TOKENIZERS_PARALLELISM=false python3 bin/make_parses.py
# Dependencies

#%.d: %.tex
	#bin/dependencies $* > $@

#sources = aux/main.tex

# include $(sources:.tex=.d)
