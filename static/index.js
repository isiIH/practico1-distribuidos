var socket = io()

var $nameField = $('#username')
var $teamField = $('#teamname')
var $joinButton = $('#join')

data = {
    name: null,
    team: null,
}

$joinButton.on('click', function(event) {
    event.preventDefault()
    data.name = $nameField.val()
    data.team = $teamField.val()
    socket.emit('join', data)
})

socket.on('play', function() {
    window.location = '/play' 
});

socket.on('reload', function() {
    location.reload();
});