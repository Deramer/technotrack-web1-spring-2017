$( document ).ready(function () {
	$( '#header-mobile-icon' ).click(mobile_menu)
	correct_footer_position()
	$( window ).resize(correct_footer_position)
})

function mobile_menu() {
	$li = $( '.header-list li' ).not( '.header-mobile' ).not( '.header-avatar' )
	if ($li.hasClass( 'header-show' )) {
		$li.removeClass( 'header-show' )
	} else {
		$li.addClass( 'header-show' )
	}
}

function correct_footer_position() {
	dif = $( '#sidebar' ).height() - $( '#content' ).height()
	if (dif > 0) {
		$( '#footer' ).css('margin-top', dif.toString() + 'px')
	} else {
		$( '#footer' ).css('margin-top', '0px')
	}
}
