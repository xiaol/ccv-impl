function openGetVideoUrl()
{
    var videoType = $('[name="videoType"]').val();
    var videoId = $('[name="videoId"]').val();

    var url = "/resource/getVideoUrl?videoType="+videoType+"&videoId="+videoId;
    window.open(url);
}

function queryVideoId()
{
	var url = $("#videoURL").val();

	$.ajax({
		type:'post',
		url:'/resource/getVideoId',
		data:{'url':url},
		success:function(data,textStatus)
		{
			var data = JSON.parse(data);
			$('*[name="videoType"]').val(data.videoType);
			$('*[name="videoId"]').val(data.videoId);
            if(data.exists)
            {
                if(confirm("警告：此视频已存在,是否跳转到该视频？"))
                {
                    window.location = '/resource/index?id='+data.id;
                }
            }
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
}

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


function calcSeconds()
{
	var minutes = $("#secondBox").val();
	$("[name=\"duration\"]").val(minutes *60);
}


function onSubmit()
{
    /*alert($('[name="tagList"]').val().replace("，",","));
    alert($('[name="tagList"]').val().replace("，",",").split(",").length);*/
    var tagStr = $('[name="tagList"]').val().replace( /^\s+|\s+$/g, '').replace(/，/g,",");
    if(tagStr=="" || tagStr.split(",").length < 3)
    {
        alert("标签列表至少填写3个标签！");
        return false;
    }
    return true;
}


function onIsRecommendChange(object)
{
    var self = $(object);
    if(self.val() == "是")
    {
        $('#genderSelect').show();
         $('#genderSelect select').removeAttr('disabled');
    }else
    {
        $('#genderSelect').hide();
        $('#genderSelect select').attr('disabled','disabled');
    }
}

function checkTextLength()
{

    var input = $('[name="resourceName"]');

    $('#resourceNameLeft').text(60-input.val().length);
    if(input.val().length > 60)
    {

    }

}

function init()
{
	$('#datetimepicker1').datetimepicker({
      language: 'pt-BR',
      pick12HourFormat: false
    });
    checkTextLength();
}
$(document).ready(init);