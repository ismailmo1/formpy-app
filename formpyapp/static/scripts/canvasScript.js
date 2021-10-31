// create canvas with id of canvas element
// add options via object
const addCircleBtn = document.getElementById("addCircle");
const exportBtn = document.getElementById("export");
const canvas = new fabric.Canvas("canvas");
const zoomIn = document.getElementById("zoomIn")
const zoomOut = document.getElementById("zoomOut")
const panMode = document.getElementById("panMode")
const circleList = document.getElementById("circleList")
const intNavBtn = document.getElementById("interactiveNavButton");
const canvasContainer = document.querySelector("#canvasDiv")

// hold spots data
let questions = {}

async function addImageToCanvas(){
    let templateImg = document.getElementById("templateImg")
    
      const bgImage = new fabric.Image.fromURL(templateImg.src, (img)=>{
  
        // get image aspect ratio to decide if scale to height or width
        imgAR = img.width/img.height
        if(imgAR>= 1){
            // scale image width to canvas
            scaleFactor = canvas.width/img.width

        }else{
            // // scale image height to canvas
            scaleFactor = canvas.height/img.height
        }
        img.set({scaleY:scaleFactor,scaleX: scaleFactor})
    
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas))
  
  
      })
        
  
  }
function resizeCanvasImage(img){

}
// fire event on bootstrap nav activation (div doesnt have any width until shown!) 
intNavBtn.addEventListener("shown.bs.tab", ()=>{
    let w = canvasContainer.offsetWidth 
    if(w!=canvas.width){
        resizeCanvas();
        addImageToCanvas();
    }
})
// exportBtn.addEventListener('click', resizeCanvas, false);

function resizeCanvas() {
    // A4 paper height/width ratio ~ 0.7
    canvas.setHeight(canvasContainer.offsetWidth*0.7);
    canvas.setWidth(canvasContainer.offsetWidth);
    canvas.renderAll();
}



panMode.addEventListener("click", (e)=>{
    if (!panMode.status){
        e.target.classList.toggle("panModeOn")
        panMode.status = true;
        canvas.isSelection=false
    }else{
        e.target.classList.toggle("panModeOn")

        panMode.status = false;
        canvas.isSelection=true
    }}
)

canvas.on('mouse:down', function(opt) {
    let evt = opt.e;
    if (panMode.status) {
      this.isDragging = true;
      this.selection = false;
      this.lastPosX = evt.clientX;
      this.lastPosY = evt.clientY;
    }
  });
  canvas.on('mouse:move', function(opt) {
    if (this.isDragging) {
        // console.log(opt)
        // console.log(opt.e)

        let e = opt.e;
        let vpt = this.viewportTransform;
        // move viewport by amount moved since last move      
        vpt[4] += e.clientX - this.lastPosX;
        vpt[5] += e.clientY - this.lastPosY;
        this.requestRenderAll();
        this.lastPosX = e.clientX;
        this.lastPosY = e.clientY;
    }
  });
  canvas.on('mouse:up', function(opt) {
    // on mouse up we want to recalculate new interaction
    // for all objects, so we call setViewportTransform
    this.setViewportTransform(this.viewportTransform);
    this.isDragging = false;
    this.selection = true;
  });
      


// add zoom in/out func
zoomOut.addEventListener("click", ()=>{
    canvas.setZoom(canvas.getZoom() *0.9)
})

zoomIn.addEventListener("click", ()=>{
    canvas.setZoom(canvas.getZoom() *1.1)
})


exportBtn.addEventListener("click", ()=>{
    circleList.innerHTML = ""
    let table = document.createElement("table")
    let hdRow = document.createElement("tr")
    let idxHdr = document.createElement("th")
    let xHdr = document.createElement("th")
    let yHdr = document.createElement("th")
    idxHdr.innerText = "Answer No."
    xHdr.innerText = "x coord"
    yHdr.innerText =  "y coord"
    hdRow.appendChild(idxHdr)
    hdRow.appendChild(xHdr)
    hdRow.appendChild(yHdr)
    table.appendChild(hdRow)
    circleList.appendChild(table)

    canvas.toObject().objects.forEach((obj, i) => {        
        let row = document.createElement("tr")
        let ansCol = document.createElement("td")
        let ansX = document.createElement("td")
        let ansY = document.createElement("td")
        ansCol.innerText = i
        ansX.innerText = Math.round(obj.left/scaleFactor)
        ansY.innerText = Math.round(obj.top/scaleFactor)
        row.appendChild(ansCol)
        row.appendChild(ansX)
        row.appendChild(ansY)
        table.appendChild(row)

    });
})
addCircleBtn.addEventListener("click", addCircle)

// get object location when moved
canvas.on("object:moved", (e)=>{
    let {type,top, left} = e.target  
console.log(type,top/scaleFactor, left/scaleFactor)
})


function addCircle(){
    const circle = new fabric.Circle({
        radius: 25,
        top: 200,
        left: 200,
        strokeWidth:5,
        stroke:'rgba(100,100,150, 0.5)',
        fill:'rgba(0,0,0,0)'
        });
    canvas.add(circle);
}

  
 