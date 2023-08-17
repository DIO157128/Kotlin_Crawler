import os
import tree_sitter
from tree_sitter import Language

# 加载Kotlin的Tree-sitter语法库
KOTLIN_LANGUAGE = Language('./kotlin.so')

# 初始化Tree-sitter解析器
parser = tree_sitter.Parser()
parser.set_language(KOTLIN_LANGUAGE)

# 要解析的Kotlin代码
kotlin_code = """
fun main() {
    println("Hello, Kotlin!")
}
"""

# 解析Kotlin代码
tree = parser.parse(bytes(kotlin_code, 'utf-8'))

# 打印解析树
print(tree.root_node)
