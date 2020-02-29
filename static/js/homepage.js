var jsBox=document.getElementById("box");
    var jsPic=document.getElementById("pic");
    var jsLeft=document.getElementById("left");
    var jsright=document.getElementById("right");

    var currentPage=1;
    var timer=setInterval(startLoop,1000);

    function startLoop() {
        currentPage++;
        change()
    }

    function change() {
        if (currentPage === 6) {
            currentPage = 1
        } else if (currentPage === 0) {
            currentPage = 5;
        }
        jsPic.src = "img/" + currentPage + ".jpg";

        jsBox.addEventListener("mouseover", overFunc, false);

        function overFunc() {
            clearInterval(timer);
            jsLeft.style.display = "block";
            jsright.style.display = "block";
        }

        jsBox.addEventListener("mouseout", outFunc, false);

        function outFunc() {
            timer = setInterval(startLoop, 2000);
            jsLeft.style.display = "none";
            jsright.style.display = "none";

        }
    }

    jsLeft.addEventListener("mouseover",deep,false);
    jsright.addEventListener("mouseover",deep,false);
    function deep() {
        this.style.backgroundColor="rgba(0,0,0,0.6)"
    }
    jsLeft.addEventListener("mouseout",nodeep,false);
    jsright.addEventListener("mouseout",nodeep,false);
    function nodeep() {
        this.style.backgroundColor="rgba(0,0,0,0.2)"
    }
    jsright.addEventListener("click",function () {
        currentPage++;
        change()
    },false);

    jsLeft.addEventListener("click",function () {
        currentPage--;
        change()
    },false);