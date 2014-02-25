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
         $('[name="image"]').val(this.result);

         // insert the image
         var range = window.getSelection().getRangeAt(0);
         range.insertNode(image);
         range.collapse(false);
         // set the selection to after the image

         var selection = window.getSelection();
         selection.removeAllRanges();
         selection.addRange(range);
       };
      fileReader.readAsDataURL(imageFile);
      // prevent the default paste action
      e.preventDefault();
      break;
     }
  }
}

function ReadClipboardData2(e) {
    for (var i = 0; i < e.clipboardData.items.length; i++)
     {
       if (e.clipboardData.items[i].kind == "file" && e.clipboardData.items[i].type == "image/png")
       {
         var imageFile = e.clipboardData.items[i].getAsFile();
         var fileReader = new FileReader();
         fileReader.onloadend = function(e)
         {
             // create an image
             var image = document.createElement("IMG");
             image.src = this.result;
             $('[name="image"]').val(this.result);

             // insert the image
             var range = window.getSelection().getRangeAt(0);
             range.insertNode(image);
             range.collapse(false);
             // set the selection to after the image

             var selection = window.getSelection();
             selection.removeAllRanges();
             selection.addRange(range);

         };
         fileReader.readAsDataURL(imageFile);
         // prevent the default paste action
         e.preventDefault();
         break;
      }
  }
}

function addPasteListener()
{
    //document.addEventListener("paste",ReadClipboardData);
    $('#snap_content').bind("paste",ReadClipboardData);

}

$(document).ready(addPasteListener);