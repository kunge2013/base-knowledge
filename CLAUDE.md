# LLM Wiki - Claude Code Schema

This is an LLM-implemented personal knowledge base following Andrej Karpathy's LLM Wiki pattern.

## Overview

This is a three-layer architecture:
- **raw/** - Immutable source documents (never modified by Claude)
- **wiki/** - LLM-maintained structured markdown wiki (Claude owns this layer)
- **CLAUDE.md** - This file: defines conventions and workflows

This wiki is for:
- Machine learning research
- Competitive analysis
- Book notes
- General knowledge accumulation

## Directory Structure

```
raw/
├── articles/    # Web articles, blog posts, research papers
├── books/       # Book chapters, complete books
├── reports/     # Competitive analysis, industry reports
└── assets/      # Images, attachments (downloaded locally for Obsidian)

wiki/
├── overview.md            # Home page - overall overview and synthesis
├── index.md               # Content-oriented catalog of all pages
├── log.md                 # Append-only chronological log of all changes
├── sources/               # Summaries of raw sources (one source = one page)
├── concepts/              # Concept/topic pages (ideas, techniques, theories)
├── entities/              # Entity pages (authors, companies, products, people)
└── queries/               # Saved query responses and analyses

code/
├── chapterxxx-code           # 某章节代码实现文件
```

## Page Format Conventions

### YAML Frontmatter

Every wiki page **must** start with YAML frontmatter compatible with Obsidian Dataview:

```yaml
---
title: Page Title
date: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [category, subtag]
sources: [["path/to/source", "Source Name"], ...]
---
```

Fields:
- `title`: Display title of the page
- `date`: Creation date
- `last_updated`: Last modification date (update on every edit)
- `tags`: List of tags for categorization. Use hierarchical tags (e.g., `ml/transformer`, `competitor/openai`)
- `sources`: List of `[link, name]` pairs for sources that informed this page

### Internal Links

Use Obsidian format `[[wiki/concepts/page-name]]` for internal links. Short form works: `[[concepts/page-name]]`.

### Citations

Always cite original sources. When referencing information from a raw source, link to the corresponding `[[sources/xxx]]` wiki page which links back to the original raw document.

## Workflows

### 1. Ingest Workflow (when adding a new raw source)

When the user asks to ingest a new source located at `raw/path/to/file.md`:

1. **Read** - Read the entire source document
2. **Discuss** - Summarize the key takeaways and main points for the user. Ask for guidance on what to emphasize.
3. **Create Source Summary** - Create/update `wiki/sources/[source-name-slug].md` with:
   - Summary of the source
   - Key points and conclusions
   - Citation back to the raw file
4. **Extract Concepts** - Identify all key concepts mentioned. For each concept:
   - If page doesn't exist: create `wiki/concepts/[concept-slug].md` with definition/explanation
   - If page exists: update it with new information from this source, note if new information contradicts existing claims
5. **Extract Entities** - Identify all key entities (authors, companies, products, people):
   - If page doesn't exist: create `wiki/entities/[entity-slug].md`
   - If page exists: update it with new information
6. **Update Index** - Add new pages to `wiki/index.md` organized by category
7. **Log Entry** - Append an entry to `wiki/log.md` with format:
   ```
   ## [YYYY-MM-DD] ingest | Source Name
   - Created: 1 source summary, 3 concepts, 2 entities
   - Updated: 1 existing concept
   - Raw source: `raw/path/to/file.md`
   ```
8. **Update Overview** - Update `wiki/overview.md` if the new source changes the overall synthesis.

A single source may touch 5-15 wiki pages. This is expected and desired - knowledge gets integrated, not just indexed.

### 2. Query Workflow (when user asks a question)

1. **Locate** - Read `wiki/index.md` to identify relevant pages
2. **Read** - Read all relevant wiki pages
3. **Synthesize** - Answer the question, citing wiki pages (and through them, original sources)
4. **Preserve** - If the answer is a valuable, enduring synthesis or analysis that future queries might benefit from, save it as `wiki/queries/[query-slug].md` and update index and log. Don't save trivial conversational answers.

### 3. Lint Workflow (periodic wiki health check)

When user asks for a lint/health check:

1. **Scan** all wiki pages
2. **Check for**:
   - Contradictions between pages
   - Stale claims that newer sources contradict
   - Orphan pages with no inbound links
   - Concepts mentioned but not yet having their own page
   - Missing cross-references
   - Broken internal links
3. **Report** findings to user with specific file paths
4. **Fix** any issues user approves fixing
5. **Suggest** new questions to explore and gaps to fill

## Index Format

`wiki/index.md` is organized by category:

```markdown
# Index

## Sources

- [[sources/source-name | Source Name]] - One-line description of the source

## Concepts

- [[concepts/concept-name | Concept Name]] - Brief definition

## Entities

- [[entities/entity-name | Entity Name]] - Brief description

## Queries

- [[queries/query-name | Query Title]] - Brief description
```

Keep this updated on every ingest.

## Log Format

`wiki/log.md` is append-only. Each entry:

```markdown
## [YYYY-MM-DD] action | Description

- Details...
```

Where `action` is one of: `ingest`, `update`, `query`, `lint`.

## Principles

- **raw is immutable**: Never modify or delete files in `raw/`. If a source needs to be replaced, add a new file.
- **Claude does the bookkeeping**: All maintenance (updating cross-references, index, log, integrating new info) is automatic. User shouldn't have to do it.
- **Compound accumulation**: Every ingest and every query should leave the wiki richer than before. Valuable output gets saved, not lost in chat.
- **Obsidian compatibility**: All conventions follow Obsidian best practices (internal links, frontmatter, etc.)
- **Git for version control**: The entire wiki is a git repo - we get version history for free.

## When in Doubt

- Follow Karpathy's original idea: the wiki should compound over time, with the LLM doing all the tedious maintenance work.
- More cross-references are better than fewer.
- Split concepts/entities into their own pages even if they're short - better to have many small pages than few large ones.


