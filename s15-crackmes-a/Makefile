# Section 15 course CrackMes (Track A). Build: make ; hashes: make hashes
CC ?= gcc
BINS = bin/cm_strcmp bin/cm_xor bin/cm_obfus bin/cm_strip
all: $(BINS)
bin: ; @mkdir -p bin
bin/cm_strcmp: src/cm_strcmp.c | bin ; $(CC) -O0 -o $@ $<
bin/cm_xor:    src/cm_xor.c    | bin ; $(CC) -O0 -o $@ $<
bin/cm_obfus:  src/cm_obfus.c  | bin ; $(CC) -O0 -o $@ $<
bin/cm_strip:  src/cm_strip.c  | bin ; $(CC) -O2 -s -o $@ $<
hashes: all ; @sha256sum $(BINS)
clean: ; rm -rf bin
