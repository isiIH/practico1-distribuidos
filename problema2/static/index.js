socket = io();

var $page = $('#page')
var $joinPage = $('#join-html')
var $playPage = $('#play-html')
var $players = $('.players')
var $teamname = $('#team')
var $turn = $('#turn')
$score = $('#score')

data = {
    name: null,
    team: null,
}

socket.on('load_join', function() {
    console.log("load_join")
    $joinPage.show()
    $playPage.hide()
});

socket.on('load_play', function(playerData) {
    if(socket.id in playerData.players) {
        console.log("load_page")
        $joinPage.hide()
        $playPage.show()
        $teamname.append(`${data.team}`)
    }
});

socket.on('updatelist', function(updateData) {

    $score.text(updateData.scores[data.team])

    $players.empty(); // Vacía el contenido actual del elemento #players

    Object.entries(updateData.teams).forEach(([key, values]) => {
        teamHtml = `<li>${key} | Score: ${updateData.scores[key]}<ul>`;
        values.forEach(value => {
            teamHtml += `<li>${updateData.players[value]}</li>`;
        });
        teamHtml += `</ul></li>`;
        $players.append(teamHtml);})

    if(data.team == updateData.turn) {
        $turn.text("| Your Turn")
    } else {
        $turn.text(`| Team ${updateData.turn}'s turn`)
    }
});

// 
// Join Page
// 

var $nameField = $('#username')
var $teamField = $('#teamname')
var $joinButton = $('#join')
var $form = $('#form')
var $state = $('#state')

$joinButton.on('click', function(event) {
    event.preventDefault()
    data.name = $nameField.val()
    data.team = $teamField.val()
    socket.emit('join', data)
    $form.hide()
    $state.text("Waiting for players...")
})

socket.on('limit', function() {
    $form.show()
    $state.text(`Límite de jugadores/equipos alcanzado`)
});

socket.on('game_over', function(data) {
    alert(`${data.message}`)
    location.reload()
});

var $confDialog = $('#confirmation-dialog');
var $confMessage = $('#confirmation-message');
var $confAccept = $('#confirm-accept');
var $confReject = $('#confirm-reject');

socket.on('asktojoin', function(userData, call) {

    $confMessage.text(userData.name + " wants to join your team. Do you accept?")
    $confDialog.show()

    $confAccept.on('click', function() {
        console.log("El usuario ha aceptado unirse al equipo");
        $confDialog.hide()
        call(true, userData);
    })

    $confReject.on('click', function() {
        console.log("El usuario ha rechazado unirse al equipo");
        $confDialog.hide()
        call(false, userData);
    })
});

socket.on('reject', function(data) {
    $form.show()
    $state.text(`${data.msg}`)
});

// 
// Play Page
// 

var $dice = $('#dice')
$diceButton = $('#dice')
$diceResult = $('#diceResult')

$diceButton.on('click', function() {
    socket.emit('rolldice', data)
})

socket.on('diceresult', function(result) {
    switch(result) {
        case -1:
            alert("Espera tu turno!")
            break
        case -2:
            alert("Ya jugaste")
            break
        case -3:
            alert("Juego terminado...")
            break
        default:
            $diceResult.text(result)
    }

});