import json

def load_json(path):
    with open(path) as json_input_file:
        return json.load(json_input_file)

def write_list_to_file(program, list_to_write):
    """ A function that writes a list to an file. The list is a JSON list """
    with open(program.split('.')[0] + ".output.json", 'a+') as output_file:
        output_file.write(json.dumps(list_to_write, indent=3, sort_keys=False))

def get_contained(list1, list2):
    """ A function that returns all communs between 2 litst """
    return [x for x in list1 for y in list2 if x == y]

def remove_duplicates(possible_vulns):
    """ A function that removes the duplicated elements of a list """
    return list(set(possible_vulns))

def indices(lst, element):
    """ A function that searches for all occurrences of an element in a list """
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)

