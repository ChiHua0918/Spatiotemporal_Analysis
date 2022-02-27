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
        img += `<td><img src='./static/image/GEI/${folder}/${imgName}' width="300px" id = ${i} onclick = "ShowModal(${i})" ><br/> ${imgName}</td>`;
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
    for (var i = 0; i < boardGEI.length; i++) {
        imgName = boardGEI[i];
        id = imgName.slice(3,imgName.length);
        img += `<td><img src='./static/image/GEI_contrast/${memory}/${imgName}.png' id = ${id} width="300px" onclick = "ShowModal(${id})" ><br/> ${imgName}</td>`;
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
    console.log("memory",memory);
}
// 依據等級/空間分類
function cluster_pattern(mode){
    picture = "";
    let information = document.getElementById('information');
    pattern = mode;
    information.innerHTML = mode;
}
// 分群 -- cluster:每一張 GEI 所屬的群
function clusterGEI(memory) {
    var maxCluster;
    $.ajax({
        url: 'cluster',
        type: "GET",
        // dataType: 'json',
        // contentType:'application/json',
        data: {"memory":memory,"pattern":pattern},
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
            html += `<td><img src="./static/image/GEI/${memory}/${GEIName[i]}.png" width="300px" id = ${id} onclick = "ShowModal(${id})"  title = ${GEIName[i]} ><br/>${GEIName[i]}</td>`;
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
