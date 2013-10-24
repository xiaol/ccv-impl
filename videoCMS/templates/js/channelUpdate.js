function onImageChange(object)
{
	var reader = new FileReader();
	reader.onload = function(evt)
	{
		$($(object).prev()[0]).attr('src',evt.target.result);
		$($(object).next()[0]).val(evt.target.result);
	} 
	reader.readAsDataURL(object.files[0]);
}

function addSourceInput(object)
{
	var p = $($(object).prev()[0]);
	var newone = p.clone();
	newone.find("input").val("");
	p.after(newone);
}

function deleteSourceInput(object)
{
	$(object).parent().remove();
}


function applyDurationAll(channelId,object)
{
	var channelId = channelId;
	var duration = $('*[name="duration"]').val();
	
	var tipText = '请求ing...';
	if($(object).text() == tipText)
	{
		alert('请求已经提交，若长时间未响应请刷新页面');
		return;
	}
	$(object).text(tipText);
	$.ajax({
		type:'get',
		url:'/channel/updateDuration',
		data:{'channelId':channelId,'duration':duration},
		success:function(data,textStatus)
		{
			alert('更新成功');
			$(object).text('应用所有');
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}


function disperseUpdateTime(channelId, object)
{
	if(channelId == '')
    {
        alert('请先保存之后再打散！');
        return;
    }
    $(object).val("正在请求..");
	$.ajax({
		type:'get',
		url:'/channel/disperseUpdateTime',
		data:{'channelId':channelId},
		success:function(data,textStatus)
		{
            $(object).val("打散视频");
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}

function calcSeconds()
{
	var minutes = $("#secondBox").val();
	$("[name=\"duration\"]").val(minutes *60);
}


function setHandleFrequent(num)
{
	$('*[name="handleFrequents"]').val(num);
}


function setHandleFrequentHours(object)
{
	var num = $(object).val() * 3600; 
	$('*[name="handleFrequents"]').val(num);
}

function setHandleFrequentMinutes(object)
{
	var num = $(object).val() * 60; 
	$('*[name="handleFrequents"]').val(num);
}




function showTips(e)
{
	$(e.target).popover('show');
}

function hideTips(e)
{
	$(e.target).popover('hide');
}

function init()
{
	$('[data-toggle="popover"]').bind("mouseover",showTips);
	$('[data-toggle="popover"]').bind("mouseout",hideTips);
}
$(document).ready(init);