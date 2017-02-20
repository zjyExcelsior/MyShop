var alertBox = function(text){
    var ab = $('<div class="alert-box">'+text+'</div>');

    $("body").append(ab);
    return function(){
        ab.show();
        $("body").one("click",function(){
            ab.hide();
        });
    };
};