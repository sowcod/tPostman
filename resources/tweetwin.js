function shorten(tweet, fn){
	matched = tweet.match(/(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)/g);

	var newtweet = tweet;
	var replaceCount = matched.length;
	function endCheck(){
		if (--replaceCount <= 0) fn(newtweet);
	}
	function replace(longUrl, shortUrl){
		newtweet = newtweet.replace(longUrl, shortUrl);
	}
	if (matched.length > 0) beginLoading();
	for (var i in matched) {
		$.getJSON('http://api.bit.ly/v3/shorten', {
				'longurl': matched[i],
				'login': 'sowcod',
				'apiKey': 'R_06f97544cc913bd63ab06d9a2c255ec8'
		}, function (longUrl) {
			return function(data){
				if (data.status_txt == "OK") {
					replace(longUrl, data.data.url);
				}
				endCheck();
			}
		}(matched[i]));
	}
}
function tweet(){
	msg = $('#tweetorg').val();
	key = $.cookie('sessionid').substring(0, 8);
	enc = des.encrypt(msg, key, "ecb");
	out = base64.encode(enc);
	$('#tweetarea').val(out);
	$('#textlen').val(msg.length);
	beginLoading();

	$.getJSON('/tweet', {'tweet': out}, function(data){
		if (data.result == 'success') {
			$('#tweetorg').val('');
			endLoading();
		}
	});
}
function textareadown(ev){
	if (ev.keyCode == 13 && ev.ctrlKey){
		tweet();
		ev.preventDefault();
	} else if (ev.keyCode == 85 && ev.ctrlKey && ev.shiftKey) {
		shorten($('#tweetorg').val(), function(newtweet){
			$('#tweetorg').val(newtweet);
			endLoading();
		});
	}
}
function beginLoading(){
	$('#tweetorg').attr("readonly","readonly");
	$('#loadingimg').css("visibility","visible");
}
function endLoading(){
	$('#tweetorg').attr("readonly",false);
	$('#loadingimg').css("visibility","hidden");
}
function checkLen(){
	var len = $('#tweetorg').val().length;
	var elem = $('#tweetlen');
	elem.text(len);
	if (len > 140) elem.attr('class', 'over');
	else elem.attr('class', 'normal');
}
$(document).ready(function(){
	$('#tweetorg').focus();
	$('#tweetorg').keydown(textareadown);
	$('#tweetlen').everyTime(50, function(i){
		checkLen();
	});
});
