function create_datepicker(ids) {
  function pass_event(el) {
    document.querySelector(el).dispatchEvent(new Event('input'));
  }
  // init date
  let date_options = {
    el: null,
    dateFormat: 'YYYY-MM-DD',
    bodyType: 'modal',
    customOkBTN: '확인',
    customCancelBTN: '취소',
    customClearBTN: '삭제'
  }
  let pickers = [];
  for (const el of ids) {
    let opt = structuredClone(date_options);
    opt.el = el;
    let dp = MCDatepicker.create(opt);
    // 날짜 변경시 oninput 이벤트가 opt.el 에 전달되지 않기 때문에 수동으로 전달
    dp.onClear(() => pass_event(opt.el));
    dp.onSelect(() => pass_event(opt.el));
    pickers.push(dp);
  }
  return pickers;
}


// code snippet from MDN
const all_css = [...document.styleSheets]
  .map((styleSheet) => {
    try {
      return [...styleSheet.cssRules].filter((rule) => rule.cssText.match(/\.bi-filetype-\w+/));
    } catch (e) {
      console.log(
        'Access to stylesheet %s is denied. Ignoring',
        styleSheet.href,
      );
    }
  })
  .filter((l) => l.length > 0)
  // .join("\n");


function get_file_bi_class(filename) {
    let ext = filename.split('.').pop().toLowerCase();
  for (const css of all_css[0]) {
    if (css.selectorText.match('-' + ext))
      return css.selectorText.split(':')[0].slice(1);
  }
  return 'bi-file-earmark-arrow-down-fill';
}


function get_api_token() {
  let api_token = window.localStorage.getItem('bizdoc.api_token');
  if (!api_token) {
    window.alert('API Token must be provided');
  }
  return api_token;
}


function update_access_security_status(url, elm_locked) {
  let api_token = get_api_token();
  fetch(url, {
    method: 'GET',
    headers: {"Authorization": `Token ${api_token}`}
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.statusText}`);
      }
      return response.json();
    })
    .then((json) => {
      //let elm_locked = document.getElementById('secdoc_perm');
      if (json.can_access_secret_attachment) {
        ['bi-unlock-fill', 'text-info'].forEach((e) => elm_locked.classList.add(e));
        ['bi-lock-fill', 'text-danger'].forEach((e) => elm_locked.classList.remove(e));
      } else {
        ['bi-unlock-fill', 'text-info'].forEach((e) => elm_locked.classList.remove(e));
        ['bi-lock-fill', 'text-danger'].forEach((e) => elm_locked.classList.add(e));
      }
      // console.log(json);
      return json;
    })
    .catch((error) => {
      console.log(error);
      return null;
    });
}

function truncate_string(str, max_length=20) {
  if (str.length > max_length) {
    return str.slice(0, max_length - 3) + '...';
  } else {
    return str;
  }
}


function extract_text(html) {
  const tmp = document.createElement('div');
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || '';
}

/*
security_class
평
II

특
Ⅱ
III
 평
[2급→평문]
Ⅲ
[대외비→평문]
2급→평문
3급→평문
대외→평문
[대→평문]
대
평문
 */
/*
    top_secret = ['I', 'Ⅰ']
    secret = ['II', 'Ⅱ', 'II 급', 'II급', '2급', '2 급']
    confidential = ['III', 'Ⅲ', 'III 급', 'III 급', '3급', '3 급']
    restricted = ['특', '대', '대외비']
    sensitive = ['#민감자료']
 */
function get_security_class_str(choices, sc_data) {
  // let s = sc_data.trim();
  //
  // let top_secret = ['I', 'Ⅰ']
  // let secret = ['II', 'Ⅱ', 'II 급', 'II급', '2급', '2 급']
  // let confidential = ['III', 'Ⅲ', 'III 급', 'III급', '3급', '3 급']
  // let restricted = ['특', '대', '대외비']
  // let sensitive = ['#민감자료']

  let value_map = {
    1: 'Ⅰ',
    2: 'Ⅱ',
    3: 'Ⅲ',
    4: '㊙',
    5: '㊕',
    9: ''
  }

  for (const c of choices) {
    if (sc_data === c[0])
      return value_map[c[0]];
  }
  return '';
}


function get_attachment_links(data) {
  if (!data || data.length === 0)
    return '';

  let json = JSON.parse(data);
  let html = '';
  json.forEach(item => {
    html += `<a href="${item.url}" target="_blank" data-bs-toggle="tooltip" data-bs-placement="top" title="${item.name}"><i class="bi ${get_file_bi_class(item.name)}"></i></a>`;
  });
  return html;
}