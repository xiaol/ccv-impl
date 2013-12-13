function HtmlEncode(text)
{
return text.replace(/\n/g,'').replace(/\r/g,'').replace(/&/g, '&amp').replace(/\"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/,/\'/);

}
function HtmlDecode(text)
{
return text.replace(/&amp;/g, '&').replace(/&quot;/g, '\"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
}


function goPage(page)
{
	$("[name='page']").val(page);
	$("#form_nav").submit();
}

function init()
{
    $('.mydropdown').parent().mouseout(function()
    {
       $(this).find('.dropdown-menu').toggle();
    });
    $('.mydropdown').parent().mouseover(function()
    {
       $(this).find('.dropdown-menu').toggle();
    });
}


$(document).ready(init);