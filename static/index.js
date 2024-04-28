socket = io();

var $nameField = $('#username')
var $teamField = $('#teamname')
var $joinButton = $('#join')
var $form = $('#form')
var $players = $('#players')

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

socket.on('updatelist', function(successData) {
    $players.empty(); // Vacía el contenido actual del elemento #players

    Object.entries(successData.teams).forEach(([key, values]) => {
        teamHtml = `<li>${key}<ul>`;
        values.forEach(value => {
            teamHtml += `<li>${successData.players[value]}</li>`;
        });
        teamHtml += `</ul></li>`;
        $players.append(teamHtml);})
});

socket.on('limit', function(successData) {
    if (!successData.success) {
        alert(`Límite de jugadores/equipos alcanzado`)
    }
});