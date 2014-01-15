/**
 * Created with PyCharm.
 * User: ding
 * Date: 14-1-15
 * Time: 下午4:39
 * To change this template use File | Settings | File Templates.
 */


function flagRead(object,id)
{
	$.ajax({
		type:'get',
		url:'/message/flagRead',
		data:{'id':id},
		success:function(data,textStatus)
		{
		},
		error:function(XMLHttpRequest, textStatus, errorThrown)
		{
			alert(errorThrown);
		}
	});
    var item = $(object).parents('.hoverHighLight');
    item.fadeOut(300);
    //item.remove();
}
