document.addEventListener("DOMContentLoaded", function () {
    let isEditing = false;
    let editModeBtn = document.getElementById("editModeBtn");
    let saveBtn = document.getElementById("saveBtn");
    let button = document.getElementById("btn1");

    editModeBtn.addEventListener("click", function() {
        isEditing = !isEditing;
        if (isEditing) {
            editModeBtn.textContent = "取消編輯";
            saveBtn.style.display = "inline-block";
            makeEditable(button);
        } else {
            editModeBtn.textContent = "編輯介面";
            saveBtn.style.display = "none";
            removeEditable(button);
        }
    });

    saveBtn.addEventListener("click", function() {
        saveChanges();
    });

    function makeEditable(element) {
        element.style.border = "2px dashed red";
        element.style.cursor = "grab";

        element.onmousedown = function (event) {
            event.preventDefault();
            let shiftX = event.clientX - element.offsetLeft;
            let shiftY = event.clientY - element.offsetTop;

            function moveAt(clientX, clientY) {
                element.style.left = (clientX - shiftX) + 'px';
                element.style.top = (clientY - shiftY) + 'px';
            }

            function onMouseMove(event) {
                moveAt(event.clientX, event.clientY);
            }

            document.addEventListener("mousemove", onMouseMove);

            document.onmouseup = function () {
                document.removeEventListener("mousemove", onMouseMove);
                document.onmouseup = null;
            };
        };

        element.ondragstart = function () {
            return false;
        };

        // 滾輪縮放
        element.addEventListener("wheel", function (event) {
            event.preventDefault();
            let scale = parseFloat(element.style.transform.replace(/[^0-9.]/g, "")) || 1;
            let newScale = event.deltaY < 0 ? scale * 1.1 : scale * 0.9;
            element.style.transform = `scale(${Math.max(0.5, Math.min(2, newScale))})`;
        });
    }

    function removeEditable(element) {
        element.style.border = "none";
        element.style.cursor = "default";
        element.onmousedown = null;
        element.onwheel = null;
    }

    function saveChanges() {
        let newX = parseInt(button.style.left);
        let newY = parseInt(button.style.top);
        let newWidth = parseInt(button.style.width);
        let newHeight = parseInt(button.style.height);

        fetch('/api/buttons/1/', {  // 假設是按鈕 ID 1
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                position_x: newX,
                position_y: newY,
                width: newWidth,
                height: newHeight
            })
        }).then(response => response.json())
        .then(data => {
            alert("儲存成功！");
        }).catch(error => {
            console.error("儲存錯誤", error);
        });
    }
});