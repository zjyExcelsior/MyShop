var addressList = function(list, ads, editcallback) {
    var ads_list = [];

    function add(a) {
        var item = $('<li><div class="head"><span class="name">' + a.name + '</span><span class="remove hoverYellow">删除</span><span class="edit hoverYellow">编辑</span></div><ul class="detail"><li class="number">' + a.number + '</li><li class="city">' + a.province + a.city + a.area + '</li><li class="location">' + a.location + '</li></ul></li>');
        var _t = {
            data: a,
            item: item,
            modify: function(ad) {
                item.find(".name").text(ad.name);
                item.find(".number").text(ad.number);
                item.find(".city").text(ad.province + ad.city + ad.area);
                item.find(".location").text(ad.location);
            }
        };
        item.find(".remove").on("click", function() {
            item.remove();
        });
        item.find(".edit").on("click", function() {
            editcallback.call(_t);
        });
        list.prepend(item);
        return _t;
    }
    if (ads) {
        ads.forEach(function(item) {
            var ads = add(item);
            ads_list.push(ads);
        });
    }
    return {
        list: ads_list,
        add: add
    };
};
var addressEdit = function(usredt, al) {
    var input = {
        name: usredt.find(".name"),
        number: usredt.find(".number"),
        province: usredt.find(".province"),
        city: usredt.find(".city"),
        area: usredt.find(".area"),
        location: usredt.find(".location")
    };

    function setAddress(ads) {
        input.name.val(ads.name || "");
        input.number.val(ads.number || "");
        input.province.val(ads.province || "");
        input.city.val(ads.city || "");
        input.area.val(ads.area || "");
        input.location.val(ads.location || "");
    }

    function getAddress() {
        return {
            name: input.name.val(),
            number: input.number.val(),
            province: input.province.val(),
            city: input.city.val(),
            area: input.area.val(),
            location: input.location.val()
        };
    }
    usredt.find(".cancel").on("click", function() {
        $(".ads-mdfy").removeClass("show");
    });
    return {
        setAddress: setAddress,
        getAddress: getAddress
    };
};