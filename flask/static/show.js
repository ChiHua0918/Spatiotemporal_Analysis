// 顯示GEI
var showPicture = document.getElementById("frame");

// 副標題
var subtitle = document.getElementById('subtitle');

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
// 選取哪一年份 （2018）
var dataYear;
// 紀錄現在選取的數據 (GEI_origin、GEI_Level)
var sourceDataset = document.getElementById("data").value;
// 目前切 cut 的方法
var cutType;
async function getGEINum() {
    console.log("cutType",cutType,"dataYear",dataYear);
    $.ajax({
        url: "GEINum", 
        type: "GET",
        data:{"cutType":cutType,"dataYear":dataYear},
        async:false,
        /*result為后端函式回傳的json*/
        success: function (result) {
            GEINum = result.num;
        }
    });
}
// 顯示GEI
function GEI() {
    folder = document.getElementById('data').value;
    subtitle.innerHTML = folder;
    sourceDataset = folder;
    showPicture.innerHTML = "";
    changeColor("dataButton","none")
}

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
    console.log("now folder is",sourceDataset);
    for (var i = 0; i < boardGEI.length; i++) {
        let id = boardGEI[i].split('.')[1];
        let imgName = boardGEI[i];
        img += `<td><img src='./static/image/GEI_contrast/${dataYear}/${cutType}/${sourceDataset}/${imgName}' id = ${id} width="${(window.innerWidth-200)/5}px" onclick = "ShowModal(${id})" ><br/> ${imgName}</td>`;
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
    // 年份
    let dataYear = document.getElementById('dataYearSelect').value;
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
    else if (clusterFile.split('_')[0] == "cnn" && filterSize == "2"){
        alert("目前 CNN 只有 filter 3*3");
        // 更改 filter 大小
        document.getElementById('filterSize').getElementsByTagName('option')[2].selected = 'selected';
        filterSize = 3;
        // filter size 改為 3*3
        $("#filterSize option[value='3']").attr("selected", true); 
    }
    picture = "";
    alert("圖片製作中，請稍等");
    // 紀錄目前的模式是 等級 or 空間
    clusterGEI(sourceDataset,dataYear,clusterFile,filterSize);
    changeColor('clustering','0');
}
// 分群 -- cluster:每一張 GEI 所屬的群
function clusterGEI(sourceDataset,dataYear,clusterFile,filterSize) {
    var maxCluster;
    // user 沒有選擇檔案
    if (clusterFile.length == 0){
        alert("請先選擇方法");
        return;
    }
    $.ajax({
        url: 'cluster',
        type: "GET",
        data: {"cutType":cutType,"sourceDataset":sourceDataset,"dataYear":dataYear,"clusterFile":clusterFile,"filterSize":filterSize},
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
            html += `<td><img src="./static/image/GEI/${dataYear}/${cutType}/${sourceDataset}/${imgName}" width="${(window.innerWidth-200)/5}px" id = ${id} onclick = "ShowModal(${id})"  title = ${GEIName[i]} ><br/>${GEIName[i]}</td>`;
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
    // 取消分群按鈕
    if (buttonType == "dataButton"){
        document.getElementsByClassName("clustering")[0].style.backgroundColor = "#F3E9DD";
        showPicture.innerHTML = "";
    }
}
$("#cutTypeSelect" ).change(function() {
    cutType = document.getElementById("cutTypeSelect").value;
});
$("#dataYearSelect" ).change(function() {
    dataYear = document.getElementById("dataYearSelect").value;
});
$( document ).ready(function() {
    cutType = document.getElementById("cutTypeSelect").value;
    dataYear = document.getElementById("dataYearSelect").value;
});
