/*! 
 * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin) 
 * Copyright 2013-2023 Start Bootstrap 
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE) 
 */

// 初始可疑人物資料
const alerts = [
    { id: 1, name: "紅色帽子男子", times: 5, location: "台北市信義區", details: "跟蹤女性" }, 
    { id: 2, name: "藍色外套男子", times: 6, location: "新北市三重區", details: "隨機拍攝行人" }, 
    { id: 3, name: "灰色連帽男子", times: 7, location: "桃園市中壢區", details: "偷拍女性" }, 
    { id: 4, name: "黑色夾克男子", times: 6, location: "新北市新莊區", details: "跟蹤女性" }, 
    { id: 5, name: "白色口罩男子", times: 8, location: "台中市西屯區", details: "持續徘徊於學校門口" }, 
    { id: 6, name: "綠色運動衫男子", times: 4, location: "高雄市左營區", details: "尾隨路人" }, 
    { id: 7, name: "棕色風衣男子", times: 9, location: "台南市東區", details: "試圖與陌生人強行搭話" }, 
    { id: 8, name: "黑色連帽外套男子", times: 5, location: "新竹市北區", details: "夜間跟蹤女性" }, 
    { id: 9, name: "藍色棒球帽男子", times: 7, location: "嘉義市東區", details: "多次出現在住宅區" }, 
    { id: 10, name: "深灰色西裝男子", times: 6, location: "基隆市仁愛區", details: "持續注視並靠近女性" }
];

// 確保 DOM 內容加載完畢後執行
document.addEventListener("DOMContentLoaded", function() {
    const alertContainer = document.querySelector(".alert-wrapper");

    // 遍歷可疑人物數據並顯示
    alerts.forEach(alert => {
        if (alert.times >= 4) { // 若該人物出現次數 >= 4
            const card = document.createElement("div");
            card.className = "alert-card";
            card.innerHTML = `
                <h3><a href="anonymous-chat.html?person=${encodeURIComponent(alert.name)}" target="_blank">${alert.name}</a></h3>
                <p><strong>地點：</strong>${alert.location}</p>
                <p><strong>行為：</strong>${alert.details}</p>
                <p><strong>出現次數：</strong>${alert.times} 次</p>
            `;
            alertContainer.appendChild(card);
        }
    });
});
