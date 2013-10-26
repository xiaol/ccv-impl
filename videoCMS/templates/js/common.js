
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