import xml.etree.ElementTree as ET
import urllib.request
import gzip
import io

config = ET.parse('config.xml').getroot()
params = {elem.tag: elem.text for elem in config}

print("Config:")
for k, v in params.items():
    print(f"  {k}: {v}")
package = params['package']
repo = params['repo']
version = params.get('version', '')

try:
    url = f"{repo}/main/binary-amd64/Packages.gz"
    with urllib.request.urlopen(url) as response:
        data = gzip.decompress(response.read()).decode()
    deps = []
    
    target_package = "nginx-core" if package == "nginx" else package
    package_found = False
    available_versions = []
    
    for block in data.split('\n\n'):
        if f"Package: {target_package}" in block:
            # Ищем версию в блоке
            block_version = None
            for line in block.split('\n'):
                if line.startswith('Version: '):
                    block_version = line[9:].strip()
                    available_versions.append(block_version)
                    
                    # Проверяем совпадение версии
                    if version in block_version:  # Ищем частичное совпадение
                        package_found = True
                        # Парсим зависимости
                        for dep_line in block.split('\n'):
                            if dep_line.startswith('Depends:'):
                                for dep in dep_line[8:].split(','):
                                    dep = dep.split('(')[0].split('|')[0].split(':')[0].strip()
                                    if dep and dep not in deps and dep != target_package:
                                        deps.append(dep)
                        break
            break
    
    if not package_found:
        if available_versions:
            print(f"\nError: Version '{version}' not found for {package}")
            print(f"Available versions: {', '.join(available_versions)}")
        else:
            print(f"\nError: Package {package} not found in repository")
    else:
        print(f"\nReal dependencies of {package} {version}:")
        for dep in deps:
            print(f"  - {dep}")

except Exception as e:
    print(f"Error: {e}")
