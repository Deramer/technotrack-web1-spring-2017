$( document ).ready(function () {
	$( '#header-mobile-icon' ).click(mobile_menu)
})

function mobile_menu() {
	$li = $( '.header-list li' ).not( '.header-mobile' ).not( '.header-avatar' )
	if ($li.hasClass( 'header-show' )) {
		$li.removeClass( 'header-show' )
	} else {
		$li.addClass( 'header-show' )
	}
}
