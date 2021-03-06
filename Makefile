DIR_DATA=./data
DIR_FILES7Z=$(DIR_DATA)/files7z
DIR_TITLES=$(DIR_DATA)/titles
DIR_GRAPHS=$(DIR_DATA)/graphs #titulo, tiempo -> vecinos activos de <titulo> en <tiempo>

FILE_FINALTITLES=$(DIR_DATA)/alltitles.txt
DIR_CHGGRAPHS=$(DIR_DATA)/chggraphs #idtitle idneighbor timewherechanges
DIR_CONTACTS=$(DIR_DATA)/contacts
FILE_MINMAXTIME=$(DIR_DATA)/minmaxtime.txt

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
	@ls $(DIR_GRAPHS)/*gz | $(PARALLEL) --eta -P $(PROCS) 'gzcat {} | gsort -k1,1 -k2,2n | $(PYTHON) changes.py $(FILE_FINALTITLES) | gzip > $(DIR_CHGGRAPHS)/{/.}.gz '
	
stage4:
	@echo "STAGE4: Obtain the min and max timepoint"
	@ls $(DIR_CHGGRAPHS)/*gz | $(PARALLEL) --eta -P $(PROCS) 'gzcat {} | awk -f time.awk' | awk -f time.awk | cut -f3 -d " " > $(FILE_MINMAXTIME)
	
stage5:
	@echo "STAGE5: Generating contacts"
	@ls $(DIR_CHGGRAPHS)/*gz | $(PARALLEL) --eta -P $(PROCS) 'gzcat {} | gsort -k1,1 -k2,2 -n | $(PYTHON) contacts.py `head -n1 $(FILE_MINMAXTIME)` `tail -n1 $(FILE_MINMAXTIME)` | gzip > $(DIR_CONTACTS)/{/.}.gz'