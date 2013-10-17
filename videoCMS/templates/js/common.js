
function goPage(page)
{
	$("[name='page']").val(page);
	$("#form_nav").submit();
}

function init()
{
    $('.dropdown-toggle').parent().mouseout(function()
    {
       $(this).find('.dropdown-toggle').dropdown("toggle");
    });
    $('.dropdown-toggle').parent().mouseover(function()
    {
       $(this).find('.dropdown-toggle').dropdown("toggle");
    });
}


$(document).ready(init);