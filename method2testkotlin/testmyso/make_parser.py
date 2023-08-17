from tree_sitter import Language

Language.build_library(
  # so文件保存位置
  './kotlin.so',

  # vendor文件下git clone的仓库
  [
    '/root/ybw/tree-sitter-kotlin',

  ]
)
