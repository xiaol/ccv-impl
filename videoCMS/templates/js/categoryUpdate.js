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

function addSourceInput(object)
{
	var p = $($(object).prev()[0]);
	var newone = p.clone();
	newone.val("");
	p.after(newone);
}

function deleteSourceInput(object)
{
	$(object).parent().remove();
}


