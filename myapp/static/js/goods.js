//颜色按钮的点击事件
$(".goods-list .color_icon").click(function(){
    var img_url = $(this).attr("pic");
    var color_id = $(this).attr("color_id");
    var color_amount = $(this).attr("color_amount");
    var img_div = $($(this).parents("li[product_id]").find(".image")[0]);
    img_div.css("background-image", "url("+img_url+")");
    img_div.attr("color_id", color_id);
    img_div.attr("color_amount", color_amount);
});



//非详情商品添加购物车
$(".rough_image span").click(function(){
    var color_amount = $(this).parent().attr('color_amount');
    var color_id = $(this).parent().attr('color_id');
    if(parseInt(color_amount) > 0){
        $(this).parent().parent().removeClass("toadd").toggleClass("carted");
        $.ajax({
            type: "POST", 
            url: '/add_to_cart/',
            data: JSON.stringify({ color_id: color_id}),
            contentType: 'application/json',
            success: function(data){
                window.location.reload();
            }
        });
    }
    else{
        var ab = $('<div class="alert-box">'+'该商品库存不足'+'</div>');
        $("body").append(ab);
        ab.show();
        window.location.reload();
    }
});

