$(".address-list .addnew").on("click",function(){
            $(".ads-mdfy").addClass("show");
        });
$(".ads-mdfy .cancel").on("click", function(){
    $(".ads-mdfy").removeAttr("address_id");
    $(".ads-mdfy").removeClass("show");
    $('#name').val('')
    $('#phone_number').val('')
    $('#province').val('')
    $('#city').val('')
    $('#region').val('')
    $('#detail_address').val('')
    $('#postcode').val('')
})
//点“编辑”，弹出表单
$(".edit_address").on("click", function(){
    var address_id = $($(this).parents('li[address_id]')[0]).attr('address_id')
    $('#address_id').val(address_id)
    $.ajax({
        type: 'GET',
        url: "/address_info/" + address_id,
        dataType: 'json',
        success: function(data){
            $('#name').val(data.name);
            $('#phone_number').val(data.phone_number);
            $('#province').val(data.province);
            $('#city').val(data.city);
            $('#region').val(data.region);
            $('#detail_address').val(data.detail_address);
            $('#postcode').val(data.postcode);
        }
    });
    $(".ads-mdfy").addClass("show");
    $(".ads-mdfy").attr("address_id", address_id)
});
//点“删除”，将该地址删除
$(".rm_address").on("click", function(){
    $($(this).parents('li[address_id]')[0]).remove()
    var address_id = $($(this).parents('li[address_id]')[0]).attr('address_id')
    $.ajax({
        type: 'POST',
        url: "",
        data: JSON.stringify({ address_id: address_id}),
        contentType: 'application/json'
    })
});