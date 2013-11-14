function deleteChannel(channelId)
{
	if(confirm("确定删除？"))
	{
		window.location = '/channel/delete?channelId='+channelId;
	}
}

function deleteAllResource(channelId)
{
	if(confirm("确定删除频道内所有视频？"))
	{
		window.location = '/resource/deleteChannelResource?channelId='+channelId;
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


function toggleProcessed(object)
{
    var channelId = $(object).attr('channelId');
    var tipText = 'changing..';
    if($(object).text() == tipText)
    {
        alert('请求已经提交，若长时间未响应请刷新页面');
        return;
    }
    $(object).text(tipText);
    $.ajax({
        type:'get',
        url:'/channel/toggleProcessed',
        data:{'channelId':channelId},
        success:function(data,textStatus)
        {
            var data = JSON.parse(data);
            if (data.status == true)
            {
                $(object).attr('class','label label-info');
                $(object).text('已处理');
            }else
            {
                $(object).attr('class','label');
                $(object).text('未处理');
            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(errorThrown);
        }
    });
}


function toggleRec(object)
{
    var channelId = $(object).attr('channelId');
    var tipText = 'changing..';
    if($(object).text() == tipText)
    {
        alert('请求已经提交，若长时间未响应请刷新页面');
        return;
    }
    $(object).text(tipText);
    $.ajax({
        type:'get',
        url:'/channel/toggleRec',
        data:{'channelId':channelId},
        success:function(data,textStatus)
        {
            var data = JSON.parse(data);
            if (data.status == true)
            {
                $(object).attr('class','label label-warning');
                $(object).text('已推荐');
            }else
            {
                $(object).attr('class','label');
                $(object).text('未推荐');
            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown)
        {
            alert(errorThrown);
        }
    });
}


function setCompleted(channelId)
{
    if(confirm("设置完结？"))
    {
        $.ajax({
            type:'get',
            url:'/channel/setCompleted',
            data:{'channelId':channelId},
            success:function(data,textStatus)
            {
                window.location = window.location;
            },
            error:function(XMLHttpRequest, textStatus, errorThrown)
            {
                alert(errorThrown);
            }
        });
    }
}

function pushChannel(channelId,channelName)
{
    $('[name=pushChannelId]').val(channelId);
    $('#pushChannelName').text(channelName);
    $('#pushModal').modal('show');
}

function init()
{
    $('#datetimepicker1').datetimepicker({
      language: 'pt-BR',
      pick12HourFormat: false
    });
}

$(document).ready(init);
