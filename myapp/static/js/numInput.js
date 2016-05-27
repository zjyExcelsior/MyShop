var numInput = function ($) {
    $(".number-pick").each(function(i){
        var ipt = $(this).children("span"),
            that = $(this);

        $(this).children(".add").on("click",function(){
            var _v = parseInt(ipt.text());
            if(_v == "0"){
                that.removeClass("zero");
            }
            ipt.text(++_v);
        });

        $(this).children(".dec").on("click",function(){
            var _v = parseInt(ipt.text());
            if(_v == "0"){
                that.addClass("zero");
                return;
            }
            ipt.text(--_v);
        });
    });
}(Zepto);
