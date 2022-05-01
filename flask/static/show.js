// 顯示GEI
var showPicture = document.getElementById("frame");
// 位置設定
var modal = document.getElementById('modal');
var modalBtn = document.getElementById('modalBtn');
var speed = document.getElementById('speed');
var speedBtn = document.getElementById('speedBtn');
setPos();

// 紀錄目前選取的照片
var picture = "";
// GEI也多少照片
var GEINum;
//所有原始圖片的檔名(.png)
var imgData = [];
//每一張GEI所屬的分類
var cluster;
//每一張GEI資料(NO.1,分群,10筆)
var GEIName;
// 判斷目前為等級分群/空間分群
var pattern = "";
// 紀錄現在畫面上的GEI
var boardGEI = [];
// bow filter 為 橫豎斜哪一個
filterType = ""
getGEINum()
function getGEINum() {
    $.ajax({
        url: "GEINum", 
        type: "GET",
        data:null,
        /*result為后端函式回傳的json*/
        success: function (result) {
            GEINum = result.num;
        }
    });
}

// 顯示GEI
function GEI(folder) {
    let img = "<tr>";
    for (var i = 0; i < GEINum; i++) {
        imgName = "NO." + i + ".png";
        img += `<td><img src='./static/image/GEI/${folder}/${imgName}' width="${(window.innerWidth-200)/5}px" id = ${i} onclick = "ShowModal(${i})" ><br/> ${imgName}</td>`;
        // 換行
        if (i % 5 == 4) {
            img += "</tr><tr>";
        }
        boardGEI.push(imgName);
    }
    showPicture.innerHTML = img;
    memory = folder;
}

//存取上一個版面
var tmp;
// 返回鑑
function back() {
    showPicture.innerHTML = tmp;
    picture = "";
}
// 紀錄我現在按的按鈕
var memory = "";

// 加強對比: 單張 GEI 的黑白對比加強
function contrast(){
    picture = "";
    let img = "<tr>";
    console.log("contrast boardGEI",boardGEI);
    console.log("now folder is",memory);
    for (var i = 0; i < boardGEI.length; i++) {
        imgName = boardGEI[i];
        id = imgName.slice(3,imgName.length);
        img += `<td><img src='./static/image/GEI_contrast/${memory}/${imgName}' id = ${id} width="${(window.innerWidth-200)/5}px" onclick = "ShowModal(${id})" ><br/> ${imgName}</td>`;
        // 換行
        if (i % 5 == 4) {
            img += "</tr><tr>";
        }
    }
    showPicture.innerHTML = img;
}
// 按下分群
function clickCluster() {
    clusterGEI(memory);
    console.log("memory",memory,"\t","filter type:",filterType);
}
// 紀錄目前的模式是 等級 or 空間
function cluster_pattern(mode){
    picture = "";
    pattern = mode;
}
// filter type
function filterMode(type){
    filterType = type;
}
// 分群 -- cluster:每一張 GEI 所屬的群
function clusterGEI(memory) {
    var maxCluster;
    // user 沒有選擇 pattern
    if (pattern.length == 0){
        alert("請先選擇模式");
        return;
    }
    $.ajax({
        url: 'cluster',
        type: "GET",
        // dataType: 'json',
        // contentType:'application/json',
        data: {"memory":memory,"pattern":pattern,"filterType":filterType},
        async: false, // 同步 -> 等到拿到後端回傳的資料再做 clusterUI
        /*result為后端函式回傳的json*/
        success: function (result) {
            clusterObject = result.cluster;  // GEI 依序所屬分群
            cluster = Object.values(clusterObject);
            GEIName = result.GEIName;        // 目前資料夾中所有 GEI 名字(NO.0.png...)
            maxCluster = result.maxCluster;  // 總共分多少群
            console.log(`分 ${maxCluster} 群`);
        }
    });
    clusterUI(maxCluster);
}
// 顯示分群的圖示
function clusterUI(maxCluster) {
    console.log("clusterUI");
    var html = "";
    for (let i = 0; i <= maxCluster; i++) {
        html += `<img src="./static/image/clusterUI/${i}.png" width="300px" onclick = "everyGEI(${i})">`;
    }
    tmp = html;
    showPicture.innerHTML = html;
}
// 每一群的GEI
function everyGEI(k) {
    console.log("everyGEI");
    picture = "";
    let html = "<tr/>";
    let n = 0;//該行有幾張
    boardGEI = [];
    console.log(cluster);
    for (let i = 0; i < cluster.length; i++) {
        if (cluster[i] == k) {
            // GEI id 數字
            let id = GEIName[i].slice(3, GEIName[i].length);
            console.log("cluterID:",id)
            html += `<td><img src="./static/image/GEI/${memory}/${GEIName[i]}.png" width="${(window.innerWidth-200)/5}px" id = ${id} onclick = "ShowModal(${id})"  title = ${GEIName[i]} ><br/>${GEIName[i]}</td>`;
            // 換行
            if (n % 5 == 4) {
                html += "</tr><tr>";
            }
            n += 1;
            boardGEI.push(GEIName[i]);
            console.log("everyGEI GEIName",GEIName[i]);
        }
    }
    showPicture.innerHTML = html;
}

// 點擊顯示gif(原始連續 PM2.5 彩色空汙圖)
function ShowModal(id) {
    show();
    // 讓上一個的邊框消失
    if (picture != "") {
        var chooseImg = document.getElementById(picture);
        chooseImg.style.border = "2px solid";
        chooseImg.style.borderColor = "white";
        console.log("pre:", picture);
    }
    // 把選起來的GEI框起來
    var chooseImg = document.getElementById(id);
    chooseImg.style.border = "6px solid";
    chooseImg.style.borderColor = "greenyellow";
    picture = id;
    console.log("after:",picture);
    console.log("id:",id);
}
function gif(){
    // 傳送資料給gif.py
    $.ajax({
        url: "gif", /*資料提交到submit處*/
        type: "GET",  /*用GET方法提交*/
        data: {"id":picture,"speed":$("#speed").val()},  /*提交的資料（json格式），從輸入框中獲取*///, "frames": $("#frames").val()
        /*result為后端函式回傳的json*/
        success: function (result) {
            console.log(result);
            modal.innerHTML = `<td><img src="${result.gif}" width="500px"></td>`;
        }
    });
}


// 顯示視窗
function show() {
    modal.style.display = 'block';
    modalBtn.style.display = 'block';
    speed.style.display = 'block';
    speedBtn.style.display = 'block';
}
// 視窗隱藏
function hide() {
    modal.style.display = 'none';
    modalBtn.style.display = 'none';
    speed.style.display = 'none';
    speedBtn.style.display = 'none';
}

// 設定modal位置
function setPos() {
    let height = document.documentElement.clientHeight / 2;
    let width = document.documentElement.clientWidth / 2;
    modal.style.marginTop = (height - 350) + "px";
    modal.style.marginLeft = (width - 700) + "px";
}
// button change color
function changeColor(buttonType,order){
    // 屬於此 className 的 button 總共有多少個
    let howManyButton = document.getElementsByClassName(buttonType).length;
    // 屬於此 className 的 button 恢復原狀
    for (var i = 0; i < howManyButton; i++){
        document.getElementsByClassName(buttonType)[i].style.backgroundColor = "#F3E9DD";
    }
    // 剛剛按下的按鈕加深背景顏色
    document.getElementsByClassName(buttonType)[order].style.backgroundColor = "#CEAB93";
    // 加強對比(contrast) 比較特殊，如果按了其他資料或是分群，目前的畫面就不是加強對比的 GEI 圖了
    if (buttonType == "clustering" || buttonType == "dataButton"){
        document.getElementsByClassName("contrast")[0].style.backgroundColor = "#F3E9DD";
    }
    // 如果還沒選 pattern 的話，分群的按鈕不可以變深
}
