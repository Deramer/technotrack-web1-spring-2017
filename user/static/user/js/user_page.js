$( document ).ready( function () {
	$( '.user-subscribe' ).click( subscribe )
})

function subscribe(event) {
	event.preventDefault()
	$.ajax({
		url: $( this ).attr( 'href' ),
		type: 'POST',
		data: {
			'csrfmiddlewaretoken': $( 'meta[name=csrf]' ).attr( 'content' ),
		},
		dataType: 'json',
	})
	.done( function(json) {
		if (json.status === 'OK') {
			$( '.user-subscribe' ).after( '<p>Subscribed!</p>' )
			$( '.user-subscribe' ).remove()
		}
	})
}
