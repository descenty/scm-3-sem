import requests
import sys
import graphviz
import re

url = 'https://registry.npmjs.org/'


def generate_graph(dependencies: dict):
    dot = graphviz.Digraph()
    nodes: list[str] = []
    for dependency in dependencies.items():
        dot.node(dependency[0], dependency[0])
        for child in dependency[1]:
            if child not in nodes:
                dot.node(child, child)
                nodes.append(child)
            dot.edge(dependency[0], child)
    dot.render(list(dependencies.items())[0][0] + '.gv')
    return dot.source


def get_max_minor_version(package_name: str, target_major: int) -> list[str]:
    versions: list[str] = list(requests.get(
        url + package_name).json()['versions'].keys())
    max_version = ''
    max_minor = 0
    for version in versions:
        major, minor = [int(x) for x in version.split('.')[:2]]
        if major != target_major:
            continue
        minor = int(version.split('.')[1])
        if minor >= max_minor:
            max_version = version
            max_minor = minor
    return max_version


def get_latest_version(package_name: str) -> str:
    return requests.get(url + package_name + '/latest').json()['version']


def get_dependencies(dependencies: dict, package_name: str, version: str = 'latest') -> None:
    response: dict = requests.get(url + package_name + '/' + version).json()
    if 'dependencies' in response:
        new_dependencies = [package_name + '@' + (get_max_minor_version(package_name, int(version.split('||')[1].replace('^', '').split('.')[0] if '||' in version else version.replace('^', '').split(
            '.')[0])) if '^' in version else (get_latest_version(package_name) if '>=' in version else re.findall(r'^[^ &|&|]+', version)[0].replace('~', ''))) for package_name, version in response['dependencies'].items()]
        dependencies[package_name + '@' +
                     response['version']] = new_dependencies
        dependency_package_name: str
        for dependency_package_name in new_dependencies:
            # if @vue/router@1.3.5
            if dependency_package_name.count('@') > 1:
                package_name, version = dependency_package_name.replace(
                    '@', '', 1).split('@')
            else:
                package_name, version = dependency_package_name.split('@')
            get_dependencies(dependencies, package_name,
                             'latest' if '^' in version else version)
    else:
        return


def main():
    package_name = sys.argv[1]
    dependencies = {}
    get_dependencies(dependencies, package_name)
    print(generate_graph(dependencies))


if __name__ == '__main__':
    main()
