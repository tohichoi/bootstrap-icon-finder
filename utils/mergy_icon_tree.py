import json
import os

def merge_icon_trees(bootstrap_path, fontawesome_path, output_path):
    """
    Bootstrap과 Font Awesome 아이콘 분류 JSON 파일을 병합합니다.
    """
    merged_data = {}

    # Bootstrap 아이콘 데이터 로드
    try:
        with open(bootstrap_path, 'r', encoding='utf-8') as f:
            bootstrap_data = json.load(f)
    except FileNotFoundError:
        print(f"오류: '{bootstrap_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
        return
    except json.JSONDecodeError:
        print(f"오류: '{bootstrap_path}' 파일의 JSON 형식이 올바르지 않습니다.")
        return

    # Font Awesome 아이콘 데이터 로드
    try:
        with open(fontawesome_path, 'r', encoding='utf-8') as f:
            fontawesome_data = json.load(f)
    except FileNotFoundError:
        print(f"오류: '{fontawesome_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
        return
    except json.JSONDecodeError:
        print(f"오류: '{fontawesome_path}' 파일의 JSON 형식이 올바르지 않습니다.")
        return

    # 두 데이터 소스의 최상위 카테고리를 순회
    all_major_categories = set(bootstrap_data.keys()).union(set(fontawesome_data.keys()))

    for major_cat in all_major_categories:
        merged_data[major_cat] = {}

        # Bootstrap의 하위 카테고리 추가
        if major_cat in bootstrap_data and isinstance(bootstrap_data[major_cat], dict):
            for sub_cat, icons in bootstrap_data[major_cat].items():
                if sub_cat not in merged_data[major_cat]:
                    merged_data[major_cat][sub_cat] = []
                merged_data[major_cat][sub_cat].extend(icons)
        elif major_cat in bootstrap_data and isinstance(bootstrap_data[major_cat], list):
             # 최상위 카테고리 바로 아래 리스트인 경우 처리
            if "_default" not in merged_data[major_cat]:
                merged_data[major_cat]["_default"] = []
            merged_data[major_cat]["_default"].extend(bootstrap_data[major_cat])


        # Font Awesome의 하위 카테고리 추가 (중복 방지 및 병합)
        if major_cat in fontawesome_data and isinstance(fontawesome_data[major_cat], dict):
            for sub_cat, icons in fontawesome_data[major_cat].items():
                if sub_cat not in merged_data[major_cat]:
                    merged_data[major_cat][sub_cat] = []
                merged_data[major_cat][sub_cat].extend(icons)
        elif major_cat in fontawesome_data and isinstance(fontawesome_data[major_cat], list):
            # 최상위 카테고리 바로 아래 리스트인 경우 처리
            if "_default" not in merged_data[major_cat]:
                merged_data[major_cat]["_default"] = []
            merged_data[major_cat]["_default"].extend(fontawesome_data[major_cat])


    # 각 카테고리와 서브 카테고리 내에서 아이콘 목록 중복 제거 및 정렬
    for major_cat, sub_cats in merged_data.items():
        for sub_cat, icons in sub_cats.items():
            merged_data[major_cat][sub_cat] = sorted(list(set(icons)))

    # 빈 서브 카테고리 제거 (선택 사항)
    for major_cat in list(merged_data.keys()):
        if isinstance(merged_data[major_cat], dict):
            for sub_cat in list(merged_data[major_cat].keys()):
                if not merged_data[major_cat][sub_cat]:
                    del merged_data[major_cat][sub_cat]
            if not merged_data[major_cat]: # 모든 서브카테고리가 비어있으면 메인카테고리도 제거
                del merged_data[major_cat]
        elif isinstance(merged_data[major_cat], list) and not merged_data[major_cat]:
            del merged_data[major_cat]


    # 최종 JSON 파일로 저장
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2)
        print(f"'{output_path}' 파일이 성공적으로 생성되었습니다.")
    except IOError as e:
        print(f"오류: '{output_path}' 파일을 쓰는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # 두 아이콘 트리의 파일 경로 (현재 디렉토리에 있다고 가정)
    bootstrap_file = "bootstrap-icon-tree.json"
    fontawesome_file = "fontawesome-icon-tree.json"
    output_file = "merged-icon-tree.json"

    # 병합 함수 실행
    merge_icon_trees(bootstrap_file, fontawesome_file, output_file)
    print("생성된 JSON 파일의 카테고리가 정확한지 확인하고 필요시 수동으로 조정해주세요.")
