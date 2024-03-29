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

function lookupDanmu(object)
{
	var id = $(object).attr('resourceId');

	$.ajax({
		type:'get',
		url:'/resource/lookupDanmu',
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

function setTobeReview(object)
{
	var resourceId = $(object).attr('resourceId');

    $.ajax({
		type:'get',
		url:'/resource/review',
		data:{'id':resourceId,'review':-2},
		success:function(data,textStatus)
		{
            alert('放入审核成功，等待管理员审核..');
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
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


function changeReviewMode(reviewMode)
{
    $('[name="review"]').val(reviewMode);
    $('#form_nav').submit();
}

function review(resourceId,review,reason)
{
    $.ajax({
		type:'get',
		url:'/resource/review',
		data:{'id':resourceId,'review':review,'reason':reason},
		success:function(data,textStatus)
		{

		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}

function rejectWithReason(resourceId,object)
{
    var rejectReason = $(object).parent();
    var reason = rejectReason.find('input:checked').next().text();
    if(reason.indexOf("12 其他") != -1)
    {
        reason += rejectReason.find('[name="customReason"]').val();
    }
    console.log(reason);
    review(resourceId,-1,reason);
    console.log(rejectReason.parent('.rejectItem').prev().prev().find('input'));
    rejectReason.prev().prev().find('input').iCheck('check');
    rejectReason.hide();
}

function pendAll()
{
    $('[review="0"]').iCheck('check');
}

function acceptAll()
{
    $('[review="1"]').iCheck('check');
}

function rejectAll()
{
    $('[review="-1"]').iCheck('check');
}

function batch_review()
{
    var tobeList = [];
    $('[review="0"]:checked').each(function()
    {
        tobeList.push($(this).attr('id').substring(3));
    });
    var acceptList = [];
    $('[review="1"]:checked').each(function()
    {
        acceptList.push($(this).attr('id').substring(3));
    });
    var rejectList = [];
    $('[review="-1"]:checked').each(function()
    {
        rejectList.push($(this).attr('id').substring(3));
    });
    $('.batch-operation-save').text('正在保存...');
    $('.batch-operation-save')[0].onclick = undefined;
    $.ajax({
		type:'post',
		url:'/resource/batch_review',
		data:{'tobeList':tobeList,'acceptList':acceptList,'rejectList':rejectList},
		success:function(data,textStatus)
		{
            window.location.reload();
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});

}


function init()
{
    $('#datetimepicker1').datetimepicker({
      language: 'pt-BR',
      pick12HourFormat: false
    });

    $('input[review="0"]').iCheck({
        checkboxClass: 'icheckbox_square-aero',
        radioClass: 'iradio_square-aero'
    });
    $('input[review="1"]').iCheck({
        checkboxClass: 'icheckbox_square-blue',
        radioClass: 'iradio_square-blue'
    });
    $('input[review="-1"]').iCheck({
        checkboxClass: 'icheckbox_square-red',
        radioClass: 'iradio_square-red'
    });


    $('.review-status input').iCheck({
    checkboxClass: 'icheckbox_square-purple',
    radioClass: 'iradio_square-purple'
    });

    // 单个审核
    if(singleReview)
    $('.topicItem input').on('ifChecked', function(event){
        var target = $(event.target);
        console.log('event',event);
        if(target.attr('review') != "-1")
        review(target.attr('id').substring(3), target.attr('review'),'')
    });
    //批量审核

    //切换状态
    $('.review-status input').on('ifChecked', function(event){
        var target = $(event.target);
        changeReviewMode(target.val());
    });
}

$(document).ready(init);
