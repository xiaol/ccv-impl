function deleteResource(resourceId)
{
	if(confirm("确定删除？"))
	{
		window.location = '/resource/delete?resourceId='+resourceId;
	}
}

function toggleOnlineStatus(object)
{
	var id = $(object).attr('topicId');
	var tipText = 'changing..';
	if($(object).text() == tipText)
	{
		alert('请求已经提交，若长时间未响应请刷新页面');
		return;
	}
	$(object).text(tipText);
	$.ajax({
		type:'get',
		url:'/topic/toggleOnlineStatus',
		data:{'id':id},
		success:function(data,textStatus)
		{
			var data = JSON.parse(data);
			if (data.status == true)
			{
				$(object).attr('class','label label-warning');
				$(object).text('上线');
			}else
			{
				$(object).attr('class','label');
				$(object).text('下线');
			}
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}


function pushResource(resourceId,resourceName)
{
    $('[name=pushResourceId]').val(resourceId);
    $('#pushResourceName').text(resourceName);
    $('#pushModal').modal('show');
}

