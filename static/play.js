var socket = io()

var $dice = $('#dice')
$score = $('#score')


$joinButton.on('click', function(event) {
    event.preventDefault()
    data.name = $nameField.val()
    data.team = $teamField.val()
})