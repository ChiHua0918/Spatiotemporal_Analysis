// BBG 一開始 load GEI_origin 圖片
$( document ).ready(function() {
    getGEINum().then(setTimeout(GEI(),0)).then(clickCluster());
});
function GEI() {
    folder = document.getElementById('data').value;
    subtitle.innerHTML = folder;
    memory = folder;
    showPicture.innerHTML = "";
    changeColor("dataButton","none")
}