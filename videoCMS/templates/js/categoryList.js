function resetWeight(categoryId)
{
    $.ajax({
        type:'get',
        url:'/category/resetWeight',
        data:{'categoryId':categoryId},
        success:function(data,textStatus)
        {
            alert("重置成功!");
        },
        error:function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(errorThrown);
        }
    });
}