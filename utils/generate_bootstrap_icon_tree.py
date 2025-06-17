import os
import json

def generate_bootstrap_icon_json(file_path):
    """
    Bootstrap 아이콘 목록 파일을 읽어 JSON 데이터를 생성합니다.
    """
    icon_data = {
        "일반 UI": {
            "파일/문서": [],
            "탐색/방향": [],
            "상태/피드백": [],
            "제어/액션": [],
            "표시/뷰": [],
            "시간/날짜": []
        },
        "미디어": {
            "재생 제어": [],
            "볼륨": [],
            "카메라/사진": [],
            "음악": []
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
            "잠금": [],
            "보안": []
        },
        "날씨": {
            "날씨": []
        },
        "접근성": {
            "접근성": []
        },
        "브랜드 및 서비스": {
            "소셜 미디어": [],
            "결제 및 금융": []
        },
        "텍스트 편집": {
            "서식 지정": [],
            "정렬/목록": [],
            "텍스트 도구": []
        },
        "일상 및 생활": {
            "집/가구": [],
            "의류/패션": [],
            "도구 및 장비": [],
            "기타": []
        }
    }

    # 아이콘 분류를 위한 키워드 기반 매핑 (icon_data 구조와 일치하도록 수정)
    category_keywords = {
        "일반 UI": {
            "파일/문서": ["file", "folder", "document", "paperclip", "archive", "clipboard", "journal", "postcard", "receipt"],
            "탐색/방향": ["arrow", "chevron", "caret", "box-arrow", "angle", "move", "return", "clockwise", "counterclockwise", "expand", "collapse", "fullscreen", "home", "door", "back"],
            "상태/피드백": ["check", "x-circle", "info", "exclamation", "question", "bell", "star", "heart", "thumbs", "award", "alert", "badge", "circle-fill", "slash-circle", "patch"],
            "제어/액션": ["plus", "dash", "minus", "power", "gear", "sliders", "filter", "trash", "bookmark", "wrench", "hammer", "lightbulb", "play", "pause", "stop", "record", "fast-forward", "rewind", "skip", "repeat", "shuffle", "upload", "download", "save", "cut", "copy", "paste", "crop", "rotate", "reload", "recycle", "eject", "print", "plug", "bolt", "magnet", "pencil", "pen", "eraser", "paint", "brush", "bucket", "eye-dropper", "command", "option", "tools", "screwdriver", "scissors", "toggle", "switch", "qr-code", "scan"],
            "표시/뷰": ["eye", "display", "monitor", "screen", "webcam", "binoculars", "fullscreen"],
            "시간/날짜": ["calendar", "clock", "hourglass", "alarm", "stopwatch", "timer"]
        },
        "미디어": {
            "재생 제어": ["play", "pause", "stop", "record", "fast-forward", "rewind", "skip", "shuffle", "repeat"],
            "볼륨": ["volume", "speaker", "mic"],
            "카메라/사진": ["camera", "image", "images", "photo", "film", "video", "aspect-ratio"],
            "음악": ["music", "headphones", "headset", "earbuds", "boombox", "cassette", "disc", "soundwave"]
        },
        "데이터 및 분석": {
            "차트": ["chart", "graph", "bar-chart", "pie-chart", "diagram"],
            "데이터베이스": ["database", "server", "hdd", "ssd", "memory", "cpu"]
        },
        "장치 및 하드웨어": {
            "컴퓨터": ["computer", "desktop", "laptop", "pc", "motherboard", "cpu", "gpu", "monitor", "keyboard", "mouse", "modem", "router", "terminal"],
            "모바일": ["mobile", "phone", "tablet", "sim-card"],
            "기타 기기": ["calculator", "joystick", "controller", "plug", "power", "radio", "satellite", "smartwatch", "tv", "vr", "webcam"]
        },
        "위치 및 지도": {
            "위치": ["geo", "map", "pin", "house", "building", "hospital", "bank", "shop", "city", "campground", "church", "landmark"],
            "교통": ["car", "truck", "airplane", "bicycle", "bus", "train", "ferry", "ship", "motorcycle", "taxi", "traffic-light", "fuel-pump", "ev-station", "minecart"]
        },
        "쇼핑 및 전자상거래": {
            "쇼핑": ["bag", "basket", "cart", "gift", "receipt", "tag", "tags"],
            "화폐": ["currency", "cash", "coin", "bitcoin", "dollar", "euro", "pound", "yen", "rupee", "bank", "piggy-bank", "credit-card"]
        },
        "보안": {
            "잠금": ["lock", "unlock"],
            "보안": ["shield", "key", "fingerprint", "bug", "virus", "eye-slash"]
        },
        "날씨": {
            "날씨": ["cloud", "sun", "moon", "rain", "snow", "wind", "storm", "drizzle", "fog", "hail", "lightning", "thermometer", "umbrella", "hurricane", "tornado", "water", "droplet"],
        },
        "접근성": {
            "접근성": ["accessible", "wheelchair", "universal-access", "ear", "blind", "low-vision", "tty"]
        },
        "브랜드 및 서비스": {
            "소셜 미디어": ["facebook", "twitter", "instagram", "youtube", "linkedin", "github", "discord", "behance", "dribbble", "pinterest", "reddit", "skype", "slack", "snapchat", "spotify", "steam", "telegram", "tiktok", "twitch", "vimeo", "whatsapp", "wordpress", "xbox", "yelp", "quora", "wechat", "alipay", "google-play"],
            "결제 및 금융": ["credit-card", "paypal", "bitcoin", "currency", "cash", "bank"]
        },
        "텍스트 편집": {
            "서식 지정": ["type", "bold", "italic", "underline", "strikethrough", "indent", "unindent"],
            "정렬/목록": ["align", "list", "justify", "columns", "grid", "distribute"],
            "텍스트 도구": ["font", "paragraph", "textarea", "spellcheck"]
        },
        "일상 및 생활": {
            "집/가구": ["house", "door", "bed", "chair", "couch"],
            "의류/패션": ["shirt", "bag", "hat"],
            "도구 및 장비": ["tools", "wrench", "hammer", "screwdriver", "scissors", "brush", "paint-bucket", "palette", "ruler", "magnet", "fire"],
            "기타": ["activity", "asterisk", "at", "bullseye", "braces", "bricks", "bug", "cup", "diamond", "dice", "egg", "emoji", "escape", "exclude", "explicit", "flower", "gem", "gender", "heartbreak", "heptagon", "hexagon", "hr", "hypnotize", "infinity", "intersect", "ladder", "lamp", "layer", "life-preserver", "lightbulb", "lungs", "magic", "mask", "nut", "octagon", "option", "outlet", "peace", "percent", "piggy-bank", "pin", "plugin", "puzzle", "radioactive", "rainbow", "robot", "rulers", "safe", "send", "segmented-nav", "shield", "shop-window", "sign", "signal", "smartwatch", "snow", "sort", "soundwave", "speedometer", "square-half", "stack", "star-half", "stars", "stickies", "sticky", "subtract", "suit", "sunglasses", "sunrise", "sunset", "symmetry", "table", "tag-fill", "tags-fill", "telephone", "terminal", "text", "three-dots", "thunderbolt", "ticket", "toggles", "tree", "triangle", "trophy", "tropical-storm", "tsunami", "union", "upc", "valentine", "vector-pen", "view", "vinyl", "virus", "voicemail", "wallet", "watch", "wechat", "windows", "wrench-adjustable", "x"]
        }
    }

    with open(file_path, 'r', encoding='utf-8') as f:
        icons = [line.strip().replace('.svg', '') for line in f if line.strip()]

    # 각 아이콘을 분류
    for icon in icons:
        prefixed_icon = f"bs-{icon}"
        found = False
        for major_cat_name, major_cat_content in category_keywords.items():
            if isinstance(major_cat_content, dict):
                for sub_cat_name, keywords in major_cat_content.items():
                    if any(keyword in icon for keyword in keywords):
                        icon_data[major_cat_name][sub_cat_name].append(prefixed_icon)
                        found = True
                        break
            else: # 단일 카테고리 (하위 딕셔너리가 아닌 리스트)
                if any(keyword in icon for keyword in major_cat_content):
                    icon_data[major_cat_name].append(prefixed_icon)
                    found = True
            if found:
                break
        if not found:
            # 분류되지 않은 아이콘은 '기타' 카테고리에 추가
            icon_data["일상 및 생활"]["기타"].append(prefixed_icon)

    # 중복 제거 및 정렬
    for major_cat_name in icon_data:
        if isinstance(icon_data[major_cat_name], dict):
            for sub_cat_name in icon_data[major_cat_name]:
                icon_data[major_cat_name][sub_cat_name] = sorted(list(set(icon_data[major_cat_name][sub_cat_name])))
        else:
            icon_data[major_cat_name] = sorted(list(set(icon_data[major_cat_name])))

    return icon_data

if __name__ == "__main__":
    input_file_path = "bootstrap-icon-list-only-name.txt" # 사용자가 업로드한 파일 이름

    generated_data = generate_bootstrap_icon_json(input_file_path)

    # 생성된 데이터를 bootstrap-icon-tree.json 파일로 저장
    output_file_path = "bootstrap-icon-tree.json"
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(generated_data, f, ensure_ascii=False, indent=2)

    print(f"'{output_file_path}' 파일이 성공적으로 생성되었습니다.")
    print("생성된 JSON 파일의 카테고리가 정확한지 확인하고 필요시 수동으로 조정해주세요.")
