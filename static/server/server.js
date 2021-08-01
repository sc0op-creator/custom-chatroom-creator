const http = require('http').createServer();
const io = require('socket.io')(http, {
    cors: '*',
})
io.on('connection', (socket) => {
    console.log('a user is connected')

    socket.on('message', (data) => {
        console.log(data);
        io.emit('message', data);
    });
})

http.listen(8080, () => console.log("listening on 8080 port"))