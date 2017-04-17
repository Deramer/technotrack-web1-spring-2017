$( document ).ready(function () {
	$( '.js-reply' ).click(show_reply_form);
	$( '.generic-like' ).click(like_request);
})

function show_reply_form() {
	$.ajax({
		url: "ajax_comment_form",
		data: {
			parent_id: $( this ).attr( 'id' ).match(/post/g) !== null ? -1 : $( this ).attr('id').match(/\d+/g)[0]
		},
		type: 'GET',
		dataType: 'html',
		context: this,
	})
	.done( function(html) {
			$( this ).parent().append(html)
	})
}

function like_request() {
	$.ajax({
		url: "ajax_like",
		type: 'POST',
		data: {
			'model': $( this ).data( 'model' ),
			'id': $( this ).data( 'id' ),
			'status': $( this ).data( 'status' ),
			'csrfmiddlewaretoken': $( "meta[name=csrf]" ).attr( 'content' ),
		},
		dataType: 'json',
		context: this,
	})
	.done( function(json) {
		if (json.result !== 'OK') {
			console.log(json.result)
			return
		}
		var $counter = $( '#comment-' + $( this ).data( 'id' ) + '-counter' )
		if ( $counter.length !== 0 ) {
			var $comment = $( '#comment-' + $( this ).data( 'id' ) )
			$comment.removeClass('comment-downvoted')
			if (json.downvoted) {
				$comment.addClass('comment-downvoted')
			}
		} else {
			$counter = $( '#post-' + $( this ).data( 'id' ) + '-counter' )
		}
		$counter.html(Math.abs(json.likes_num))
		$counter.removeClass('comment-counter-negative comment-counter-zero comment-counter-positive')
		if (json.likes_num < 0) {
			$counter.addClass('comment-counter-negative')
		}
		if (json.likes_num === 0) {
			$counter.addClass('comment-counter-zero')
		}
		if (json.likes_num > 0) {
			$counter.addClass('comment-counter-positive')
		}
	})
}
