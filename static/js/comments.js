$( document ).ready(function () {
	$( '.comment-reply' ).click(show_reply_form)
})

function show_reply_form() {
	$.ajax({
		url: "ajax_comment_form",
		data: {
			parent_id: $( this ).attr('id').match(/\d+/g)[0]
		},
		type: 'GET',
		dataType: 'html',
		context: this,
	})
	.done( function(html) {
			$( this ).parent().append(html)
	})
}
