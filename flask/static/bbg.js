// BBG 一開始 load GEI_origin 圖片
$( document ).ready(function() {
    getGEINum().then(setTimeout(GEI(),0));
});
// 顯示GEI
function GEI() {
    folder = document.getElementById('data').value;
    console.log(folder);
    subtitle.innerHTML = folder;
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
    console.log(boardGEI);
    console.log(GEINum);
    showPicture.innerHTML = img;
    memory = folder;
    changeColor("dataButton","none");
}