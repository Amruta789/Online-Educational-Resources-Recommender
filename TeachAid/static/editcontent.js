function getFormData(contentid) {
    var $editContentForm = $('#editContentForm'+contentid)
    $.getJSON('/'+contentid+'/updatecontent', function(result) {
        $editContentForm.find('input,textarea').each(function() {       
            var $item = $(this)
            if($item.attr('id')==='title'){
                $item.val(result['title'])
            }
            if($item.attr('id')==='description'){
               $item.val(result['description'])
            }
            if($item.attr('id')==='url'){
                $item.val(result['url'])
            }
        })
    })
}

function deleteFile(contentid) {
    $.post('/'+contentid+'/deletefile',{id: contentid},  ()=> {
        $('#filename'+contentid).hide()
        if($('#fileicon'+contentid).length !== 0){
            $('#fileicon'+contentid).hide()
        }            
        $('#filedelete'+contentid).hide()
    })
}
