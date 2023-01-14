from codelimit.common.scope_utils import build_scopes
from codelimit.languages.c.CLanguage import CLanguage
from codelimit.languages.c.CScopeExtractor import CScopeExtractor


def test_get_blocks_no_block():
    code = ''

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 0


def test_get_blocks_single_block():
    code = ''
    code += '#include <stdio.h>\n'
    code += 'int main(int argc, char *argv[]) {\n'
    code += '  printf("Hello world!");\n'
    code += 'return 0;\n'
    code += '}\n'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 2
    assert result[0].tokens[0].location.column == 34
    assert result[0].tokens[-1].location.line == 5
    assert result[0].tokens[-1].location.column == 1


def test_get_blocks_single_multiline_block():
    code = ''
    code += '{\n'
    code += '  int spam;\n'
    code += '  spam = 1;\n'
    code += '}'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 1
    assert result[0].tokens[-1].location.line == 4
    assert result[0].tokens[-1].location.column == 1


def test_get_blocks_multi_blocks():
    code = ''
    code += '{ int foo; }\n'
    code += '{ char bar; }\n'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 2
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[-1].location.line == 1
    assert result[1].tokens[0].location.line == 2
    assert result[1].tokens[-1].location.line == 2


def test_get_nested_blocks():
    code = ''
    code += '{ { { int foo; } } }\n'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 3
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 1
    assert result[1].tokens[0].location.line == 1
    assert result[1].tokens[0].location.column == 3
    assert result[2].tokens[0].location.line == 1
    assert result[2].tokens[0].location.column == 5


def test_get_headers_no_headers():
    tokens = CLanguage().lex('')
    result = CScopeExtractor().extract_headers(tokens)

    assert len(result) == 0


def test_get_headers_single_header():
    code = ''
    code += 'int main(int argc, char *argv) {\n'
    code += '  return 0;\n'
    code += '}\n'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_headers(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 5
    assert result[0].tokens[0].value == 'main'
    assert result[0].tokens[-1].location.line == 1
    assert result[0].tokens[-1].location.column == 30
    assert result[0].tokens[-1].value == ')'


def test_build_scopes():
    code = ''
    code += '#include <stdio.h>\n'
    code += 'char * bar() {\n'
    code += '  return "Hello world";\n'
    code += '}\n'
    code += 'void foo() {\n'
    code += '  printf(bar());\n'
    code += '}\n'

    scopes = build_scopes(CLanguage(), code)

    assert len(scopes) == 2
    assert scopes[0].header.token_string() == 'bar ( )'
    assert scopes[1].header.token_string() == 'foo ( )'


def test_build_scope_c_function():
    code = ''
    code += 'int nfs_register_sysctl(void)\n'
    code += '{\n'
    code += '    nfs_callback_sysctl_table = register_sysctl_table(nfs_cb_sysctl_root);\n'
    code += '    if (nfs_callback_sysctl_table == NULL)\n'
    code += '        return -ENOMEM;\n'
    code += '    return 0;\n'
    code += '}\n'

    tokens = CLanguage().lex(code)
    result = CScopeExtractor().extract_headers(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 1
    assert result[0].tokens[0].location.column == 5
    assert result[0].tokens[0].value == 'nfs_register_sysctl'
    assert result[0].tokens[-1].location.line == 1
    assert result[0].tokens[-1].location.column == 29
    assert result[0].tokens[-1].value == ')'

    result = CScopeExtractor().extract_blocks(tokens)

    assert len(result) == 1
    assert result[0].tokens[0].location.line == 2
    assert result[0].tokens[0].location.column == 1
    assert result[0].tokens[-1].location.line == 7
    assert result[0].tokens[-1].location.column == 1

    scopes = build_scopes(CLanguage(), code)

    assert len(scopes) == 1
