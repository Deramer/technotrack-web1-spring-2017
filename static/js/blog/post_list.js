$( document ).ready(function () {
	show_shadows();
})

function show_shadows() {
	$( '.post-text' ).each(function(index) {
		if ($( this ).height().toString() + 'px' === $( this ).css( 'max-height' )) {
			$( this ).addClass( 'overflow' )
		}
	})
}
