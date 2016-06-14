var cmn = function($) {
    var header = {
        icon: $(".menu-icon"),
        menuList: $(".menu-list"),
        searchBar: $("#search"),
        searchInput: $("#search input"),
        searchSubmit: $("#search .submit")
    };

    function toggleStatus(el, config, callback) {
        var evt = config.evt || "click",
            className = config.className || "active",
            status = false;
        el.on(evt, function() {
            $(this).toggleClass(className);
            status = !status;
            if(callback){
                callback.call(el);
            }
        });
    }


    toggleStatus(header.icon, {
        className: "open"
    }, function() {
        header.menuList.toggle();
    });

    header.searchBar.on("click",function() {
        $(this).addClass("active");
        $("body").one("scroll", function() {
            header.searchBar.removeClass("active");
        });
        header.searchSubmit.one("click", function() {
            if(header.searchBar.hasClass("active")){
                header.searchBar.submit();
            }
        });
    });

    return {
        toggleStatus: toggleStatus
    };
}(Zepto);

$(".logo").click(function(){
    window.location.href = '/';
});