function main(){
	$.ajax({url: "/current/",
				dataType: 'json',
				success: function(json) {
					if(json.status == "PLAYING")
						showNowPlaying(json.data);
					else
						document.getElementById('track_info').innerHTML = "Not Playing";
				}
			});
}

function sendCommand(action){
	$.ajax({url: "/action/?action=" + action,
				dataType: 'json',
				success: function(json) {
					if(json.status == "PLAYING")
						showNowPlaying(json.data);
					else
						document.getElementById('track_info').innerHTML = "Not Playing";
				}
			});
}

function showNowPlaying(track){
	var html = '<table>';

	var titles = 	['Title', 'Artist', 'Album'];
	var elems = 	['title','artist', 'album'];
	for(var i in elems)
		html+='<tr><td class="title"><strong>' + titles[i] + ':</strong></td>' + '<td class="data">'+ track[elems[i]] + '</td></tr>';
	
	html+= '</table>';
		
	document.getElementById('track_info').innerHTML = html;
	
	html = '<img src="' + track.artUrl + '"/>';
	document.getElementById('art_work').innerHTML = html; 
}

main();
