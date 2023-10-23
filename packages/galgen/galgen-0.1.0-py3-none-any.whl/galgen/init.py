import yaml
import shutil
import pkg_resources
from pathlib import Path
from galgen import CONFIG_NAME

def init_action(path, force):
    path = Path(path)
    title = str(path.absolute().name).capitalize()
    galleries = [{'path': str(f.relative_to(path)), 'title': str(f.name).capitalize()}
                 for f in sorted(path.iterdir()) if f.is_dir()]

    if not len(galleries):
        raise RuntimeError(f'At least one directory expected in {path}')
    elif len(galleries) == 1:
        galleries[0]['title'] = ''
    
    config = dict(title=title, galleries=galleries)
    config_path = path / CONFIG_NAME

    template_src_path = pkg_resources.resource_filename('galgen', 'index.html.j2')
    template_dst_path = path / Path(template_src_path).name
        
    if not force and (config_path.exists() or template_dst_path.exists()):
        raise RuntimeError('Gallery already initialized. Use -f to overwrite.')
    
    with config_path.open('w') as f:
        f.write(yaml.dump(config, sort_keys=False))
    
    shutil.copyfile(template_src_path, template_dst_path)
