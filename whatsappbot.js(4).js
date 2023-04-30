client.on('message', message => {
	if(message.body === '!hi') {
		message.reply('hello');
	}
});