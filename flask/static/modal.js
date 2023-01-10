// setPos();
// gif modal 位置設定
var gifModal = document.getElementById('gif');
var modal = document.getElementById('modal');
// 點擊顯示gif(原始連續 PM2.5 彩色空汙圖)
function ShowModal(id) {
    show();
    // 設置 gif
    let gifPath = `../static/image/gif/KMeansCut/${id}.gif`;
    let widthSize = `${(window.innerWidth/4)}px`;
    modal.setAttribute("src",gifPath);
    modal.setAttribute("width",widthSize)

    // 目前挑選的 GEI 編號以及 GEI 的型態
    let number = "NO."+id;
    $("#gifName").text(number);
    $("#selectName").val(number);
    $("#GEIfolder").val(memory);

    // modal.innerHTML = `<img src="./static/image/gif/KMeansCut/${id}.gif" width="${(window.innerWidth/4)}px">`;
    // 讓上一個的邊框消失
    if (picture.length != 0) {
        var chooseImg = document.getElementById(picture);
        chooseImg.style.border = "2px solid";
        chooseImg.style.borderColor = "white";
        console.log("Previous choose:", picture);
    }
    // 把選起來的 GEI 框起來(color=綠色)
    var chooseImg = document.getElementById(id);
    chooseImg.style.border = "6px solid";
    chooseImg.style.borderColor = "greenyellow";
    picture = id;
    console.log("after choose:",id);
}
function gif(){
    let speed = $("#speed").val();
    if (speed == ""){
        alert("請輸入動圖速度");
        return;
    }
    // 傳送資料給gif.py
    $.ajax({
        url: "gif", /*資料提交到submit處*/
        type: "GET",  /*用GET方法提交*/
        data: {"id":picture,"speed":speed},  /*提交的資料（json格式），從輸入框中獲取*///, "frames": $("#frames").val()
        /*result為后端函式回傳的json*/
        success: function (result) {
            console.log(result);
            modal.innerHTML = `<img src="${result.gif}" width="${(window.innerWidth)/4}px">`;
        }
    });
}
// 顯示 gif 視窗
function show() {
    gifModal.style.display = 'block'
}
// 隱藏 gif 視窗
function hide() {
    gifModal.style.display = 'none';
}

// // 設定modal位置
// function setPos() {
//     // let height = document.documentElement.scrollHeight;
//     // let width = document.documentElement.scrollWidth;
//     let height = document.body.clientHeight;
//     let width = document.body.clientWidth;
//     // modal.style.marginTop = ($('#functionButton')[0].offsetHeight)/2 + "px";
//     // modal.style.marginLeft = ($('#functionButton')[0].offsetWidth)/2 + "px";
//     // console.log(document.getElementsByClassName('text')[0].offsetHeight );
// }