var lastItem;

function callback(json){
	var currentItem = JSON.stringify(json.data);
	if(currentItem != lastItem){
		lastItem = currentItem;
		if(json.status == "PLAYING" && json.data.artist != 'Spotify') 
		//Not showing data for ads
			renderHTML(json.data);
		else
			renderHTML({artUrl: '/static/img/no_art.gif'})
	}
}

function getNowPlaying(){
	var wait = 10 * 1000;
	var reloadNowPlaying;
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
	var html;
	if(track.artist){ 
	//Means we have something playing and not ads
		html = '<table>';
		var titles 	= 	['Title', 'Artist', 'Album'];
		var elems	= 	['title','artist', 'album'];
		for(var i in elems)
			html+='<tr><td class="title"><strong>' + titles[i] +
			 ':</strong></td>' + '<td class="data">'+ track[elems[i]] + '</td></tr>';
	
		html+= '</table>';
		
		document.getElementById('track_info').innerHTML = html;
	}
		
	html = '<img class="artwork" src="' + track.artUrl + '" width="90" height="90" />';
	document.getElementById('art_work').innerHTML = html; 
}

getNowPlaying();
