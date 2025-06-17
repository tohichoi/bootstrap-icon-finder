import os
import json

def generate_fontawesome_icon_json(base_path):
    """
    Font Awesome 아이콘 디렉토리를 스캔하여 JSON 데이터를 생성합니다.
    """
    icon_data = {
        "브랜드 및 서비스": {
            "소셜 미디어": [],
            "결제 및 금융": [],
            "오픈소스 및 라이선스": []
        },
        "일반 아이콘": {
            "숫자": [],
            "문자": [],
            "탐색 및 방향": [],
            "상태 및 피드백": [],
            "제어 및 액션": [],
            "파일 및 문서": [],
            "표시 및 뷰": []
        },
        "미디어": {
            "재생 제어": [],
            "볼륨": [],
            "카메라 및 사진": [],
            "음악": [],
            "비디오": []
        },
        "데이터 및 분석": {
            "차트": [],
            "데이터베이스": []
        },
        "장치 및 하드웨어": {
            "컴퓨터": [],
            "모바일": [],
            "기타 기기": []
        },
        "위치 및 지도": {
            "위치": [],
            "교통": []
        },
        "쇼핑 및 전자상거래": {
            "쇼핑": [],
            "화폐": []
        },
        "보안": {
            "보안": []
        },
        "날씨": {
            "날씨": []
        },
        "접근성": {
            "접근성": []
        },
        "개발 및 기술": {
            "개발": []
        },
        "의료 및 건강": {
            "의료": []
        },
        "스포츠 및 게임": {
            "스포츠/게임": []
        },
        "동물": {
            "동물": []
        },
        "파일 유형": {
            "문서 형식": []
        },
        "텍스트 편집": {
            "서식 지정": [],
            "정렬/목록": [],
            "텍스트 도구": []
        },
        "시간 및 날짜": {
            "달력/시계": []
        },
        "종교 및 문화": {
            "종교": []
        },
        "사람 및 사용자": {
            "사람": []
        },
        "음식 및 음료": {
            "음식": [],
            "음료": []
        },
        "일상 및 생활": {
            "집/가구": [],
            "의류/패션": [],
            "도구 및 장비": [],
            "기타": []
        }
    }

    # Font Awesome 아이콘 경로
    fa_base_path = os.path.join(base_path, 'icons', 'fontawesome-free-6.7.2-web', 'svgs')

    # Font Awesome Solid
    fa_solid_path = os.path.join(fa_base_path, 'solid')
    if os.path.exists(fa_solid_path):
        for filename in os.listdir(fa_solid_path):
            if filename.endswith('.svg'):
                icon_name = os.path.splitext(filename)[0]
                # 각 카테고리에 맞는 아이콘을 직접 분류 (이 부분은 수동으로 매칭 필요)
                # 여기서는 임시로 '기타'에 넣고, 실제 분류는 수동으로 업데이트해야 합니다.
                # 편의를 위해 '일반 아이콘 - 제어 및 액션'에 우선 넣어둠 (가장 많은 일반 아이콘이 들어갈 가능성 높음)
                icon_data["일반 아이콘"]["제어 및 액션"].append(f"fa-solid-{icon_name}")
        icon_data["일반 아이콘"]["제어 및 액션"].sort()

    # Font Awesome Regular
    fa_regular_path = os.path.join(fa_base_path, 'regular')
    if os.path.exists(fa_regular_path):
        for filename in os.listdir(fa_regular_path):
            if filename.endswith('.svg'):
                icon_name = os.path.splitext(filename)[0]
                # 편의를 위해 '일반 아이콘 - 파일 및 문서'에 우선 넣어둠
                icon_data["일반 아이콘"]["파일 및 문서"].append(f"fa-regular-{icon_name}")
        icon_data["일반 아이콘"]["파일 및 문서"].sort()

    # Font Awesome Brands
    fa_brands_path = os.path.join(fa_base_path, 'brands')
    if os.path.exists(fa_brands_path):
        for filename in os.listdir(fa_brands_path):
            if filename.endswith('.svg'):
                icon_name = os.path.splitext(filename)[0]
                icon_data["브랜드 및 서비스"]["소셜 미디어"].append(f"fa-brands-{icon_name}")
        icon_data["브랜드 및 서비스"]["소셜 미디어"].sort()

    return icon_data

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    generated_data = generate_fontawesome_icon_json(current_directory)

    # 생성된 데이터를 fontawesome-tree.json 파일로 저장
    output_file_path = os.path.join(current_directory, 'fontawesome-icon-tree.json')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(generated_data, f, ensure_ascii=False, indent=2)

    print(f"'{output_file_path}' 파일이 성공적으로 생성되었습니다.")
    print("생성된 JSON 파일의 카테고리가 정확한지 확인하고 필요시 수동으로 조정해주세요.")
    print("특히 'icons/fontawesome-free-6.7.2-web/svgs/' 경로가 정확한지 확인해주세요.")
