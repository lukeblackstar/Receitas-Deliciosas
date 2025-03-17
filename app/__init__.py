import os
import sys
from pathlib import Path

def init_app():
    """Inicializa o ambiente da aplicação."""
    
    base_dir = Path(__file__).parent

    dirs = ['data', 'images', 'utils']
    for dir_name in dirs:
        dir_path = base_dir / dir_name
        dir_path.mkdir(exist_ok=True)

    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))

init_app() 