#!/usr/bin/env node
const path = require('path');
const app = require(path.join(__dirname, '..', 'js_bot.js'));
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`whatsapp-botjs CLI started on ${port}`));
