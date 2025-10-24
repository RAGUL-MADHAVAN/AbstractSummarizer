import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from genai_abstract_summarizer import create_app

# Create app instance using the factory function from __init__.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
