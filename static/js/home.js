var jsBox=document.getElementById("box");
var a=document.getElementById("a");
var b=document.getElementById("b");
var c=document.getElementById("c");
var d=document.getElementById("d");
var jsLeft=document.getElementById("left");
var jsRight=document.getElementById("right");

var num=1;
//var timer=setInterval(startLoop,1000);

//function startLoop() {
//    currentPage++;
//    change()
//}

jsLeft.onclick = function() {
    num --;
    if (num < 1) {
        num = 4;
    }
    analysis();
}

jsRight.onclick = function(){
    num ++;
    if (num > 4){
        num = 1;
    }
    analysis();
}

function analysis(){
      if(num==1){
          a.style.display="block";
          b.style.display="none";
          c.style.display="none";
          d.style.display="none";
      }
      if(num==2){
          a.style.display="none";
          b.style.display="block";
          c.style.display="none";
          d.style.display="none";
      }
      if(num==3){
          a.style.display="none";
          b.style.display="none";
          c.style.display="block";
          d.style.display="none";
      }
      if(num==4){
          a.style.display="none";
          b.style.display="none";
          c.style.display="none";
          d.style.display="block";
      }
}
