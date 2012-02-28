var wait = 10 * 1000;
var reloadNowPlaying;

function callback(json){
	if(json.status == "PLAYING")
		renderHTML(json.data);
	else
		document.getElementById('track_info').innerHTML = "Not Playing";
}

function getNowPlaying(){
	$.ajax({url: "/current/",
				dataType: 'json',
				success: callback
			});
	reloadNowPlaying = setTimeout(getNowPlaying, wait);
}

function sendCommand(action){
	$.ajax({url: "/action/?action=" + action,
				dataType: 'json',
				success: callback
			});
}

function renderHTML(track){
	var html = '<table>';

	var titles = 	['Title', 'Artist', 'Album'];
	var elems = 	['title','artist', 'album'];
	for(var i in elems)
		html+='<tr><td class="title"><strong>' + titles[i] + ':</strong></td>' + '<td class="data">'+ track[elems[i]] + '</td></tr>';
	
	html+= '</table>';
		
	document.getElementById('track_info').innerHTML = html;
	
	html = '<img src="' + track.artUrl + '" width="90" height="90" />';
	document.getElementById('art_work').innerHTML = html; 
}

getNowPlaying();
