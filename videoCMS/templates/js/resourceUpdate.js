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




function init()
{
	$('#datetimepicker1').datetimepicker({
      language: 'pt-BR',
      pick12HourFormat: false
    });
}
$(document).ready(init);