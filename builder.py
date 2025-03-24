import os
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone

# Directories
MARKDOWN_DIR = "markdown"       
BUILD_DIR = "build"             
TEMPLATES_DIR = "templates"      
STATIC_DIR = "static"            

# Default Templates
INDEX_TEMPLATE = "index.html"  
DEFAULT_TEMPLATE = "default.html"             # Renamed from base.html

# Ensure build directory exists
os.makedirs(BUILD_DIR, exist_ok=True)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Collect metadata for all pages (for Site Index and Sitemap)
all_pages = []
sitemap_entries = []
base_url = "https://yourdomain.com"  # Change this to your actual site URL

for filename in os.listdir(MARKDOWN_DIR):
    if filename.endswith(".md"):
        md_path = os.path.join(MARKDOWN_DIR, filename)
        
        with open(md_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        name = filename.replace(".md", "")
        page_url = f"/{name}.html"
        lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Extract front matter data
        sort_class = post.get("sort_class", None)  # Default is None
        template = post.get("template", None)  # Custom template if specified
        title = post.get("title", name.title())
        desc = post.get("desc", "")
        imago = post.get("imago", "")
        css_class = post.get("css_class", "")

        # Exclude index.html from the Site Index
        if name != "index":
            all_pages.append({
                "title": title,
                "desc": desc,
                "imago": imago,
                "css_class": css_class,
                "url": page_url,
                "sort_class": sort_class,  # Pass to template
            })

        # Add to sitemap
        sitemap_entries.append(f'<url>\n'
                               f'<loc>{base_url}{page_url}</loc>\n'
                               f'<lastmod>{lastmod}</lastmod>\n'
                               f'</url>\n')




# Assign a low sorting value (~) for empty or missing sort_class
sorted_pages = sorted(
    [p for p in all_pages if p.get("sort_class") and p["sort_class"].strip()],
    key=lambda p: p["sort_class"].strip() if p["sort_class"].strip() else "~"
)

# All pages without a valid `sort_class` remain in original order
unsorted_pages = [p for p in all_pages if not p.get("sort_class") or not p["sort_class"].strip()]

# Concatenate: sorted pages first, unsorted pages after
all_pages = sorted_pages + unsorted_pages

# Debugging: Print to check sorted output
print("Sorted Pages:", sorted_pages)
print("Unsorted Pages:", unsorted_pages)



# Process Markdown files
for filename in os.listdir(MARKDOWN_DIR):
    if filename.endswith(".md"):
        md_path = os.path.join(MARKDOWN_DIR, filename)
        html_filename = filename.replace(".md", ".html")
        html_path = os.path.join(BUILD_DIR, html_filename)

        # Read frontmatter and content
        with open(md_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # Extract metadata
        title = post.get("title", filename.replace(".md", "").title())
        desc = post.get("desc", "")
        imago = post.get("imago", "")
        css_class = post.get("css_class", "")
        sort_class = post.get("sort_class", None)  # Include sort-class in processing
        template = post.get("template", None)  # Get custom template if specified

        # Convert Markdown content to HTML
        html_content = markdown.markdown(post.content)

        # Determine which template to use
        if template:
            template_file = f"{template}.html"  # Use user-defined template
        elif filename == "index.md":
            template_file = INDEX_TEMPLATE  # Use index template
        else:
            template_file = DEFAULT_TEMPLATE  # Default to default.html

        # Load Jinja2 template
        template = env.get_template(template_file)

        # Exclude the current page from the Site Index
        filtered_pages = [p for p in all_pages if p["url"] != f"/{html_filename}"]

        output = template.render(
            title=title,
            desc=desc,
            imago=imago,
            css_class=css_class,
            sort_class=sort_class,
            template=template_file,
            content=html_content,
            all_pages=filtered_pages,  # Sorted list of all pages
        )

        # Write HTML to build directory
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"Generated {html_path} using {template_file}")

# Copy static files (CSS, JS, images) to build directory
os.system(f"cp -r {STATIC_DIR} {BUILD_DIR}")
os.system(f"cp -r {os.path.join(MARKDOWN_DIR, '..', 'images')} {BUILD_DIR}")

# Generate sitemap.xml with better structure
sitemap_xml = f'''
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(sitemap_entries)}
</urlset>
'''


sitemap_path = os.path.join(BUILD_DIR, "sitemap.xml")
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Generated {sitemap_path}")
