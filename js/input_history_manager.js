/**
 * InputHistoryManager 클래스
 * - 입력 필드의 입력 기록을 관리하고 표시하는 기능을 제공합니다.
 */
class InputHistoryManager {
    /**
     * @param {string} inputId - 입력 필드의 ID.
     * @param {string} historyListId - 기록 목록을 표시할 요소의 ID.
     * @param {string} saveButtonId - 저장 버튼의 ID.
     * @param {string} messageId - 메시지를 표시할 요소의 ID. (선택적)
     * @param {number} maxHistoryLength - 최대 저장 가능한 기록 개수. (선택적, 기본값: 5)
     * @param {string} storageKey - 로컬 스토리지에 저장할 키. (선택적, 기본값: 'inputHistory')
     */
    constructor(inputId, historyListId, saveButtonId, messageId = null, maxHistoryLength = 5, storageKey = 'inputHistory') {
        this.inputElement = document.getElementById(inputId);
        this.historyListElement = document.getElementById(historyListId);
        this.saveButtonElement = document.getElementById(saveButtonId);
        this.messageElement = messageId ? document.getElementById(messageId) : null;
        this.maxHistoryLength = maxHistoryLength;
        this.storageKey = storageKey;
        this.history = [];
        this.init();
    }

    /**
     * 초기화 함수
     * - 로컬 스토리지에서 기록을 불러오고, 이벤트 리스너를 설정합니다.
     */
    init() {
        this.loadHistory();
        this.bindEvents();
        this.displayHistory(); // 초기 로드 시 기록 표시
    }

    /**
     * 로컬 스토리지에서 기록을 불러오는 함수
     */
    loadHistory() {
        if (localStorage.getItem(this.storageKey)) {
            try {
                this.history = JSON.parse(localStorage.getItem(this.storageKey));
                if (!Array.isArray(this.history)) {
                    this.history = [];
                    localStorage.removeItem(this.storageKey);
                    console.warn('잘못된 형식의 기록 데이터를 삭제했습니다.');
                }
            } catch (e) {
                console.error("로컬 스토리지에서 기록을 불러오는 중 오류 발생:", e);
                this.history = [];
                localStorage.removeItem(this.storageKey);
            }
        }
    }

    /**
     * 입력 기록을 로컬 스토리지에 저장하는 함수
     */
    saveHistory() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.history));
    }

    /**
     * 입력 기록을 화면에 표시하는 함수
     */
    displayHistory() {
        this.historyListElement.innerHTML = '';
        this.history.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            li.addEventListener('click', () => this.onHistoryItemClick(item));
            this.historyListElement.appendChild(li);
        });
        this.saveButtonElement.disabled = this.history.length >= this.maxHistoryLength;
        if (this.messageElement) {
            this.messageElement.textContent = this.history.length >= this.maxHistoryLength
                ? `최대 ${this.maxHistoryLength}개까지 저장할 수 있습니다.`
                : '';
        }
    }

    /**
     * 기록 아이템 클릭 시 처리하는 함수
     * @param {string} item - 클릭된 기록 아이템의 텍스트.
     */
    onHistoryItemClick(item) {
        this.inputElement.value = item;
        const selectedItem = this.historyListElement.querySelector('.selected');
        if (selectedItem) {
            selectedItem.classList.remove('selected');
        }
        const clickedItem = Array.from(this.historyListElement.children).find(li => li.textContent === item);
        if (clickedItem) {
            clickedItem.classList.add('selected');
        }
    }

    /**
     * 이벤트 리스너를 설정하는 함수
     */
    bindEvents() {
        this.saveButtonElement.addEventListener('click', () => this.onSaveButtonClick());
    }

    /**
     * 저장 버튼 클릭 시 처리하는 함수
     */
    onSaveButtonClick() {
        const inputText = this.inputElement.value.trim();
        if (inputText !== '') {
            this.history.unshift(inputText);
            if (this.history.length > this.maxHistoryLength) {
                this.history.pop();
            }
            this.saveHistory();
            this.inputElement.value = '';
            this.displayHistory();
        }
    }
}

// 사용 예시
// const inputHistoryManager = new InputHistoryManager('textInput', 'historyList', 'saveButton', 'message', 5);