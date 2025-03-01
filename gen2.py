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
def find_markdown_files(root_dir):
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                md_files.append(file_path)
    return md_files

# Main function
def main():
    config = load_config()
    print(f'CONFIG: {config}')
    build_dir = config.get('build_directory', 'public')
    source_dir = os.path.dirname(config.get('root_directory', 'source/root'))
    
    prepare_build_directory(build_dir)
    markdown_files = find_markdown_files(source_dir)
    #print("Markdown files found:", markdown_files)

    all_file_data = {}
    #for filepath in markdown_files:
        #all_file_data[filepath] = {}
    #print(all_file_data)


    for filepath in markdown_files:
        # Read the markdown file
        with open(filepath, 'r') as file:
            post = frontmatter.load(file)
        
            # Extract frontmatter and content
            frontmatter_data = post.metadata  # This is a dictionary of frontmatter
            content = post.content  # This is the markdown content
        
            #key = 'source/root/index.md'

            # Extract leading directory (first part of the path)
            leading_dir = filepath.split(os.sep)[0]

            # Extract filename without extension
            filename = os.path.splitext(os.path.basename(filepath))[0]

            # Add the frontmatter and content to the dictionary
            all_file_data[filepath] = {
                'frontmatter': frontmatter_data,
                'content': content,
                'collection': leading_dir,
                'fn': filename
            }

    print(all_file_data)

if __name__ == '__main__':
    main()
