#!/bin/sh
# Node-only regression tests for the pure Core logic in src/chord-sketch.html
cd "$(dirname "$0")" || exit 1
fail=0
for t in check*.js; do
  if out=$(node "$t" 2>&1); then echo "ok   $t"; else echo "FAIL $t"; echo "$out" | tail -5; fail=1; fi
done
exit $fail
