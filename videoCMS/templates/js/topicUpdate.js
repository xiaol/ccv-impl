/**
 * Created with PyCharm.
 * User: ding
 * Date: 13-12-13
 * Time: 下午2:25
 * To change this template use File | Settings | File Templates.
 */
var IMG_INTERFACE = 'http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/50/50/';
var SEARCH_CHANNEL_RESULT;
var SEARCH_RESOURCE_RESULT;

//=========================================


function domSwapTop(object)
{
	var top = $($(object).parent().children()[0]);
	console.log(top);
	if(top.length != 0)
	{
		top.before($(object));
	}
}

function domSwapDown(object)
{

	var next = $(object).next();
	if(next.length != 0)
	{
		next.after($(object));
	}
}

function domSwapUp(object)
{
	var pre = $(object).prev();
	//console.log(pre);
	if(pre.length != 0)
	{
		pre.before($(object));
	}
}

function domRemove(object)
{
	$(object).remove();
}


function addChannel(channel)
{
    var item = $($("#topicItemTemplate").find(".topicItem")[0]).clone();
    item.attr("type","channel");
    item.attr("channelId",channel.channelId);
    item.find('img').attr('src',IMG_INTERFACE+channel.channelImageUrl);
    item.find('a').text(channel.channelName);
    item.find('a').attr('href',"/channel/index?channelId="+channel.channelId);
    item.prepend($("#elementToolbar").clone(true));
    $("#content").append(item);
}

function addResource(resource)
{
    var item = $($("#topicItemTemplate").find(".topicItem")[0]).clone();
    item.attr("type","resource");
    item.attr("resourceUd",resource.id);
    item.find('img').attr('src',IMG_INTERFACE+resource.resourceImageUrl);
    item.find('a').text(resource.resourceName);
    item.find('a').attr('href',"/resource/index?id="+resource.id);
    item.prepend($("#elementToolbar").clone(true));
    $("#content").append(item);
}

function showAddChannelModal()
{
	$('#AddChannelModal').modal('show');
}

function showAddResourceModal()
{
	$('#AddResourceModal').modal('show');
}

function onSearchChannelSuc(data,textStatus){
		$('#channelSearchResult').find('tr').remove();
		SEARCH_CHANNEL_RESULT = JSON.parse(data);
        var ret = SEARCH_CHANNEL_RESULT;
		for(var i=0; i<ret.length; ++i)
		{
			var params = "SEARCH_CHANNEL_RESULT["+i+"]";
			var s='<tr><td><a href="/channel/update?channelId='+ret[i].channelId+'" target="_blank">'+ret[i].channelName+'</a></td>\
			<td><a class="btn btn-small" onclick="addChannel('+params+')">添加</a></td></tr>';
			$('#channelSearchResult').find('table').append(s);
		}
	}

function searchChannelByName()
{
	var name = $('#channelSearch').val();
	$.ajax({url:"/channel/search",type:"get",data:{keyword:name},success:onSearchChannelSuc
	,
	error:function(XMLHttpRequest, textStatus, errorThrown)
	{
		alert(textStatus);
	}
	});
}

function searchChannelById()
{
    var name = $('#channelSearch').val();
	$.ajax({url:"/channel/searchChannelId",type:"get",data:{channelId:name},success:onSearchChannelSuc
	,
	error:function(XMLHttpRequest, textStatus, errorThrown)
	{
		alert(textStatus);
	}
	});
}



function onSearchResourceSuc(data,textStatus)
{
    $('#resourceSearchResult').find('tr').remove();
    SEARCH_RESOURCE_RESULT = JSON.parse(data);
    var ret = SEARCH_RESOURCE_RESULT;
    for(var i=0; i<ret.length; ++i)
    {
        var params = "SEARCH_RESOURCE_RESULT["+i+"]";
        var s='<tr><td><a href="/resource/update?id='+ret[i].id+'" target="_blank">'+ret[i].resourceName+'</a></td>\
        <td><a class="btn btn-small" onclick="addResource('+params+')">添加</a></td></tr>';
        $('#resourceSearchResult').find('table').append(s);
    }
}

function searchResourceByName()
{
	var name = $('#resourceSearch').val();
	$.ajax({url:"/resource/search",type:"get",data:{keyword:name},success:onSearchResourceSuc,
	error:function(XMLHttpRequest, textStatus, errorThrown)
	{
		alert(textStatus);
	}
	});
}

function searchResourceById()
{
    var id = $('#resourceSearch').val();
	$.ajax({url:"/resource/searchResourceId",type:"get",data:{id:id},success:onSearchResourceSuc,
	error:function(XMLHttpRequest, textStatus, errorThrown)
	{
		alert(textStatus);
	}
	});
}


function loadData()
{
    var data = JSON.parse(HtmlDecode($("[name='content']").val()));
    for(var i=0;i<data.length;++i)
    {
        if(data[i].type=="channel")
        {
            addChannel(data[i]);
        }else if (data[i].type=="resource")
        {
            addResource(data[i]);
        }
    }
}

function dumpData()
{
    var content = $('.topicItem');
    var ret= [];
    for(var i=0; i< content.length;++i)
    {
        var item = $(content[i]);
        if(item.attr("type") == "channel")
        {
            ret.push({type:"channel",channelId:parseInt(item.attr('channelId'))});
        }else if (item.attr("type") == "resource")
        {
            ret.push({type:"resource",resourceId:item.attr('resourceId') });
        }
    }

    $('[name="content"]').val(JSON.stringify(ret));
}


function OnSubmit()
{
    dumpData();
    return true;
}

$(document).ready(function()
{
   loadData();
});



