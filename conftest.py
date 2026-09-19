# 空文件，但必须存在：项目里的模块（ingest.py、rag.py...）都是平铺在根目录的，
# 没有打包成 src 布局。pytest 发现某个目录下有 conftest.py 时，会把这个目录也
# 加进 sys.path，tests/ 里的用例才能 `from ingest import ...` 这样直接导入。
