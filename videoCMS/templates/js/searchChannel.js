function searchChannel()
{
    var keyword = $("#searchKeyword").val();
    $.ajax({
        type:'get',
        url:'/channel/search',
        data:{'keyword':keyword},
        success:function(data,textStatus)
        {
            data = JSON.parse(data);
            for(var i=0;i<data.length; ++i)
            {
                var item = data[i];
                var r = $("#SearchResultRow").clone();
                r.removeAttr("id");
                r.removeAttr("class");

                r.find('.searchChannel_Id').text(item['channelId']);
                r.find('.searchChannel_Name').text(item['channelName']);
                r.find('.searchChannel_Name').attr('href','/channel/update?id='+item['id']);
                $('#SearchResultRow').after(r);

            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(errorThrown);
        }
    });
}

function select(object)
{
    var channelId = $(object).parent().parent().find('.searchChannel_Id').text();
    var channelName = $(object).parent().parent().find('.searchChannel_Name').text();
    $('[name="channelId"]').val(channelId);
    $('#channelName').text(channelName);
    $('#channelName').attr('href','/channel/index?channelId='+channelId);
}