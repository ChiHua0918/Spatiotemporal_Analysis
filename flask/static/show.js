// 顯示GEI
let showPicture = document.getElementById("frame");
// 位置設定
let modal = document.getElementById('modal');
let modalBtn = document.getElementById('modalBtn');
let speed = document.getElementById('speed');
let speedBtn = document.getElementById('speedBtn');
setPos();

// 紀錄目前選取的照片
let picture = "";
// GEI也多少照片
let GEINum;
//所有原始圖片的檔名(.png)
let imgData = [];
//每一張GEI所屬的分類
let cluster;
//每一張GEI資料(NO.1,分群,10筆)
let GEIName;
// 判斷目前為等級分群/空間分群
let classify_pattern = "";
// 紀錄現在畫面上的GEI
let boardGEI = [];
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
    for (var i = 1; i <= GEINum; i++) {
        imgName = "NO." + i;
        img += `<td><img src='./static/image/GEI~3/${folder}/${imgName}.png' width="280px" id = ${i} onclick = "ShowModal(${i})" ><br/> ${imgName}</td>`;
        // 換行
        if (i % 5 == 0) {
            img += "</tr><tr>";
        }
        boardGEI.push(imgName);
    }
    showPicture.innerHTML = img;
    memory = folder;
}

//存取上一個版面
let tmp;
// 返回鑑
function back() {
    showPicture.innerHTML = tmp;
    picture = "";
}
// 紀錄我現在按的按鈕
let memory = "";

// 加強對比: 單張 GEI 的黑白對比加強
function contrast(){
    picture = "";
    let img = "<tr>";
    for (var i = 0; i < boardGEI.length; i++) {
        imgName = boardGEI[i];
        id = imgName.slice(3,imgName.length);
        img += `<td><img src='./static/image/GEI~3Contrast/${memory}/${imgName}.png' id = ${id} width="280px" onclick = "ShowModal(${id})" ><br/> ${imgName}</td>`;
        // 換行
        if (i % 5 == 4 && i != 0) {
            img += "</tr><tr>";
        }
    }
    showPicture.innerHTML = img;
}
// 按下分群
function clickClassify() {
    classify(memory);
}
// 依據等級/空間分類
function cluster_pattern(pattern){
    picture = "";
    let information = document.getElementById('information');
    classify_pattern = pattern;
    information.innerHTML = pattern;
}
// 分類 -- cluster:每一張 GEI 所屬的群
function classify(memory) {
    $.ajax({
        url: 'cluster',
        type: "GET",
        // dataType: 'json',
        // contentType:'application/json',
        data: {"memory":memory,"pattern":classify_pattern},
        /*result為后端函式回傳的json*/
        success: function (result) {
            clusterObject = result.cluster;
            cluster = Object.values(clusterObject);
            GEIName = result.GEIName;
        }
    });
    clusterUI(cluster);
}
// 顯示分群的圖示
function clusterUI(cluster) {
    let html = "";
    for (let i = 0; i <= Math.max(...cluster); i++) {
        html += `<img src="./static/image/Number_icon/${i + 1}.png" width="200px" onclick = "everyGEI(${i})">`;
    }
    tmp = html;
    showPicture.innerHTML = html;
}
// 每一群的GEI
function everyGEI(k) {
    picture = "";
    let html = "<tr/>";
    let n = 0;//該行有幾張
    boardGEI = [];
    for (let i = 0; i < cluster.length; i++) {
        if (cluster[i] == k) {
            n += 1;
            // id數字
            let id = GEIName[i].slice(3, GEIName[i].length);
            console.log("cluterID:",id)
            html += `<td><img src="./static/image/GEI~3/${memory}/${GEIName[i]}.png" width="300px" id = ${id} onclick = "ShowModal(${id})"  title = ${GEIName[i]} ><br/>${GEIName[i]}</td>`;
            // 換行
            if (n % 5 == 0) {
                html += "</tr><tr>";
            }
            boardGEI.push(GEIName[i]);
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
