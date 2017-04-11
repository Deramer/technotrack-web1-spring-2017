$( document ).ready(function () {
	$( '.button-create-blog' ).click(blog_form)
})

function blog_form() {
	$.ajax({
		url: 'create',
		type: 'GET',
		dataType: 'html',
	})
	.done( function (html) {
		$( 'body' ).prepend( html )
		$( '.form-background' ).click(remove_form)
		$( '.form-content .form-close' ).click(remove_form)
	})
}

function remove_form() {
	$( '.form-background' ).remove()
	$( '.form-content' ).remove()
}
