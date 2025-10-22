/*
rest_client.js
version: 1.2  @2023/05/03
Wenchin Hsieh @Goomo.Net Studio, wenchin@goomo.net
*/


// 定義 RESTful API 的 URL
const url_host = 'http://localhost:5000/';
const url_read_all = url_host + "fruit/read_all";
const url_read = url_host + "fruit/read/";
const url_create = url_host + "fruit/create";
const url_delete = url_host + "fruit/delete/";
const url_replace = url_host + "fruit/replace/";


// 取得 READ_ALL 按鈕的 DOM 物件。當按下時，執行 GET Request
const getAllButton = document.getElementById('read-all-button');
getAllButton.addEventListener('click', () => {
    fetch(url_read_all)
        .then(response => response.json())
        .then(data => console.log('read_collection():', data));
});


// 取得 READ 按鈕的 DOM 物件。當按下時，執行 GET Request
const getButton = document.getElementById('read-button');
getButton.addEventListener('click', () => {
    let find_key = 'banana'
    fetch(url_read + find_key)
        .then(response => response.json())
        .then(data => console.log('read_docu_path():', data));
});


// 取得 DELETE 按鈕的 DOM 物件。當按下時，執行 DELETE Request
const deleteButton = document.getElementById('delete-button');
deleteButton.addEventListener('click', () => {
    let find_key = 'banana'
    fetch(url_delete + find_key, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => console.log('DELETE:', data));
});


// 取得 POST 按鈕的 DOM 物件。當按下時，執行 POST Request
const postButton = document.getElementById('post-button');
postButton.addEventListener('click', () => {
    let json_data = { 'name': 'kiwi', 'amount': 9 }
    fetch(url_create, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(json_data)
    })
        .then(response => response.json())
        .then(data => console.log('create_docu():', data));
});



// 取得 PUT 按鈕的 DOM 物件。當按下時，執行 PUT Request
const putButton = document.getElementById('put-button');
putButton.addEventListener('click', () => {
    let find_key = 'kiwi'
    let json_data = { 'name': 'mongo', 'amount': 12 }
    fetch(url_replace + find_key, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(json_data)
    })
        .then(response => response.json())
        .then(data => console.log('replace_docu_path():', data));
});