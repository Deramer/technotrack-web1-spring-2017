$( document ).ready(function () {
	show_shadows();
	$( '.button-create-post' ).click(post_form)
})

function show_shadows() {
	$( '.post-text' ).each(function(index) {
		if ($( this ).height().toString() + 'px' === $( this ).css( 'max-height' )) {
			$( this ).addClass( 'overflow' )
		}
	})
}

function post_form() {
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
