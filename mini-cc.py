#!/usr/bin/env python3
import time
import sys
import re

# Terminal Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RED = '\033[91m'
RESET = '\033[0m'

C_SOURCE = """#include <stdio.h>

int main() {
    int power_level = 9000;
    printf("Scanner says: %d\\n", power_level);
    return 0;
}"""

def animate_text(text, delay=0.01, color=RESET):
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def lexer(code):
    animate_text(">>> [1/3] INITIATING LEXICAL ANALYSIS...", 0.03, CYAN)
    # The catch-all group |(\S) prevents silent failures
    token_specification = r'(#include\s+<.*?>)|(".*?")|(\w+)|([{}();,=])|(\S)'
    tokens = []
    
    for match in re.finditer(token_specification, code):
        text = match.group(0)
        
        if text.startswith('#'): kind = 'PREPROCESSOR'
        elif text.startswith('"'): kind = 'STRING'
        elif text.isdigit(): kind = 'NUMBER'
        elif text in ['int', 'return']: kind = 'KEYWORD'
        elif re.match(r'^[{}();,=]$', text): kind = 'SYMBOL'
        elif match.group(5): 
            print(f"\n{RED}SYNTAX ERROR: Unrecognized character '{text}'{RESET}")
            sys.exit(1)
        else: kind = 'IDENTIFIER'
        
        tokens.append((kind, text))
        time.sleep(0.02)
        print(f"  {YELLOW}Tokenizing:{RESET} {kind:<12} -> {text}")
        
    return tokens

def parser(tokens):
    animate_text("\n>>> [2/3] BUILDING ABSTRACT SYNTAX TREE (AST)...", 0.03, CYAN)
    ast = {"type": "Program", "body": []}
    
    i = 0
    while i < len(tokens):
        kind, val = tokens[i]
        
        # 1. Detect Variable Declarations
        if kind == 'KEYWORD' and val == 'int' and i + 3 < len(tokens):
            if tokens[i+1][0] == 'IDENTIFIER' and tokens[i+2][1] == '=':
                var_name = tokens[i+1][1]
                var_value = tokens[i+3][1]
                
                node = {"type": "VariableDeclaration", "name": var_name, "value": var_value}
                ast["body"].append(node)
                time.sleep(0.2)
                print(f"  {MAGENTA}AST Node Generated:{RESET} {node}")
                i += 4
                continue
                
        # 2. Detect Function Calls (Now supporting arguments)
        if kind == 'IDENTIFIER' and val == 'printf':
            str_arg = tokens[i+2][1].strip('"')
            var_arg = None
            
            # Look ahead to see if there is a comma after the string
            if i + 3 < len(tokens) and tokens[i+3][1] == ',':
                var_arg = tokens[i+4][1] # Extract the variable name
                
            node = {"type": "CallExpression", "name": "printf", "value": str_arg, "variable": var_arg}
            ast["body"].append(node)
            time.sleep(0.2)
            print(f"  {MAGENTA}AST Node Generated:{RESET} {node}")
            
        i += 1
            
    return ast

def execute(ast):
    animate_text("\n>>> [3/3] EXECUTING AT COMPILE-TIME (JIT)...", 0.03, CYAN)
    time.sleep(0.5)
    print(f"\n{GREEN}--- PROGRAM OUTPUT ---{RESET}")
    
    memory = {}
    
    for node in ast["body"]:
        # Execute Variable Allocation
        if node["type"] == "VariableDeclaration":
            memory[node["name"]] = int(node["value"])
            animate_text(f"[SYSTEM] Allocated integer '{node['name']}' at virtual address 0x01 = {node['value']}", 0.02, YELLOW)
            
        # Execute Print Statement
        elif node["type"] == "CallExpression" and node["name"] == "printf":
            output = node["value"].replace('\\n', '\n')
            
            # Memory Injection Logic
            if node.get("variable"):
                target_var = node["variable"]
                if target_var in memory:
                    # Replace %d with the value pulled from memory
                    output = output.replace("%d", str(memory[target_var]))
                else:
                    print(f"\n{RED}RUNTIME ERROR: Variable '{target_var}' is not defined!{RESET}")
                    sys.exit(1)
                    
            animate_text(output, 0.05, GREEN)
            
    print(f"{GREEN}----------------------{RESET}")

if __name__ == "__main__":
    animate_text("LOADING C SOURCE CODE:\n", 0.02)
    print(C_SOURCE + "\n")
    time.sleep(0.5)
    
    tokens = lexer(C_SOURCE)
    ast = parser(tokens)
    execute(ast)