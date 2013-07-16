function toggleOnlineStatus(object)
{
	var id = $(object).attr('resourceId');
	var tipText = 'changing..';
	if($(object).text() == tipText)
	{
		alert('请求已经提交，若长时间未响应请刷新页面');
		return;
	}
	$(object).text(tipText);
	$.ajax({
		type:'get',
		url:'/resource/toggleOnlineStatus',
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

function refreshSnapshot(object)
{
	var id = $(object).attr('resourceId');

	$.ajax({
		type:'get',
		url:'/resource/refreshSnapshot',
		data:{'id':id},
		success:function(data,textStatus)
		{
			if(data != 'ok')
			{
				alert('请求失败');
				
			}else
			{
				alert('请求成功');
			}
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}
