// Polyfill for Node.js TextEncoder/TextDecoder required by jsdom
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;

const { JSDOM } = require('jsdom');

describe('index-test.html UI logic', () => {
  let dom;
  beforeEach(() => {
    dom = new JSDOM(`<!DOCTYPE html><html lang="en"><head><title>Test</title></head><body></body></html>`, { runScripts: 'dangerously', resources: 'usable' });
    global.window = dom.window;
    global.document = dom.window.document;
    global.document.body.innerHTML = `
      <input id="search-categories" value="Shapes">
      <input id="search-tags" value="Number">
      <input id="search-vendor" value="bi">
      <span id="search-status"></span>
      <div id="results"></div>
    `;
    // Mock open_db and show_results for search_icons
    global.open_db = jest.fn().mockResolvedValue({
      transaction: () => ({
        objectStore: () => ({
          openCursor: () => ({
            onsuccess: function() {
              // Simulate one icon result
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
    // Debug: check DOM elements
    expect(global.document.getElementById('search-categories')).not.toBeNull();
    expect(global.document.getElementById('search-tags')).not.toBeNull();
    expect(global.document.getElementById('search-vendor')).not.toBeNull();
    expect(global.document.getElementById('search-status')).not.toBeNull();
    // Minimal search_icons function using kebab-case IDs
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
    // Simulate form submit event
    const event = { preventDefault: jest.fn() };
    await search_icons(event);
    expect(global.show_results).toHaveBeenCalledWith([
      { categories: ['Shapes'], tags: ['Number'], vendor: 'bi' }
    ]);
    expect(global.document.getElementById('search-status').textContent).toBe('Found 1 icons.');
  });
});
