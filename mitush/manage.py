
import os
import sys

# Add the project root directory to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Add the virtual environment to sys.path
venv_path = os.path.join(project_root, 'env')
if venv_path not in sys.path:
    sys.path.append(venv_path)

# Add the app directories to sys.path
app_dirs = [
    os.path.join(project_root, 'main_app'),
    os.path.join(project_root, 'cart'),
    os.path.join(project_root, 'products'),
]
for dir in app_dirs:
    if dir not in sys.path:
        sys.path.append(dir)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mitush.settings')
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as err:
        # fall back to sys.exit so that if something goes wrong during imports
        # execution doesn't stop too.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH?"
        ) from err
