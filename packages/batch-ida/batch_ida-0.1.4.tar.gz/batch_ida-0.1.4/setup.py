# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batch_ida']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'batch-ida',
    'version': '0.1.4',
    'description': 'A python library for generate ida pro files in batch mode & compare executable files use bindiff in batch mode.',
    'long_description': '# Batch-IDA\n\nA python library for generate ida pro files in batch mode & compare executable files use bindiff in batch mode.\n\n\n## Features\n\n1. Fast generate idb/i64 files from binary files in batch mode (Multiprocess supported)\n    ![generate_idb](images/generate_idb.gif)\n2. IDA Pro Plugin Script support\n3. Use bindiff to batch compare idb files\n4. Roughly read the comparison results\n\n## Requirements\n\n+ Windows environment (i don\'t know if it works on linux)\n+ IDA pro 7 (Only tested on IDA pro 7.7)\n+ BinDiff 7 (Optional, used to compare executable files in batch mode)\n\n## Install\n\n```\npip install --upgrade batch-ida\n```\n\n## Usage\n\n### BI_IDA\n\nGenerate .idb/.i64 files (and run plugin) in batch mode.\n\n```python\nfrom batch_ida import BI_IDA\n\n\nbi = BI_IDA()\nbi.set_ida_path(\'C:\\Tools\\IDA Pro\')\n\n# optional\nbi.set_script(r\'.\\example_script.py\')   # run efiXplore IDA plugin\nbi.max_subprocess = 8\n\nbi.batch_idb_fromdir(r\'.\\qhtf.bin_PEs\')\n```\n\n\n### BI_Dircmp\n\nCompare files in dirA & dirB, and move different files to dst_a & dst_b.\n\n```python\n# 1. BI_Dircmp比较原文件夹，并复制哈希不同的文件到目标文件夹\nfrom batch_ida import BI_Dircmp\n\n# 原始文件夹dirA，dirB，包含需要比较的二进制\ndirA = r\'\\\\wsl.localhost\\Ubuntu-22.04\\home\\zzh\\fw_project/d9_idrac/_5.00.10.20.d9.extracted/squashfs-root/usr/lib/\'\ndirB = r\'\\\\wsl.localhost\\Ubuntu-22.04\\home\\zzh\\fw_project/d9_idrac/_5.00.20.00.d9.extracted/squashfs-root/usr/lib/\'\n\n# 目标文件夹dstA，dstB，用来存放哈希值不同的二进制，是空文件夹\ndst_a = r\'C:\\Users\\zzhihan\\Desktop\\36347\\1020\'\ndst_b = r\'C:\\Users\\zzhihan\\Desktop\\36347\\2000\'\n\n# 使用Dircmp比较两个文件夹中文件的差异，并将哈希不同的文件复制到目标文件夹\nbid = BI_Dircmp(dirA, dirB, dst_a, dst_b)\nbid.cmp()\n```\n\n### BI_Bindiff\n\nGenerate .idb and .bindiff files in batch mode.\n\n```python\n# 使用Bindiff批量分析二进制文件\nfrom batch_ida import BI_Bindiff\n\nbib = BI_Bindiff()\n\n# 设置ida和bindiff路径\nbib.set_ida_path(\'C:\\Tools\\IDA Pro\')\nbib.set_bindiff_path(\'C:\\Program Files\\BinDiff\')\nbib.max_subprocess = 16\n\n# 开始比较，结果输出到output文件夹，批量生成idb比较慢\noutput = bib.batch_bindiff(dst_a, dst_b)\n```\n\n### BI_Analyzer\n\nAnalyze Bindiff files (sqlite3 file format) in batch mode and print the results.\n\n```python\n# 使用Analyzer批量读输出的Bindiff文件，其实就是sqlite3数据库文件\nfrom batch_ida import BI_Analyzer\n\nbia = BI_Analyzer(r\'C:\\Users\\zzhihan\\Desktop\\test\\4_4010_vs_4_4040\')\n# bia.print_base_info()\n\n# 输出存在不匹配函数的文件，和相似度小于0.95的文件\ninfo_list = bia.get_info_list()\nfor i in info_list:\n    if i[\'total_func\'] & i[\'func_dif\'] & i[\'libfunc_dif\']:\n        print("%.02f\\t%.2f\\t%d\\t%d\\t%d\\t%s" % (i[\'similarity\'], i[\'confidence\'], i[\'total_func\'], i[\'func_dif\'], i[\n            "libfunc_dif"], i[\'name\']))\n    elif i[\'similarity\'] < 0.95 and i[\'similarity\'] != 0.0:\n        print("%.02f\\t%.2f\\t%d\\t%d\\t%d\\t%s" % (i[\'similarity\'], i[\'confidence\'], i[\'total_func\'], i[\'func_dif\'], i[\n            "libfunc_dif"], i[\'name\']))\n```\n',
    'author': 'ZhengZH',
    'author_email': '41407837+chnzzh@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chnzzh/batch-ida',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
