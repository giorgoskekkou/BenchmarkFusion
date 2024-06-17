from function_merge import main as function_merge

in_folder = './benchmarks/'

# class Node:
#     def __init__(self, line, function_name):
#         self.line = line
#         self.function_name = function_name
#         self.children = []
#         self.parent = None

#     def add_child(self, child):
#         self.children.append(child)

#     def print_tree(self, level=0):
#         print(' ' * level, self.line, ' -> ', self.function_name)
#         # print(' ' * level, self.function_name)
#         for child in self.children:
#             print("Child: ", child.function_name)
#             child.print_tree(level + 1)
def tokenize_line(line):
    tokens = []
    buffer = ''
    for char in line:
        if char in [' ', '.', '(', ')']:
            tokens.append(buffer)
            buffer = ''
        else:
            buffer += char
    return tokens



def remove_duplicates(l):
    new_l = []
    for item in l:
        if item not in new_l:
            new_l.append(item)
    return new_l
    # return list(set(l))

def is_function_call(line, function_names):
    # print("FUNCTION NAMES: ", function_names)
    function_matches = []
    stripped_line = line.strip()
    for name in function_names:
        # if name in stripped_line and stripped_line.startswith(name) and not stripped_line.startswith('def'):
        # Tokenize the line
        tokenized_line = tokenize_line(line)
        # print("Tokenized line: ", tokenized_line)
        if name in tokenized_line:
            print("FOUND: ", name)
        # if name in stripped_line:
            function_matches.append(name)
            # return name
    print("Function matches: ", remove_duplicates(function_matches))
    return remove_duplicates(function_matches)
    # return function_matches
    # return list(set(function_matches))
    # return None
    # return stripped_line.endswith(')') and not stripped_line.startswith('def')

# filename = input('Enter the name of the file: ')
# filename = "src/in/func.py"
# node = Node('main', 'main')
# node = Node('root', 'root')


function_names = []
list_of_nodes = []
function_calls = []
hierarchical_functions = {}
function_dictionary, lambda_functions = function_merge()

function_names = [function_dictionary[function]['function_name'] for function in function_dictionary]

for item in function_dictionary:
    directory = function_dictionary[item]['directory']
    function_name = function_dictionary[item]['function_name']
    if directory not in hierarchical_functions:
        hierarchical_functions[directory] = []
    hierarchical_functions[directory].append(function_name)

print("Hierarchical functions: ", hierarchical_functions)


print("Function names: ", function_names)

for lambda_function in lambda_functions:
    with open(f'{in_folder}{lambda_function}/func.py') as f:
        code = f.read().split('\n')
        
        # for function_element in function_dictionary:
        #     print(function_element)
        for function_element in function_dictionary:
            el = function_dictionary[function_element]
            if el['directory'] == lambda_function:
                start = el['start']
                end = el['end']
                print(f"Function: {el['function_name']} at {start} - {end} from file: {lambda_function}")
                for index in range(start - 1, end):
                    line = code[index]
                    # print(line)
                    if line.strip().startswith('#'):
                        continue
                    print("TEMP: ", el['function_name'])
                    print(hierarchical_functions[lambda_function])
                    function_matches = is_function_call(line, hierarchical_functions[lambda_function])
                    # function_matches = is_function_call(line, function_names)
                    # if function_name and function_name != el['function_name']:
                    if function_matches != []:
                        # print("FUNCTION MATCES: ", function_matches)

                        for i in range(len(function_matches)):
                            if function_matches[i] != el['function_name']:
                                print(f"Function call: {function_matches[i]}")
                                function_calls.append({'src': el['function_name'], 'dst': function_matches[i] , 'lambda': lambda_function, 'line': index + 1})
                                # print(f"Function call: {function_names[i]}")
                                # function_calls.append({'src': el['function_name'], 'dst': function_names[i] , 'lambda': lambda_function, 'line': index + 1})
                        # print(f"Function call: {function_name}")
                        # function_calls.append({'src': el['function_name'], 'dst': function_name , 'lambda': lambda_function, 'line': index + 1})


for key in function_calls:
    print(key)
#     # iterate to get the function calls
#     for line in lines:
#         if line.strip().startswith('#'):    # skip comments
#             continue
#         # print(line.strip('\n'))
#         function_name = is_function_call(line, function_names)
#         # if is_function_call(line, function_names):
#         if function_name:
#             print()
#             # list_of_nodes.append(Node)
#             node.add_child(Node(line.strip('\n'), function_name))
#             list_of_nodes.append(Node(line.strip('\n'), function_name))

#     # iterate 3rd time to add children to the nodes
#     for node in list_of_nodes:
#         node.print_tree()
