CC ?= gcc
CFLAGS ?= -O0 -g -fno-stack-protector -no-pie
SRC := src
BIN := bin

.PHONY: all clean test
all: $(BIN)/l1_hello $(BIN)/l2_xor $(BIN)/l3_serial $(BIN)/l4_nested

$(BIN):
	mkdir -p $(BIN)

$(BIN)/l1_hello: $(SRC)/l1_hello.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN)/l2_xor: $(SRC)/l2_xor.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN)/l3_serial: $(SRC)/l3_serial.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ $<

$(BIN)/l4_nested: $(SRC)/l4_nested.c | $(BIN)
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf $(BIN)
