import json
from collections import deque
import sys
import os

def load_spec(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_input(path, white):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    if data.endswith("\n"):
        data = data.rstrip("\n")
    if data == "":
        return deque([white])
    return deque(list(data))

def build_transition_map(transitions):
    m = {}
    for t in transitions:
        key = (t['from'], t['read'])
        m[key] = (t['to'], t['write'], t['dir'])
    return m

def simulate(spec, tape, max_steps=10_000_000):
    white = spec.get('white', '_')
    initial = spec.get('initial', 0)
    finals = set(spec.get('final', []))
    trans_map = build_transition_map(spec.get('transitions', []))
    head = 0
    state = initial
    steps = 0

    if len(tape) == 0:
        tape.append(white)

    while steps < max_steps:
        if head < 0:
            tape.appendleft(white)
            head = 0
        if head >= len(tape):
            tape.append(white)

        symbol = tape[head]
        key = (state, symbol)
        if key not in trans_map:
            return (1 if state in finals else 0), tape

        to_state, write_sym, direction = trans_map[key]
        tape[head] = write_sym

        if direction == 'R':
            head += 1
            if head == len(tape):
                tape.append(white)
        elif direction == 'L':
            if head == 0:
                tape.appendleft(white)
                head = 0
            else:
                head -= 1
        else:
            return 0, tape

        state = to_state
        steps += 1

    return (1 if state in finals else 0), tape

def tape_to_string(tape, white):
    s = ''.join(tape)
    if all(ch == white for ch in s):
        return white
    left = 0
    right = len(s) - 1
    while left <= right and s[left] == white:
        left += 1
    while right >= left and s[right] == white:
        right -= 1
    return s[left:right+1]

def main():
    if len(sys.argv) != 4:
        print("Uso: python tm_simulator.py <spec.json> <input.txt> <output.txt>")
        sys.exit(1)

    spec_path, input_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    spec = load_spec(spec_path)
    tape = load_input(input_path, spec.get('white', '_'))

    result, final_tape = simulate(spec, tape)

    out_str = tape_to_string(final_tape, spec.get('white', '_'))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(out_str)

    print(result)

if __name__ == "__main__":
    main()