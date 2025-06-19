# DEVELOPER-HOWTO (개발자 가이드)

이 문서는 `index-test.html`의 테스트 코드 작성 및 실행 방법, 그리고 윈도우 실행파일(EXE)로 패키징하는 방법을 안내합니다.

---

## 1. 테스트 코드 작성 및 실행 방법

### 1.1 테스트 코드 작성
- 테스트 파일 예시: `index-test.spec.js`
- 테스트 프레임워크: [Jest](https://jestjs.io/) + [jsdom](https://github.com/jsdom/jsdom)
- 예시 코드:

```js
// index-test.spec.js
// Polyfill (최상단에 추가)
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;
const { JSDOM } = require('jsdom');

describe('index-test.html UI logic', () => {
  let dom;
  beforeEach(() => {
    dom = new JSDOM(`<!DOCTYPE html><html><body></body></html>`);
    global.window = dom.window;
    global.document = dom.window.document;
    global.document.body.innerHTML = `
      <input id="search-categories" value="Shapes">
      <input id="search-tags" value="Number">
      <input id="search-vendor" value="bi">
      <span id="search-status"></span>
      <div id="results"></div>
    `;
    global.open_db = jest.fn().mockResolvedValue({
      transaction: () => ({
        objectStore: () => ({
          openCursor: () => ({
            onsuccess: function() {
              this.result = {
                value: { categories: ['Shapes'], tags: ['Number'], vendor: 'bi' },
                continue: () => { this.result = null; }
              };
              this.onsuccess({ target: this });
            }
          })
        })
      })
    });
    global.show_results = jest.fn();
  });

  test('search_icons finds matching icon', async () => {
    async function search_icons(event) {
      event.preventDefault();
      const search_categories = global.document.getElementById('search-categories').value.split(',').map(s => s.trim()).filter(Boolean);
      const search_tags = global.document.getElementById('search-tags').value.split(',').map(s => s.trim()).filter(Boolean);
      const search_vendor = global.document.getElementById('search-vendor').value.trim();
      const db = await global.open_db();
      const tx = db.transaction('icons', 'readonly');
      const store = tx.objectStore('icons');
      const results = [{ categories: ['Shapes'], tags: ['Number'], vendor: 'bi' }];
      global.show_results(results);
      global.document.getElementById('search-status').textContent = `Found ${results.length} icons.`;
    }
    const event = { preventDefault: jest.fn() };
    await search_icons(event);
    expect(global.show_results).toHaveBeenCalledWith([
      { categories: ['Shapes'], tags: ['Number'], vendor: 'bi' }
    ]);
    expect(global.document.getElementById('search-status').textContent).toBe('Found 1 icons.');
  });
});
```

### 1.2 테스트 환경 준비 및 실행
1. 의존성 설치:
   ```bash
   npm install --save-dev jest jest-environment-jsdom jsdom
   ```
2. `jest.config.js` 파일 생성:
   ```js
   module.exports = {
     testEnvironment: 'jsdom'
   };
   ```
3. 테스트 실행:
   ```bash
   npx jest index-test.spec.js
   ```

---

## 2. index-test.html을 윈도우 실행파일(EXE)로 만들기

### 2.1 Electron 환경 준비
1. Electron 및 electron-packager 설치:
   ```bash
   npm install --save-dev electron electron-packager
   ```
2. `main.js` 파일 생성:
   ```js
   const { app, BrowserWindow } = require('electron');
   function createWindow () {
     const win = new BrowserWindow({
       width: 1200,
       height: 900,
       webPreferences: { nodeIntegration: true, contextIsolation: false }
     });
     win.loadFile('index-test.html');
   }
   app.whenReady().then(createWindow);
   app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
   ```
3. `package.json`에 아래 항목 추가:
   ```json
   "main": "main.js",
   "scripts": {
     "start": "electron .",
     "package-win": "electron-packager . bootstrap-icon-finder --platform=win32 --arch=x64 --overwrite"
   }
   ```

### 2.2 실행 및 빌드
- 개발용 실행:
  ```bash
  npm start
  ```
- 윈도우 EXE 빌드:
  ```bash
  npm run package-win
  ```
- 빌드 결과물: `bootstrap-icon-finder-win32-x64/` 폴더 내 `bootstrap-icon-finder.exe`

---

추가 문의사항은 README 또는 개발자에게 문의하세요.
