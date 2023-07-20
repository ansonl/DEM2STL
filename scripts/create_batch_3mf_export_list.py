import os

regionsTopDir = 'K:/USAofPlasticv1/release_250m_v1/'
regionList = os.listdir(regionsTopDir)
excludeList = []

def get_dir_size(path='.', exclude3MF=True):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                if entry.name.endswith('.stl'):
                    total += entry.stat().st_size
                if exclude3MF and entry.name.endswith('transparent.3mf'):
                    excludeList.append(path[path.rfind('/')+1:])
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

regionList.sort(key=lambda f: get_dir_size(regionsTopDir+f), reverse=False)

excludeList.sort(key=lambda f: get_dir_size(regionsTopDir+f, False), reverse=False)
