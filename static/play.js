socket = io();

var $dice = $('#dice')
$score = $('#score')
$players = $('#players')
$diceButton = $('#dice')
$diceResult = $('#diceResult')

$diceButton.on('click', function() {
    socket.emit('rolldice')
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
            $diceResult.textContent(result)
    }

});