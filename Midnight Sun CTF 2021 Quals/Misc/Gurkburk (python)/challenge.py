#!/usr/bin/env python3
import io
import base64
import pickle


class Notes:

    def __init__(self):
        self.name = "My notes"
        self.notes = []

    def add_note(self, text):
        self.notes.append(text)
    
    def remove_note(self, index):
        if index >= 0 and index < len(self.notes):
            del self.notes[index]

    def list_notes(self):
        print()
        print("##" + "#"*(len(self.name)+2))
        print("# " + self.name + " #")
        print("##" + "#"*(len(self.name)+2))
        for index, note in enumerate(self.notes):
            print(index, note)
        print()
    
    def set_title(self, title):
        self.name = title


class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if module == "copy_reg" or module == "copyreg":
            import copyreg
            return getattr(copyreg, name)

        if module == "__main__":
            import sys
            return getattr(sys.modules['__main__'], name)

        if module == "__builtin__" and name not in ["eval", "exec"]:
            import builtins
            return getattr(builtins, name)


        message = f"Your pickle is trying to load something sneaky. Only the modules __main__, __builtin__ and copyreg are allowed. eval and exec are not allowed. '{module}.{name}' is forbidden"
        raise pickle.UnpicklingError(message)



def main():

    notes = Notes()



    user_input = ""

    while user_input != "q":
        print("* Menu *")
        print("a: add a new note")
        print("e: erase a note")
        print("t: change title")
        print("d: display notes")
        print("s: save notes")
        print("l: load notes")
        print("q: quit")


        user_input = input("==> ")
        while user_input not in "aetdslq":
            user_input = input("==> ")


        if user_input == "a":
            new_text = input("Please enter a new note: ")
            notes.add_note(new_text)
            continue


        if user_input == "e":
            try:
                index = int(input("Please enter index of note to erase: "))
                notes.remove_note(index)
            except:
                pass
            continue


        if user_input == "t":
            new_title = input("Please enter a new title: ")
            notes.set_title(new_title)
            continue


        if user_input == "d":
            notes.list_notes()
            continue


        if user_input == "s":
            data = pickle.dumps(notes, 0)
            base64_data = base64.b64encode(data).decode("ascii")
            print("Here is your loading code:", base64_data)
            print()
            continue


        if user_input == "l":
            loading_data = input("Please enter loading code: ")
            pickle_data = base64.b64decode(loading_data)
            notes = RestrictedUnpickler(io.BytesIO(pickle_data)).load()


        if user_input == "q":
            break


if __name__ == "__main__":
    main()