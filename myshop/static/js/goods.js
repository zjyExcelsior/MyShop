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
        $(this).removeClass("toadd").text("").toggleClass("carted");
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

        $(document).bind("mouseup", function(e){
            if($(".alert-box")){
                var target = $(e.target);
                if(target != $(".alert-box")){
                    $(".alert-box").remove();
                }
            }
        });
        // window.location.reload();
    }
});

//移入鼠标出现“加入购物车”按钮，移出消失
if(document.body.clientWidth > 1024){
    $('.rough_image').on("mouseenter", function(){
        $(this).find('span').addClass("toadd").show();
    });
    $('.rough_image').on("mouseleave", function(){
        $(this).find('span').hide();
    }); 
}

