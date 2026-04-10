# `/coding-cap - 生成文章中的代码

# Usage

`/coding-cap  <path-to-raw-file>`

## Description
生成文章内容中的相关代码，如果没有coding，自动创建coding目录以及章节目录

代码位置

```
coding/
├── chapterxxx-code           # 某章节代码实现文件
```



## Instructions

### coding 目录
- coding 目录是用于对一章节(chapters) 目录下的文件的代码实践，
例如 章节 Chapter 1_ Prompt Chaining.md 的代码需要放入 coding/Chapter_1_Prompt_Chaining/ 目录下，且基于python langchain.  安装包 requires.txt.
- 每个章节可能有很多代码文件注意都放到章节目录下面 按照 章节内容 对于的 功能生成 {章节段落}-{功能}.py ,py文件名是英文。
- 代码目录每个章节需要生成一个README.md,说明每个文件为了讲解什么内容，以及相关的代码文件说明 
- 生成的每个文件需要带上章节序号，有序命名 (生成的python文件需要带上需要带上序号 从1开始 按照章节顺序生成序号放到python 文件名前面 生成)
- python 依赖和coding/requirements.txt 维护 都是基于langchain 实现
- 生成代码摘要: 基于生成的代码 + agentic设计模式内容(Chapter_X.md)，生成摘要文件，且摘要文件的名字为Chapter_x_xxx_SUMMARY.md，生成位置在 coding/Chapter_x_xxx_SUMMARY
 *** 摘要要求***
 - 1.摘要基于中文语言描述
 - 2.摘要需要映入代码块，并说明每个代码用到了什么范式
 - 3.总结范式的使用场景
 - 4.摘要生成
  - 1.标题: 以范式名为标题-不要带任何其他内容例如(路由模式-代码摘要)不允许，只能是(路由模式)
  - 2.摘要格式: 要求整体章节结构要清晰，分层次描述，分为 4级标题
  - 3.流程图: 通过流程图 绘制 当前agentic范式的流程，基于 “mermaid” 语法
  - 4.代码块: 摘要的agentic 范式中，需要带上完整的流程代码，便于理解范式如何使用，以及场景
  - 5.所以的llm配置都和 coding/Chapter_1_Prompt_Chaining/llm_config.py 一样