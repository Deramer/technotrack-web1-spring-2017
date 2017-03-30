$( document ).ready(function () {
	$( '.js-reply' ).click(show_reply_form);
	$( '.comment-like' ).click(like_request);
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

function like_request() {
	$.ajax({
		url: 'ajax_like',
		data: {
			node_id: $( this ).attr('id').match(/\d+/g)[0],
			like: $( this ).attr('id').match(/dis/g) === null,
		},
		type: 'GET',
		dataType: 'html',
		context: this,
	})
	.done( function(html) {
		$.ajax({
			type: 'POST',
			url: 'ajax_like',
			data: $( html ).serialize(),
			dataType: 'json',
			context: this,
			success: function(json) {
				var $counter = $( '#comment-' + $( this ).attr('id').match(/\d+/g)[0] + '-counter' )
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
				var $comment = $( '#comment-' + $( this ).attr('id').match(/\d+/g)[0] )
				$comment.removeClass('comment-downvoted')
				if (json.downvoted) {
					$comment.addClass('comment-downvoted')
				} 
			}
		})
	})
}
