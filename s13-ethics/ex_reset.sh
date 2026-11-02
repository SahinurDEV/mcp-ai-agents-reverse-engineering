#!/bin/sh
# ex_reset.sh: undo Exercise 13 (remove own(...) lines and the built binary)
cd "$(dirname "$0")"; sed -i '/ own(/d' scope.txt; rm -f ex/mytool; ./reset.sh
