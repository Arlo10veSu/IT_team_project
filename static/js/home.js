var jsBox=document.getElementById("box");
var a=document.getElementById("a");
var b=document.getElementById("b");
var c=document.getElementById("c");
var d=document.getElementById("d");
var jsLeft=document.getElementById("left");
var jsRight=document.getElementById("right");

var num=1;

// this is the js function for changing the picture:
// the methodology of this is that we create a iterator num.
    // if click left button num--
    // if click right button num++
    // if the num = n then show the picture pn
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
