import copy
from pathlib import Path
import re
from typing import OrderedDict
import requests
import networkx as nx
from collections import OrderedDict, defaultdict
from bs4 import BeautifulSoup
import yaml
import json
import logging
from icon_info import IconInfo


# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_icon_info():
    icon_infos = OrderedDict()
    icon_list_files = ['bootstrap-icon-list.txt', 'fontawesome-icon-list.txt']
    for icon_list_file in icon_list_files:
        paths = [ Path(i.strip()) for i in open(icon_list_file, 'r').readlines() ]
        for path in paths:
            ii = IconInfo(path)
            icon_infos[ii.icon_class] = ii

    # for icon_name, icon_info in icon_infos.items():
    #     print(icon_info)
    # print(icon_name_to_infos)

    return icon_infos


def get_bi_taxanomy_from_web(icon_info: IconInfo):
    base_url = 'https://icons.getbootstrap.com/icons/'
    url = base_url + icon_info.icon_name + '/'

    try:
        response = requests.get(url)
        html_content = response.text

        bs = BeautifulSoup(html_content, 'html.parser')
        
        h1=bs.find_all('h1')[0]
        lis=h1.parent.ul.find_all('li')

        # friendly name
        icon_info.friendly_name = h1.text.strip()
        # tags
        icon_info.tags = [ s.strip() for s in re.sub(r'Tags: ', '', lis[0].text).split(', ') ]
        # categories
        icon_info.categories = re.sub('Category: ', '', lis[1].text).strip()

        return icon_info
        # #content > div.row.align-items-md-center > div.col-md-6.col-lg-8 > ul
        # print(html_content)
    except Exception as e:
        logger.error(e)
        return None


def get_fa_categories(force_refresh=False):
    path = Path('icons/fontawesome-free-6.7.2-web/metadata/categories.yml')
    import yaml
    with open(path, 'r') as f:
        fa_categories = yaml.safe_load(f)
    return fa_categories


def get_fa_taxanomy_from_file(icon_info: IconInfo):
    categories = get_fa_categories()


def parse_markdown_with_front_matter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 프론트 매터 구분자 (---)를 기준으로 분리
    parts = content.split('---', 2) # 첫 두 개의 ---까지만 분리

    if len(parts) >= 3 and not parts[0].strip(): # 첫 부분이 비어있고, 구분자가 두 개 이상일 때
        front_matter_str = parts[1].strip()
        markdown_body = parts[2].strip()
        
        try:
            # Remove resolver for bool so 'no', 'yes', etc. are loaded as strings
            for ch in "yYnNoO":
                if ch in yaml.SafeLoader.yaml_implicit_resolvers:
                    yaml.SafeLoader.yaml_implicit_resolvers[ch] = [
                        x for x in yaml.SafeLoader.yaml_implicit_resolvers[ch]
                        if x[0] != 'tag:yaml.org,2002:bool'
                    ]
            metadata = yaml.safe_load(front_matter_str)
        except yaml.YAMLError as e:
            logger.error(f"YAML 파싱 오류: {e}")
            metadata = {} # 파싱 실패 시 빈 딕셔너리 반환
    else:
        # 프론트 매터가 없거나 형식이 맞지 않는 경우
        metadata = {}
        markdown_body = content.strip()

    return metadata, markdown_body

# arrow-left.md 파일 생성 (예시)
def load_bootstrap_categories():
    icon_infos = defaultdict(list)
    logger.info('[BI] Reading icon categories & tags')
    path = Path('icons/src/bootstrap-icons/docs/content/icons/')
    for p in path.glob('*.md'):
        # 파일 파싱 실행
        metadata, body = parse_markdown_with_front_matter(p)
        # {'title': 'Arrow left', 'categories': ['Arrows'], 'tags': ['arrow']}
        
        icon_info = IconInfo(icon_path=p)
        cat = metadata.get('categories', [])
        icon_info.categories = [ s.capitalize() for s in list(set(cat if cat else [])) ]
        tags = metadata.get('tags', [])
        icon_info.tags = [ s.capitalize() for s in list(set(tags if tags else [])) ]
        title = metadata.get('title', '')
        icon_info.friendly_name = title if title else icon_info.icon_name
        icon_infos[icon_info.icon_name].append(icon_info)

    return icon_infos


def get_icon_file_paths(icon_name, vendor):
    paths = []
    if vendor == 'bi':
        path = Path(f'icons/src/fontawesome-free-6.7.2-web/svgs/{prefix}/') / (icon_name + '.svg')
        if path.exists():
            paths.append(path)
        return paths
    elif vendor == 'fa':
        for prefix in ['solid', 'regular', 'brands']:
            path = Path(f'icons/src/fontawesome-free-6.7.2-web/svgs/{prefix}/') / (icon_name + '.svg')
            if path.exists():
                paths.append(path)
        return paths
    else:
        return None


def load_fontawesome_categories():
    icon_infos = defaultdict(list)

    # family, style
    logger.info('[FA] Reading icon families')
    path = Path('icons/src/fontawesome-free-6.7.2-web/metadata/icon-families.yml')
    with open(path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
        for icon_name, values in metadata.items():
            styles = [ x['style'] for x in values['familyStylesByLicense']['free']]
            icon_paths = get_icon_file_paths(icon_name, 'fa')
            for icon_path in icon_paths:
                icon_info = IconInfo(icon_path=icon_path)
                icon_info.tags = [s.capitalize() for s in set(values['search']['terms'])]
                icon_info.friendly_name = icon_name
                icon_info.styles = set(styles)
                icon_infos[icon_info.icon_name].append(icon_info)

    # categories
    logger.info('[FA] Reading icon categories')
    path = Path('icons/src/fontawesome-free-6.7.2-web/metadata/categories.yml')
    with open(path, 'r') as f:
        metadata = yaml.safe_load(f)
        for category, icons in metadata.items():
            for icon_name in icons['icons']:
                ii = icon_infos.get(icon_name, None)
                if ii:
                    for i in ii:
                        i.categories.add(category.capitalize())
                else:
                    icon_paths = get_icon_file_paths(icon_name, 'fa')
                    for icon_path in icon_paths:
                        icon_info = IconInfo(icon_path=icon_path)
                        icon_info.categories = [s.capitalize() for s in set([category])]
                        icon_info.friendly_name = icons['label']
                        icon_infos[icon_info.icon_name].append(icon_info)

    # tags
    logger.info('[FA] Reading icon tags')
    path = Path('icons/src/fontawesome-free-6.7.2-web/metadata/icons.yml')
    with open(path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
        for icon_name, values in metadata.items():
            tags = set(values['search']['terms'])
            try:
                for ii in icon_infos[icon_name]:
                    ii.tags = [ s.capitalize() for s in set(ii.tags).union(tags) ]
            except KeyError:
                logger.error(f"Icon not found: {icon_name}")
                continue

    return icon_infos


if __name__ == "__main__":
    icon_infos = load_bootstrap_categories()
    icon_infos.update(load_fontawesome_categories())

    # print(icon_infos['left'])

    def icon_info_to_dict(icon_info):
        return {
            'vendor': icon_info.vendor,
            'file_name': icon_info.file_name,
            'file_path': str(icon_info.file_path.as_posix()) if hasattr(icon_info, 'file_path') else None,
            'icon_name': icon_info.icon_name,
            'icon_class': icon_info.icon_class,
            'categories': list(getattr(icon_info, 'categories', [])),
            'tags': list(getattr(icon_info, 'tags', [])),
            'styles': list(getattr(icon_info, 'styles', [])) if hasattr(icon_info, 'styles') else [],
            'friendly_name': getattr(icon_info, 'friendly_name', None),
        }

    output = {}
    for icon_name, infos in icon_infos.items():
        output[icon_name] = [icon_info_to_dict(ii) for ii in infos]

    with open('./icon_info.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
