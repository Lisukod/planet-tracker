function hideUi(){
    var elements = [
        document.getElementById("form-box"), 
        document.getElementById("info-box")
    ];
    for (x in elements){
        elements[x].classList.toggle("no-display");
        if (x == 0)
            elements[x].classList.toggle("form-box");
        else
            elements[x].classList.toggle("info-box");

    }
}