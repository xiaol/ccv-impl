function deleteResource(resourceId)
{
	if(confirm("确定删除？"))
	{
		window.location = '/resource/delete?resourceId='+resourceId;
	}
}

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


function stopSnapshot(object)
{
	var id = $(object).attr('resourceId');
	window.location = "/resource/stopSnapshot?id=" + id;
}


function unsetInvalid(object,id)
{
	$.ajax({
		type:'get',
		url:'/resource/unsetInvalid',
		data:{'id':id},
		success:function(data,textStatus)
		{
			if(data == 'ok')
			{
				//alert('请求成功');
				$(object).parent().remove();
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



function addToBaBa(object,resourceId)
{
    $(object).text("发送中...");
    $.ajax({
		type:'get',
		url:'/topic/addResourceToNewestBaBa',
		data:{'resourceId':resourceId},
		success:function(data,textStatus)
		{
            alert(data);
            $(object).text("+Baba视频");

		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
            $(object).text("+Baba视频");
		}
	});
}


function init()
{
    $('#datetimepicker1').datetimepicker({
      language: 'pt-BR',
      pick12HourFormat: false
    });

    /*$('input').iCheck({
    checkboxClass: 'icheckbox_square-blue',
    radioClass: 'iradio_square-blue',
  });*/
}

$(document).ready(init);
