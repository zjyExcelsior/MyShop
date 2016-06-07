//颜色按钮的点击事件
$(".goods-list .color_icon").on("click", function(){
    var img_url = $(this).attr("pic");
    var color_id = $(this).attr("color_id");
    var img_div = $($(this).parents("li[product_id]").find(".image")[0]);
    img_div.css("background-image", "url("+img_url+")");
    img_div.attr("color_id", color_id);
});