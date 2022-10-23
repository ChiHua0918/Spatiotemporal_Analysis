// 顯示GEI
var showPicture = document.getElementById("frame");
// gif modal 位置設定
var gifModal = document.getElementById('gif');
var modal = document.getElementById('modal');
setPos();
// 副標題
var subtitle = document.getElementById('subtitle');
// 紀錄目前選取的照片
var picture = "";
// GEI也多少照片
var GEINum;
//所有原始圖片的檔名(.png)
// var imgData = [];
//每一張GEI所屬的分類
var cluster;
//每一張GEI資料(NO.1,分群,10筆)
var GEIName;
// 紀錄現在畫面上的GEI
var boardGEI = [];
//存取上一個版面
var tmp;
// 紀錄現在選取的數據 (GEI_origin、GEI_Level)
var memory = "";
async function getGEINum() {
    $.ajax({
        url: "GEINum", 
        type: "GET",
        data:null,
        async:false,
        /*result為后端函式回傳的json*/
        success: function (result) {
            GEINum = result.num;
        }
    });
}
// 顯示GEI
// function GEI() {
//     folder = document.getElementById('data').value;
//     console.log(folder);
//     subtitle.innerHTML = folder;
//     let img = "<tr>";
//     for (var i = 0; i < GEINum; i++) {
//         imgName = "NO." + i + ".png";
//         img += `<td><img src='./static/image/GEI/${folder}/${imgName}' width="${(window.innerWidth-200)/5}px" id = ${i} onclick = "ShowModal(${i})" ><br/> ${imgName}</td>`;
//         // 換行
//         if (i % 5 == 4) {
//             img += "</tr><tr>";
//         }
//         boardGEI.push(imgName);
//     }
//     console.log(boardGEI);
//     console.log(GEINum);
//     showPicture.innerHTML = img;
//     memory = folder;
// }

// 返回鑑
function back() {
    subtitle.innerHTML = "分群結果 - "+ document.getElementById('clusterFile').name;
    showPicture.innerHTML = tmp;
    picture = "";
    changeColor('back','0');
}
// 加強對比: 單張 GEI 的黑白對比加強
function contrast(){
    picture = "";
    let img = "<tr>";
    console.log("contrast boardGEI",boardGEI);
    console.log("now folder is",memory);
    for (var i = 0; i < boardGEI.length; i++) {
        let id = boardGEI[i].split('.')[1];
        let imgName = boardGEI[i];
        img += `<td><img src='./static/image/GEI_contrast/${memory}/${imgName}' id = ${id} width="${(window.innerWidth-200)/5}px" onclick = "ShowModal(${id})" ><br/> ${imgName}</td>`;
        // 換行
        if (i % 5 == 4) {
            img += "</tr><tr>";
        }
    }
    console.log(boardGEI);
    showPicture.innerHTML = img;
}
// 按下分群
function clickCluster() {
    subtitle.innerHTML = "分群結果 - "+document.getElementById('clusterFile').name;
    // 要顯示哪一個檔案的 GEI 分群
    let clusterFile = document.getElementById('clusterFile').value;
    // filter 大小
    let filterSize = document.getElementById('filterSize').value;
    // 沒有選取檔案
    if (clusterFile.length == 0){
        alert("請先選取檔案");
        return
    }
    // BOW 要選擇 filter 的大小
    if (clusterFile.split('_')[0] == "bow" && filterSize == ""){
        alert('bow 須選擇 filter 大小');
        return;
    }
    // CNN 目前只有 3*3
    else if (filterSize == "2"){
        alert("目前 CNN 只有 filter 3*3");
        // 更改 filter 大小
        document.getElementById('filterSize').getElementsByTagName('option')[2].selected = 'selected';
        filterSize = 3;
    }
    picture = "";
    alert("圖片製作中，請稍等");
    // 紀錄目前的模式是 等級 or 空間
    clusterGEI(memory,clusterFile,filterSize);
    changeColor('clustering','0');
}
// 分群 -- cluster:每一張 GEI 所屬的群
function clusterGEI(memory,clusterFile,filterSize) {
    var maxCluster;
    // user 沒有選擇檔案
    if (clusterFile.length == 0){
        alert("請先選擇模式");
        return;
    }
    $.ajax({
        url: 'cluster',
        type: "GET",
        data: {"memory":memory,"clusterFile":clusterFile,"filterSize":filterSize},
        async: true,
        /*result為后端函式回傳的json*/
        success: function (result) {
            clusterObject = result.cluster;  // GEI 依序所屬分群
            cluster = Object.values(clusterObject);
            GEIName = result.GEIName;        // 目前資料夾中所有 GEI 名字(NO.0.png...)
            maxCluster = result.maxCluster;  // 總共分多少群
            console.log(`分 ${maxCluster} 群`);
            clusterUI(maxCluster);
        }
    });
}
// 顯示分群的圖示
function clusterUI(maxCluster) {
    console.log("clusterUI");
    var html = "<tr>";
    for (let i = 0; i <= maxCluster; i++) {
        // directory = "dynamicPic"
        // path = `clusterUI/${i}.png`
        // $.ajax({
        //     url:  "dynamicImage",
        //     type: "GET",
        //     data: {"directory":directory,"path":path},
        //     success: function(result){
        //     }
        // })
        html += `<td><img src="./static/image/clusterUI/${i}.png" width="${(window.innerWidth-200)/5}px" onclick = "everyGEI(${i})"></br>第 ${i} 群</td>`;
        // html += `<td><img src="./${directory}/${path}" width="${(window.innerWidth-200)/5}px" onclick = "everyGEI(${i})"></br>第 ${i} 群</td>`;
        // 換行
        if (i % 5 == 4){
            html += "</tr><tr>";
        }
    }
    html += "</tr>";
    tmp = html;
    showPicture.innerHTML = html;
}
// 每一群的GEI
function everyGEI(k) {
    console.log("everyGEI");
    picture = "";
    let html = "<tr/>";
    let n = 0;   // 屬於這群有多少張 GEI
    boardGEI = [];
    console.log(cluster);
    for (let i = 0; i < cluster.length; i++) {
        if (cluster[i] == k) {
            // GEI id 數字
            let id = GEIName[i].slice(3, GEIName[i].length);
            let imgName = GEIName[i]+".png";
            console.log("cluterID:",id)
            html += `<td><img src="./static/image/GEI/${memory}/${imgName}" width="${(window.innerWidth-200)/5}px" id = ${id} onclick = "ShowModal(${id})"  title = ${GEIName[i]} ><br/>${GEIName[i]}</td>`;
            // 換行
            if (n % 5 == 4) {
                html += "</tr><tr>";
            }
            n += 1;
            boardGEI.push(imgName);
        }
    }
    showPicture.innerHTML = html;
    subtitle.innerHTML = `分群結果 - 第 ${k} 群<br/> 總共有 ${n} 張 GEI`;
}

// 點擊顯示gif(原始連續 PM2.5 彩色空汙圖)
function ShowModal(id) {
    show();
    modal.innerHTML = `<img src="./static/image/gif/KMeansCut/${id}.gif" width="${(window.innerWidth/4)}px"><br/>${id}.gif`;
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

// 設定modal位置
function setPos() {
    let height = document.documentElement.scrollHeight;
    let width = document.documentElement.scrollWidth;
    modal.style.marginTop = (height - 1000)/2 + "px";
    modal.style.marginLeft = (width - 700)/2 + "px";
}
// button change color
function changeColor(buttonType,order){
    // 屬於此 className 的 button 總共有多少個
    let howManyButton = document.getElementsByClassName(buttonType).length;
    // 屬於此 className 的 button 恢復原狀
    for (var i = 0; i < howManyButton; i++){
        document.getElementsByClassName(buttonType)[i].style.backgroundColor = "#F3E9DD";
    }
    console.log("button type",buttonType);
    // 剛剛按下的按鈕加深背景顏色
    try {
        document.getElementsByClassName(buttonType)[order].style.backgroundColor = "#CEAB93";
    } catch (error) {
        console.log("buttonType",buttonType);
    }
    // 加強對比(contrast)，如果按了其他資料或是分群，目前的畫面就不是加強對比的 GEI 圖了
    if (buttonType != "contrast"){
        document.getElementsByClassName("contrast")[0].style.backgroundColor = "#F3E9DD";
    }
    // 分群按鈕
    if (buttonType == "dataButton"){
        document.getElementsByClassName("clustering")[0].style.backgroundColor = "#F3E9DD";
    }
}
