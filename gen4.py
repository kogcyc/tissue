import frontmatter
import os
import json
from jinja2 import Environment, FileSystemLoader

# Load configuration
def load_config(config_path='config.json'):
    with open(config_path, 'r') as file:
        return json.load(file)

# Prepare build directory
def prepare_build_directory(build_dir):
    if os.path.exists(build_dir):
        for root, dirs, files in os.walk(build_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
    os.makedirs(build_dir, exist_ok=True)

# Find all markdown files in source directory
def find_markdown_files(source_dir, skip_dirs):
    md_files = []
    for dirpath, _, filenames in os.walk(source_dir):
        if any(skip_dir in dirpath.split(os.sep) for skip_dir in skip_dirs):
            continue  # Skip directories listed in config
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                md_files.append(file_path)
    return md_files

# Render HTML
def render_html(config, filedata, template_name='base.html'):
    env = Environment(loader=FileSystemLoader(config.get('template_directory', 'source/static/templates')))
    template = env.get_template(template_name)

    collection = filedata['collection']
    build_dir = config.get('build_directory', 'build')
    
    if collection == 'root':
        output_file = os.path.join(build_dir, f"{filedata['fn']}.html")
    else:
        collection_dir = os.path.join(build_dir, collection)
        os.makedirs(collection_dir, exist_ok=True)
        output_file = os.path.join(collection_dir, f"{filedata['fn']}.html")

    rendered_html = template.render(filedata)

    with open(output_file, 'w') as f:
        f.write(rendered_html)
    
    print(f"Generated: {output_file}")

# Main function
def main():
    config = load_config()
    build_dir = config.get('build_directory', 'build')
    source_dir = config.get('source_directory', 'source')
    skip_dirs = config.get('skip_directories', [])

    prepare_build_directory(build_dir)
    markdown_files = find_markdown_files(source_dir, skip_dirs)

    all_file_data = {}
    for filepath in markdown_files:
        with open(filepath, 'r') as file:
            post = frontmatter.load(file)

            frontmatter_data = post.metadata
            content = post.content

            rel_path = os.path.relpath(filepath, source_dir)
            collection = rel_path.split(os.sep)[0]

            filename = os.path.splitext(os.path.basename(filepath))[0]

            all_file_data[filepath] = {
                'frontmatter': frontmatter_data,
                'content': content,
                'collection': collection,
                'fn': filename
            }

    print(all_file_data)

    for filepath, data in all_file_data.items():
        render_html(config=config, filedata=data)

if __name__ == '__main__':
    main()
