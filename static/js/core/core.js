$( document ).ready(function () {
	$( '#header-mobile-icon' ).click(mobile_menu)
	correct_footer_position()
	$( window ).resize(correct_footer_position)
	setTimeout(refresh_sidebar, 5000)
	$( '.login-button' ).click(show_login_form)
	$( '.signup-button' ).click(show_login_form)
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
	if (dif > 0 && $( '#sidebar' ).css('position') !== 'static') {
		$( '#footer' ).css('margin-top', dif.toString() + 'px')
	} else {
		$( '#footer' ).css('margin-top', '0px')
	}
}

function refresh_sidebar() {
	$.ajax({
		url: '/ajax_refresh_sidebar',
		data: { from_time: $( '.sidebar-timestamp' ).html() },
		type: 'GET',
		dataType: 'html',
	})
	.done( function(html) {
		if ($( html ).length === 0) return;
		len = $( html ).filter( '.sidebar-element' ).length
		if (len > 0) {
			$( '#sidebar' ).children().slice(-len).remove()
		}
		$( '#sidebar' ).find( '.sidebar-timestamp' ).remove()
		$( '#sidebar' ).prepend( html )
		setTimeout(refresh_sidebar, 5000)
	})
}

function show_login_form(event) {
	event.preventDefault()
	$.ajax({
		url: $( this ).attr( 'href' ),
		type: 'GET',
		dataType: 'html',
	})
	.done( function (html) {
		$( 'body' ).prepend( html )
		$( '.form-background' ).click(remove_form)
		$( '.form-content .form-close' ).click(remove_form)
		$( '.form-content form' ).submit(send_login_form)
	})
}

function send_login_form(event) {
	event.preventDefault()
	$.ajax({
		url: $( this ).attr( 'action' ),
		type: 'POST',
		data: $( this ).serialize(),
		dataType: 'html',
	})
	.done( function(html) {
		$( '.form-background' ).remove()
		$( '.form-content' ).remove()
		if ($( html ).find( '.form-close' ).length !== 0) {
			$( 'body' ).prepend( html )
			$( '.form-background' ).click(remove_form)
			$( '.form-content .form-close' ).click(remove_form)
			$( '.form-content form' ).submit(send_login_form)
		} else {
			location = location
		}
	})
}

function remove_form() {
	$( '.form-background' ).remove()
	$( '.form-content' ).remove()
}
