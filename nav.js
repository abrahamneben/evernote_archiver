function change_focus(self){
	document.getElementsByClassName('selected')[0].className = '';
	self.className = 'selected';
}

note_tags = document.getElementsByTagName('a');
num_notes = note_tags.length;
function arrow_up_or_down(e){
	selected_ind = Array.from(note_tags).map(function (t){return t.className}).indexOf('selected');

	if (e.keyCode == '38' && selected_ind > 0){ // up arrow
		note_tags[selected_ind].className = '';
		note_tags[selected_ind-1].className = 'selected';
		note_tags[selected_ind-1].click();
	}
	if (e.keyCode == '40' && selected_ind < num_notes - 1){ // down arrow
		note_tags[selected_ind].className = '';
		note_tags[selected_ind+1].className = 'selected';
		note_tags[selected_ind+1].click();
	}
}
document.onkeydown = arrow_up_or_down;
