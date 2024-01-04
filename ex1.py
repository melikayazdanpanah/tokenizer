import re

keywords = {"ashar", "chap", "begir", "sahih", "agar"}
operators = {"+", "-", "*", "/", "<", ">", "=", "<=", ">=", "==", "!=", "++", "--", "%"}
delimiters = {'(', ')', '{', '}', '[', ']', '"', "'", ';', ','}  # Removed empty string

def detect_keywords(text):
    return list(set(filter(lambda word: word in keywords, text)))

def detect_operators(text):
    return list(set(filter(lambda word: word in operators, text)))

def detect_delimiters(text):
    return list(set(filter(lambda word: word in delimiters, text)))

def detect_num(text):
    return re.findall(r'-?\d+\.\d+|-?\d+', ' '.join(text))


def detect_strings(text):
    return re.findall(r'"([^"]*)"', ' '.join(text))


def detect_identifiers(text):
    k = detect_keywords(text)
    o = detect_operators(text)
    d = detect_delimiters(text)
    n = detect_num(text)
    s = detect_strings(text)
    not_ident = k + o + d + n + s
    return list(filter(lambda word: word not in not_ident, text))



def remove_comments(input_text):
    # Remove single-line comments
    input_text = re.sub(r'//.*', '', input_text)
    # Remove multi-line comments
    input_text = re.sub(r'/\*.*?\*/', '', input_text, flags=re.DOTALL)
    return input_text

def build_symbol_table(identifiers, types, rows, columns):
    symbol_table = {}
    for identifier, type_, row, column in zip(identifiers, types, rows, columns):
        symbol_table[identifier] = {'Type': type_, 'Row': row, 'Column': column}
    return symbol_table

with open('e1-example.txt') as t:
    text = remove_comments(t.read())
    text_tokens = re.findall(r'\b\w+\b|[^\w\s]|\w*\([^)]*\)|"[^"]*"|\b\d*\.\d+|\d+', text)

# Separate strings from other tokens
strings = detect_strings(text_tokens)

# Get identifiers and their types
identifiers = detect_identifiers(text_tokens)


types = ['keyword' if word in keywords else 'operator' if word in operators else 'delimiter' if word in delimiters else 'number' if re.match(r'-?\d+\.\d+|-?\d+', word) else 'string' if word in strings else 'identifier' for word in identifiers]

# Get row and column information
rows = [match.start() + 1 for match in re.finditer('\S', text)]
columns = [match.start() - text.rfind('\n', 0, match.start()) for match in re.finditer('\S', text)]

# Build the symbol table
symbol_table = build_symbol_table(identifiers, types, rows, columns)

print("*****************************************************")


print("\n")

print("Keywords: ", detect_keywords(text_tokens))
print("Operators: ", detect_operators(text_tokens))
print("Delimiters: ", detect_delimiters(text_tokens))
print("Identifiers: ", detect_identifiers(text_tokens))
print("Numbers: ", detect_num(text_tokens))
print("Strings: ", strings)

print("\n")
print("*****************************************************")

# Print the symbol table
print("Lexeme\t\tToken Type\t\tRow\t\tColumn\t\t")
print("-" * 70)
for identifier, info in symbol_table.items():
    print(f"{identifier}\t\t{info['Type']}\t\t{info['Row']}\t\t{info['Column']}\t\t")
