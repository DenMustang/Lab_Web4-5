function checkTypeInputValue() {
    var name = document.forms["myForm"]["name"].value;
    var visitors = document.forms["myForm"]["visitors"].value;
    var rooms = document.forms["myForm"]["rooms"].value;

    var regex_str = /^[a-zA-Z]+$/;
    var regex_num = /^[0-9]+$/;
    if (!name.match(regex_str) || !visitors.match(regex_num) ||!rooms.match(regex_num)
        ) {
    } 

}