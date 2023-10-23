import yaml
import webbrowser
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from galgen import CONFIG_NAME

def build_action(path, force, show):
    path = Path(path)
    index_path = Path(path) / 'index.html'
    environment = Environment(loader=FileSystemLoader(path))
    template = environment.get_template("index.html.j2")
    config = yaml.safe_load((path / CONFIG_NAME).read_text())

    def list_images(path):
        thumbnails_path = path / 'thumbnails'
        if not thumbnails_path.exists():
            thumbnails_path = path
            
        images = [dict(image=f, thumb=thumbnails_path / f.name )
                for f in sorted(path.iterdir()) if f.is_file()]
        
        if not images:
            raise RuntimeError(f'At least one image expected in {path}')

        return images

    galleries = [dict(title=gallery['title'], images=list_images(path / gallery['path']))
                for gallery in config['galleries']]

    params = dict(title=config['title'], galleries=galleries)
    
    if not force and index_path.exists():
        raise RuntimeError('Gallery already built. Use -f to overwrite.')
    
    template.stream(**params).dump(str(index_path))

    if show:
        webbrowser.open(f'file://{index_path.absolute()}')
