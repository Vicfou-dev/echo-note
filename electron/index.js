const path = require('path');
const { PythonShell } = require('python-shell');

document.addEventListener("DOMContentLoaded", () => {
	var startButton = document.getElementById('start_button');
	startButton.disabled = true;

	document.getElementById('upload_file').addEventListener('change', function () {
		var fileInfo = document.getElementById('file_info');
		if (this.files.length > 0) {
			fileInfo.textContent = 'Selected file : ' + this.files[0].name;
		} else {
			fileInfo.textContent = 'No file selected';
		}
		startButton.disabled = this.files.length === 0;
		fileInfo.classList.remove('hidden');
	});

	var copyButton = document.getElementById('copy_button');
	var transcription = document.getElementById('transcription');

	var alert = document.getElementById('alert');
	copyButton.addEventListener('click', function () {

		transcription.select();
		transcription.setSelectionRange(0, 99999); 


		document.execCommand('copy');

		transcription.blur();

		alert.classList.add('show');

		setTimeout(function () {
			alert.classList.remove('show');
		}, 3000);
	});

	document.getElementById('start_button').addEventListener('click', function () {
		this.classList.add('loading');
		const url = document.getElementById('upload_file').files[0].path;
		const name = document.getElementById('model').value
		const jsonArg = JSON.stringify({ url: url, name: name })

		let options = {
			mode: 'text',
			pythonOptions: ['-u'], 
			scriptPath: path.join(__dirname, '..', 'python'),
			args: [jsonArg]
		};

		const success = (messages) => {
			const message = messages[0];
			message.replace(/\\/g, '');
			const text = JSON.parse(message).text;
			document.getElementById('transcription').innerHTML = text.trim();
		}

		const error = (error) => {
			console.log(error);
			document.getElementById('transcription').innerHTML = 'An error occurred';
		}

		const end = () => {
			this.classList.remove('loading');
		}

		PythonShell.run('whisper.py', options).then(success).catch(error).finally(end);
	})
});