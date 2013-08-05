function deleteChannel(channelId)
{
	if(confirm("确定删除？"))
	{
		window.location = '/channel/delete?channelId='+channelId;
	}
}

function updateNow(channelId)
{
	$.ajax({
		type:'get',
		url:'/channel/updateSearchNow',
		data:{'channelId':channelId},
		success:function(data,textStatus)
		{
			alert("标记成功,稍后会更新");
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}


function resetWeight(channelId)
{
    $.ajax({
        type:'get',
        url:'/channel/resetWeight',
        data:{'channelId':channelId},
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