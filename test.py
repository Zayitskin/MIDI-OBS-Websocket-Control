import mido
import sys
from typing import NoReturn

def read_mode() -> NoReturn:
    selections: list = mido.get_input_names()

    if len(selections) == 0:
        print("No MIDI inputs detected.")
        sys.exit()

    for index, name in enumerate(selections):
        print(f"{index + 1}: {name}")

    choice: int = -1
    while choice < 0:
        choice = int(input("Select a port: ")) - 1
        if choice >= len(selections) or choice < 0:
            print(f"Chosen value not in valid range [1, {len(selections)}].")
            choice = -1

    with mido.open_input(selections[choice]) as port:
        for msg in port:
            print(msg)

def write_mode() -> None:
    selections: list = mido.get_output_names()

    if len(selections) == 0:
        print("No MIDI outputs detected.")
        sys.exit()

    for index, name in enumerate(selections):
        print(f"{index + 1}: {name}")

    choice: int = -1
    while choice < 0:
        choice = int(input("Select a port: ")) - 1
        if choice >= len(selections) or choice < 0:
            print(f"Chosen value not in valid range [1, {len(selections)}].")
            choice = -1

    with mido.open_output(selections[choice]) as port:
        while True:
            cmd: str = input("Input a command ([o]n, o[f]f, [q]uit): ")
            if cmd not in ["o", "f", "q"]:
                print(f"Invalid command: {cmd}")
                continue

            if cmd == "o":
                port.send(mido.Message("note_on", note = 84, velocity = 1))
            if cmd == "f":
                port.send(mido.Message("note_off", note = 84, velocity = 1))
            if cmd == "q":
                break

if __name__ == "__main__":
    mode: str = ""
    while mode not in ["r", "w"]:
        mode = input("Select a mode ([r]ead, [w]rite): ")
        if mode not in ["r", "w"]:
            print(f"Invalid mode: {mode}.")
    if mode == "r":
        read_mode()
    elif mode == "w":
        write_mode()
        
