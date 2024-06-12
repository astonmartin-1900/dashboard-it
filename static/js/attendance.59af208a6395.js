//////////////// POP-UP FORM ///////////////
function openForm() {
    var element = document.getElementById("popup");
    element.classList.add("show");
    document.body.style.overflowY = "hidden";
}
function closeForm() {
    var element = document.getElementById("popup");
    element.classList.remove("show");
    document.body.style.overflowY = "scroll";
}
