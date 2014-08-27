DIR_DATA=./data
DIR_FILES7Z=$(DIR_DATA)/files7z
DIR_TITLES=$(DIR_DATA)/titles
DIR_GRAPHS=$(DIR_DATA)/graphs

FILE_FINALTITLES=$(DIR_DATA)/alltitles.txt
DIR_CHGGRAPHS=$(DIR_DATA)/chggraphs

DIR_LOGS=./logs

PARALLEL=parallel
PROCS=8
PYTHON=python2.7
SORT=gsort

all:
	@echo "Do Nothing"

clean:
	rm -f $(DIR_TITLES)/*
	rm -f $(DIR_GRAPHS)/*
	rm -f $(DIR_LOGS)/*
	rm -f $(FILE_FINALTITLES)
	
stage1:
	@echo "STAGE1: Recovering links between pages. Also recover the title of processed pages."
	@ls $(DIR_FILES7Z)/*7z | $(PARALLEL) --eta -P $(PROCS) '7z x -so {} | $(PYTHON) parselink.py 2> $(DIR_LOGS)/stage1-{/.}.log | tee >( bash title2id.sh > $(DIR_TITLES)/{/.}.txt ) | gzip >> $(DIR_GRAPHS)/{/.}.gz'

stage2:
	@echo "STAGE2: Collect all pages' titles"
	@cat $(DIR_TITLES)/*.txt | gsort -u > $(FILE_FINALTITLES)

stage3:
	@echo "STAGE3: Sort graphs and get a collection of changes"
	@ls $(DIR_GRAPHS)/*gz | $(PARALLEL) --eta -P $(PROCS) 'gzcat {} | gsort -k1,1 -k2,2 -n | $(PYTHON) changes.py $(FILE_FINALTITLES) | gzip > $(DIR_CHGGRAPHS)/{/.}.gz '