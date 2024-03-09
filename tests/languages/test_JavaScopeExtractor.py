from pygments.lexers.jvm import JavaLexer

from codelimit.common.lexer_utils import lex
from codelimit.common.scope.scope_extractor_utils import build_scopes
from codelimit.languages.JavaScopeExtractor import JavaScopeExtractor
from tests.common.ScopeExtractorTestCase import ScopeExtractorTestCase


class JavaScopeExtractorTestCase(ScopeExtractorTestCase):
    def test_extract_headers_single_header(self):
        code = ""
        code += "public class T {\n"
        code += "  public static void main(String[] args) {\n"
        code += "    System.out.println(\"Hello world!\");\n"
        code += "  }\n"
        code += "}\n"

        tokens = lex(JavaLexer(), code)
        scope_extractor = JavaScopeExtractor()
        headers = scope_extractor.extract_headers(tokens)

        assert len(headers) == 1
        assert headers[0].name == "main"

    def test_extract_blocks_single_block(self):
        code = ""
        code += "public class T {\n"
        code += "  public static void main(String[] args) {\n"
        code += "    System.out.println(\"Hello world!\");\n"
        code += "  }\n"
        code += "}\n"

        tokens = lex(JavaLexer(), code)
        scope_extractor = JavaScopeExtractor()
        blocks = scope_extractor.extract_blocks(tokens, [])

        assert len(blocks) == 2

    def test_extract_blocks_multiple_blocks(self):
        code = ""
        code += "public class T {\n"
        code += "  private int one() {\n"
        code += "    return 1;\n"
        code += "  }\n"
        code += "  private int two() {\n"
        code += "    return 2;\n"
        code += "  }\n"
        code += "}\n"

        tokens = lex(JavaLexer(), code)
        scope_extractor = JavaScopeExtractor()
        blocks = scope_extractor.extract_blocks(tokens, [])

        assert len(blocks) == 3

    def test_single_scope(self):
        code = ""
        code += "public class T {\n"
        code += "  public static void main(String[] args) {\n"
        code += "    System.out.println(\"Hello world!\");\n"
        code += "  }\n"
        code += "}\n"

        tokens = lex(JavaLexer(), code)
        result = build_scopes(tokens, JavaScopeExtractor())

        assert len(result) == 1
        assert result[0].header.name == 'main'

    def test_multiple_scopes(self):
        code = ""
        code += "public class T {\n"
        code += "  private int one() {\n"
        code += "    return 1;\n"
        code += "  }\n"
        code += "  private int two() {\n"
        code += "    return 2;\n"
        code += "  }\n"
        code += "}\n"

        tokens = lex(JavaLexer(), code)
        result = build_scopes(tokens, JavaScopeExtractor())

        assert len(result) == 2
        assert result[0].header.name == 'one'
        assert result[1].header.name == 'two'
