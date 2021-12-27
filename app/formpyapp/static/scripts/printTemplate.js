// adapted from https://developer.mozilla.org/en-US/docs/Web/Guide/Printing

function closePrint() {
    document.body.removeChild(this.__container__);
}

function setPrint() {
    this.contentWindow.__container__ = this;
    this.contentWindow.onbeforeunload = closePrint;
    this.contentWindow.onafterprint = closePrint;
    this.contentWindow.focus(); // Required for IE
    this.contentWindow.print();
}

function printPage(btn) {
    let imgSrc = btn.parentElement.parentElement.parentElement.getElementsByTagName("img")[0].src
    let oHideFrame = document.createElement("iframe");
    oHideFrame.onload = setPrint;
    oHideFrame.style.position = "fixed";
    oHideFrame.style.right = "0";
    oHideFrame.style.bottom = "0";
    oHideFrame.style.width = "0";
    oHideFrame.style.height = "0";
    oHideFrame.style.border = "0";
    oHideFrame.src = imgSrc;
    document.body.appendChild(oHideFrame);
}