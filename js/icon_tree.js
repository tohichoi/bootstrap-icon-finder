document.addEventListener('DOMContentLoaded', () => {
    const iconTreeContainer = document.getElementById('icon-tree');

    /**
     * SVG 파일 경로를 결정하는 헬퍼 함수
     * @param {string} fullIconName - icon-tree.json에 있는 아이콘 이름 (예: "bs-arrow-right", "fa-solid-bell")
     * @returns {string|null} - SVG 파일 경로 또는 null (경로를 찾을 수 없을 때)
     */
    async function getSvgPath(fullIconName) {
        let svgPath = [];
        let iconName = ''; // 실제 SVG 파일 이름 부분

        if (fullIconName.startsWith('bs-')) {
            iconName = fullIconName.substring(3); // "bs-" 제거
            svgPath.push(`icons/bootstrap-icons-1.9.1/${iconName}.svg`);
        } else if (fullIconName.startsWith('fa-')) {
            iconName = fullIconName.substring(3); // "fa-solid-" 제거
            ['solid', 'regular', 'brands'].forEach(prefix => {
                svgPath.push(`icons/fontawesome-free-6.7.2-web/svgs/${prefix}/${iconName}.svg`);
            });
        } else {
            console.warn(`Unknown icon prefix for: ${fullIconName}`);
            return null; // 알 수 없는 접두사
        }

        svgPath.filter(path => async function() {
            const response = await fetch(path, { method: 'HEAD' });
            if (!response.ok) {
                console.warn(`SVG file ${path} not found at ${svgPath} for icon: ${fullIconName}`);
                return null;
            }
            return path; // 유효한 경로만 반환
        })

        return svgPath;
    }

    /**
     * AJAX를 통해 icon-tree.json 파일을 불러옵니다.
     * @returns {Promise<Object|null>} JSON 데이터를 resolve하는 Promise 또는 null (에러 시).
     */
    async function fetchIconTreeData() {
        try {
            const response = await fetch('./icon-tree.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Failed to load icon categories:", error);
            iconTreeContainer.innerHTML = '<p style="color: red;">아이콘 데이터를 불러오는 데 실패했습니다. 콘솔을 확인해주세요.</p>';
            return null;
        }
    }

    /**
     * JSON 데이터를 기반으로 아이콘 트리를 동적으로 생성합니다.
     * @param {Object} data - 아이콘 분류 JSON 데이터.
     * @param {HTMLElement} parentElement - 트리가 추가될 부모 DOM 요소.
     * @param {number} level - 현재 트리의 깊이 (들여쓰기 조절용).
     */
    function buildTree(data, parentElement, level = 0) {
        const ul = document.createElement('ul');
        ul.classList.add('tree-level-' + level);

        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                const li = document.createElement('li');
                li.classList.add('tree-node');

                const titleSpan = document.createElement('span');
                titleSpan.classList.add('tree-node-title');

                // 모든 카테고리 노드 (하위 카테고리나 아이콘 목록을 가지는 노드)에 토글 아이콘 추가
                if (typeof data[key] === 'object' && data[key] !== null && (Object.keys(data[key]).length > 0 || Array.isArray(data[key]))) {
                    const toggleIcon = document.createElement('i');
                    toggleIcon.classList.add('toggle-icon', 'fa-solid', 'fa-caret-right'); // Font Awesome 화살표 아이콘 사용
                    titleSpan.appendChild(toggleIcon);
                    li.classList.add('collapsed'); // 기본적으로 접힌 상태로 시작
                }

                titleSpan.innerHTML += key; // 카테고리 이름 추가
                li.appendChild(titleSpan);

                // 하위 카테고리 또는 아이콘 목록을 재귀적으로 처리
                if (typeof data[key] === 'object' && !Array.isArray(data[key])) {
                    // 하위 카테고리 (객체)
                    buildTree(data[key], li, level + 1);
                } else if (Array.isArray(data[key])) {
                    // 아이콘 목록 (배열)
                    const iconListDiv = document.createElement('div');
                    iconListDiv.classList.add('icon-list');

                    // 모든 아이콘을 비동기적으로 로드
                    data[key].forEach(async fullIconName => {
                        const iconItem = document.createElement('div');
                        iconItem.classList.add('icon-item');
                        iconItem.dataset.fullIconName = fullIconName; // 전체 아이콘 이름 저장

                        const svgPaths = await getSvgPath(fullIconName); // 정확한 SVG 경로 가져오기

                        if (svgPaths.length > 0) {
                            for (const svgPath of svgPaths) {
                                try {
                                    const response = await fetch(svgPath);
                                    if (response.ok) {
                                        const svgContent = await response.text();
                                        const imgElement = document.createElement('img');
                                        imgElement.src = `data:image/svg+xml;base64,${btoa(svgContent)}`;
                                        imgElement.alt = fullIconName;
                                        imgElement.title = fullIconName; // 툴팁으로 전체 아이콘 이름 표시
                                        iconItem.appendChild(imgElement);
                                    } else {
                                        // continue;
                                        const errorSpan = document.createElement('span');
                                        errorSpan.textContent = `🚫 ${fullIconName}`;
                                        errorSpan.style.color = 'red';
                                        iconItem.appendChild(errorSpan);
                                        console.warn(`Failed to load SVG content for ${fullIconName} from ${svgPath}. Status: ${response.status}`);
                                    }
                                } catch (error) {
                                    const errorSpan = document.createElement('span');
                                    errorSpan.textContent = `❌ ${fullIconName}`;
                                    errorSpan.style.color = 'red';
                                    iconItem.appendChild(errorSpan);
                                    console.error(`Error fetching SVG content for ${fullIconName}:`, error);
                                    continue;
                                }
                            }
                        } else {
                            const missingSpan = document.createElement('span');
                            missingSpan.textContent = `? ${fullIconName}`;
                            missingSpan.style.color = '#888';
                            iconItem.appendChild(missingSpan);
                            console.warn(`SVG path not resolved for icon: ${fullIconName}`);
                        }

                        // 아이콘 이름 텍스트 (접두사 포함)
                        const iconNameSpan = document.createElement('span');
                        iconNameSpan.textContent = fullIconName;
                        iconItem.appendChild(iconNameSpan);

                        iconListDiv.appendChild(iconItem);
                    });
                    li.appendChild(iconListDiv);
                }
                ul.appendChild(li);
            }
        }
        parentElement.appendChild(ul);
    }

    /**
     * 트리 노드 토글 이벤트 핸들러.
     * @param {Event} event - 클릭 이벤트 객체.
     */
    function handleTreeToggle(event) {
        const target = event.target.closest('.tree-node-title');
        if (!target) return;

        const listItem = target.closest('.tree-node');
        if (!listItem) return;

        const hasToggleIcon = listItem.querySelector('.toggle-icon');

        if (hasToggleIcon) {
            listItem.classList.toggle('collapsed');
            listItem.classList.toggle('expanded');

            const childUl = listItem.querySelector(':scope > ul');
            const childIconList = listItem.querySelector(':scope > .icon-list');

            if (childIconList) {
                childIconList.classList.toggle('open');
            }
        }
    }

    // 초기 데이터 로드 및 트리 생성
    fetchIconTreeData().then(data => {
        if (data) {
            iconTreeContainer.innerHTML = ''; // 로딩 메시지 제거
            buildTree(data, iconTreeContainer);
            // 트리 토글 이벤트 리스너는 여전히 필요
            iconTreeContainer.addEventListener('click', handleTreeToggle);
        }
    });
});