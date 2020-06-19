const path = require('path');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);

const port = 3000;

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/test', (req, res) => {
    res.send("Hello, World!")
})

// let i = 0;
// setInterval(() => {
//     io.emit('image', i++);
// }, 1000);

io.on('connection', (socket) => {
    
    socket.on('frame', (data) => {
        io.emit('image', data);
    });

})

server.listen(port, () => console.log(`Server listening on port ${port}`));