
function goPage(page)
{
	$("[name='page']").val(page);
	$("#form_nav").submit();
}