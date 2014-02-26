function ReadClipboardData(e) {
    e = e.originalEvent;
    for (var i = 0; i < e.clipboardData.items.length; i++) {
       if (e.clipboardData.items[i].kind == "file" && e.clipboardData.items[i].type == "image/png") {
         // get the blob
         var imageFile = e.clipboardData.items[i].getAsFile();
         // read the blob as a data URL
         var fileReader = new FileReader();
         fileReader.onloadend = function(e) {
         // create an image
         var image = document.createElement("IMG");
         image.src = this.result;
         image.id  = "snapshot_" +($('.snapshot img').length+1) ;
         $('.snapshot').append(image);

         //$('[name="image"]').val(this.result);

         // insert the image
         /*
         var range = window.getSelection().getRangeAt(0);
         range.insertNode(image);
         range.collapse(false);
         // set the selection to after the image

         var selection = window.getSelection();
         selection.removeAllRanges();
         selection.addRange(range);*/
       };
      fileReader.readAsDataURL(imageFile);
      // prevent the default paste action
      e.preventDefault();
      break;
     }
  }
}

//获取图片真实大小


function onDrop(e)
{
    console.log('drop');
    var id = e.originalEvent.dataTransfer.getData('text');
    //原始图
    var srcImage = $('#'+id);
    var src = srcImage.attr('src');
    //原始图大小
    var naturalWidth = srcImage[0].naturalWidth;
    var naturalHeight = srcImage[0].naturalHeight;
    //div 大小
    var divWidth = $(e.target).parent()[0].offsetWidth;
    var divHeight = $(e.target).parent()[0].offsetHeight;
    //缩放后图片大小
    var imageHeight = divHeight;
    var imageWidth = 1.0*imageHeight/naturalHeight*naturalWidth;

    console.log(naturalWidth,naturalHeight,divWidth,divHeight,imageHeight,imageWidth);


    if(src != "")
    {
        e.target.src = src;
        e.target.style.width = ""+imageWidth+"px";
        e.target.style.height = ""+imageHeight+"px";
        e.target.style.left = ""+(divWidth - imageWidth)/2 +"px";

        $('[name="'+$(e.target).attr('target')+'"]').val(src);

        checkAlright() ?
            $('#submit').removeClass('disabled'):
            $('#submit').addClass('disabled');

    }
}

function onDragStart(e)
{
    console.log('start');
    e.originalEvent.dataTransfer.setData('text', e.srcElement.id);
}

function allowDrop(ev)
{
    ev.preventDefault();
}

// 切换样式
function changeStyle(event)
{
    //将 预览数据 更新到 表单
    $('.preview .active img').each(function(i,e){
        var src = $(e).attr('src');
        //阻止默认图
        if(src.indexOf('/static/img/') != -1)
        {
            src = "";
        }
        $('[name="'+$(e).attr('target')+'"]').val(src);
    });

    //设置 style 数据
    $('[name="style"]').val($(event.target).attr('sty'));
    //设置保存按钮状态
    checkAlright() ?
            $('#submit').removeClass('disabled'):
            $('#submit').addClass('disabled');
}

function checkAlright()
{
    if( $('[name="style"]').val() == "1")
    {
        if( $('[name="image1"]').val() != "")
        {
            return true
        }
    }
    else if ( $('[name="style"]').val() == "2" || $('[name="style"]').val() == "3")
    {
        if($('[name="image1"]').val() != "" && $('[name="image2"]').val() != "" && $('[name="image3"]').val() != "" )
        {
            return true
        }
    }
    return false;
}



function addPasteListener()
{
    $('.snapshot img').live('dragstart',onDragStart);
    $('.preview img').bind('dragstart',onDragStart);
    $('.preview img').bind('drop',onDrop);
    $('.preview img').bind('dragover',allowDrop);

    $('.style a[data-toggle="tab"]').on('shown',changeStyle);
    $('.main-tabs a').bind('mouseenter',function(){
        $(this).tab('show');
    });

    $('#snap_content').bind('paste',ReadClipboardData);
}

$(document).ready(addPasteListener);