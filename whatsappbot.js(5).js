client.on('message', message => {
	if(message.body === '!ping') {
		client.sendMessage(message.from, 'pong');
	}
});