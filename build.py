import os
import re

def get_component(name):
    with open(f'components/{name}.html', 'r', encoding='utf-8') as f:
        return f.read().strip()

def build():
    # Load components
    nav = get_component('nav')
    footer = get_component('footer')
    cart = get_component('cart')

    # Files to process
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html' and os.path.isfile(f)]
    # Special handling for index or just process all
    all_files = [f for f in os.listdir('.') if f.endswith('.html') and os.path.isfile(f)]

    for filename in all_files:
        print(f"Processing {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple regex replacement for nav, footer, cart blocks
        # Assumes the user might want to keep the structure

        # Replace Nav
        content = re.sub(r'<!-- BEGIN NAV -->.*?<!-- END NAV -->',
                        f'<!-- BEGIN NAV -->\n{nav}\n<!-- END NAV -->',
                        content, flags=re.DOTALL)

        # Replace Footer
        content = re.sub(r'<!-- BEGIN FOOTER -->.*?<!-- END FOOTER -->',
                        f'<!-- BEGIN FOOTER -->\n{footer}\n<!-- END FOOTER -->',
                        content, flags=re.DOTALL)

        # Replace Cart
        content = re.sub(r'<!-- BEGIN CART -->.*?<!-- END CART -->',
                        f'<!-- BEGIN CART -->\n{cart}\n<!-- END CART -->',
                        content, flags=re.DOTALL)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    build()
