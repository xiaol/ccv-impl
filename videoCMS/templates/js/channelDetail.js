function queryVideoId(object)
{
	var self = $(object);
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


function addRole(object)
{
	var self = $(object).parent();
	var roleName = $("#detailLeadingRole").val();
	var item = $("#directerItem-hidden").clone();
	item.find('span').text(roleName);
	item.find('input').val(roleName);
	item.attr('class','labelItem');
	item.removeAttr('id');
	self.before(item);
	
	return false;
}

function addMovieCategory(object)
{
	var self = $(object).parent();
	var movieCategory = $("#detaildetailMovieCategory").val();
	var item = $("#movieCategoryItem-hidden").clone();
	item.find('span').text(movieCategory);
	item.find('input').val(movieCategory);
	item.attr('class','labelItem');
	item.removeAttr('id');
	self.before(item);
	
	return false;
}

function extraDouban(id)
{
	url = $('[name="detailDoubanUrl"]').val();
	$.ajax({
		type:'get',
		url:'/channel/detail/extraDouban',
		data:{'id':id,'url':url},
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

function removeSelf(object)
{
	$(object).parent().remove();
}


function init()
{

}
$(document).ready(init);