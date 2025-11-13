import xml.etree.ElementTree as ET
import urllib.request
import gzip
import io

config = ET.parse('config.xml').getroot()
params = {elem.tag: elem.text for elem in config}

packages_to_analyze = ["nginx", "python3", "git"]
repo = params['repo']

def get_package_dependencies(package_name):
    try:
        url = f"{repo}/main/binary-amd64/Packages.gz"
        with urllib.request.urlopen(url) as response:
            data = gzip.decompress(response.read()).decode()
        
        deps = []
        target = "nginx-core" if package_name == "nginx" else package_name
        
        for block in data.split('\n\n'):
            if f"Package: {target}" in block:
                for line in block.split('\n'):
                    if line.startswith('Depends:'):
                        for dep in line[8:].split(','):
                            dep = dep.split('(')[0].split('|')[0].split(':')[0].strip()
                            if dep and dep != target and dep not in deps:
                                deps.append(dep)
                break
        return deps
    except Exception as e:
        return []

all_data = {}
for package in packages_to_analyze:
    deps = get_package_dependencies(package)
    all_data[package] = deps

plantuml_code = "@startuml\nleft to right direction\n"

common_deps = {}
for package, deps in all_data.items():
    for dep in deps:
        if dep not in common_deps:
            common_deps[dep] = []
        common_deps[dep].append(package)

for package in packages_to_analyze:
    plantuml_code += f'rectangle "{package}"\n'

for dep, packages in common_deps.items():
    plantuml_code += f'rectangle "{dep}"\n'
    for package in packages:
        plantuml_code += f'"{package}" --> "{dep}"\n'

plantuml_code += "@enduml"

with open("graph.puml", "w", encoding="utf-8") as f:
    f.write(plantuml_code)

print("graph.puml")
