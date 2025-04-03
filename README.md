#Tissue: A Static Site Generator (Reverse-Engineered)#

**Purpose:**
This static site generator transforms a directory of Markdown files with frontmatter into a fully rendered static HTML site. It uses Jinja2 for templating, supports partials, allows for custom templates per page, includes automatic filtering of content subsets, and generates SEO-friendly output including a sitemap.

---

## System Overview

**Input:**
- Markdown (`.md`) files with YAML frontmatter
- Optional partials in Markdown format for inclusion in templates
- Jinja2-compatible HTML templates
- Static assets (e.g. CSS, JS, images)

**Output:**
- Rendered `.html` pages in a `build/` directory
- A `sitemap.xml` file
- A copy of all static files and images

**Key Behaviors:**
- Uses a default template unless a specific template is declared in frontmatter
- Treats `index.md` specially: it automatically uses `index.html` from templates
- Renders partial Markdown files into Jinja2-includable HTML snippets prefixed with `_`
- Filters pages out of `all_pages` if frontmatter key `exclude_from_pages` is present and truthy (even blank)
- Exposes `all_pages` and named subsets (e.g., `p_pages`) to templates

---

## Directory Layout

```
.
├── build/               # Output directory (generated)
├── markdown/            # Markdown content files
│   └── index.md
├── partials/            # Markdown fragments (converted to _*.html)
│   └── header.md
├── static/              # Static files copied as-is
├── templates/           # Jinja2 HTML templates
│   ├── default.html
│   └── index.html
└── generate.py          # The builder script
```

---

## Markdown File Conventions

Each `.md` file may include a YAML frontmatter block:

```yaml
---
title: "Page Title"
desc: "Meta description"
template: custom.html
sort_class: p
css_class: product-card
imago: /images/widget.jpg
exclude_from_pages: true
---
```

### Frontmatter Keys:
- `title`: Used in the page and metadata
- `desc`: Used in meta tags or page summaries
- `template`: Custom template to use instead of default
- `sort_class`: Used for ordering in `all_pages`
- `css_class`: Optional CSS class for the page
- `imago`: Path to an image (for cards, galleries)
- `exclude_from_pages`: If present and not explicitly false, this page is omitted from `all_pages`

---

## Template Context
Each page is rendered with:

- `content`: Rendered HTML from the Markdown content
- `title`, `desc`, `template`, etc.: From frontmatter
- `all_pages`: All other pages, excluding the current and any with `exclude_from_pages`
- `p_pages`: Subset where `sort_class == "p"`

These context variables can be used in templates for listings, menus, indexes, galleries, etc.

---

## Rendering Rules

| Result HTML      | Markdown Input     | Template Used     | Subtleties                                                                  |
|------------------|--------------------|-------------------|-----------------------------------------------------------------------------|
| `index.html`     | `index.md`         | `index.html`      | Automatically uses `index.html` if present in templates                    |
| `foo.html`       | `foo.md`           | `default.html`    | Unless frontmatter specifies `template: custom.html`                        |
| `bar.html`       | `bar.md`           | `custom.html`     | Custom template must be in `templates/`                                     |

---

## Partials

Files in `partials/` ending with `.md` are rendered into HTML and saved to `templates/_<name>.html`. These can be included in templates using:

```jinja
{% include "_header.html" %}
```

---

## Build Process Steps

1. **Render Partials:** Convert Markdown files in `partials/` to HTML in `templates/`
2. **Load Pages:** Read all `.md` files in `markdown/` with frontmatter and content
3. **Sort Pages:** Pages with `sort_class` are sorted lexically, others follow
4. **Subset Pages:** Create named subsets (e.g., `p_pages`) for use in templates
5. **Render Pages:** Apply templates to each Markdown file and write to `build/`
6. **Copy Static Files:** Copy `static/` and `images/` into the `build/` output
7. **Generate Sitemap:** Write a sitemap.xml including all page URLs and `lastmod`

---

## Summary
This builder is optimized for clarity and modularity. It supports dynamic composition of content using Markdown + frontmatter, allows partial reuse of content, and provides a maintainable base for content-heavy sites with minimal tooling dependencies.

It is designed for developers and content creators who prefer structure and clarity over complexity and automation magic.

---

**Author:** Matthew Grimm
**Tooling:** Python, Jinja2, Markdown, YAML, HTML, CSS

