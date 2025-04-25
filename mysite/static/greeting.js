$(document).ready(function () {
    console.log('Doc READY');
    // Event listener for button click
    $('#greet-btn').click(function () {
        let name = $("#name").val();
        $.ajax({
            method: "POST",
            url: "/greeting",
            data: JSON.stringify({name: name}),
            contentType: "application/json; charset=utf-8"
        }).done(function (data) {
            $("#greeting").text(data.greeting);
        })
    });
});