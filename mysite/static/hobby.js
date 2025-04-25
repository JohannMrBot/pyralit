document.getElementById('submit-hobby-add').addEventListener('click', function (event) {
    event.preventDefault();
    let form = event.target.form;

    // Create a FormData object
    let formData = new FormData(form);

    // Get form values
    let name = formData.get('name');

    console.log(name);
    $.ajax({
        method: "POST",
        url: "/hobby/",
        data: JSON.stringify({name: name}),
        contentType: "application/json; charset=utf-8"
    }).done(function (data) {

        let hobby =
            div("list-group-item d-flex flex-row align-items-center justify-content-between",
                [div("d-flex flex-row align-items-center",
                    [anchor(
                        "btn btn-default btn-xs",
                        data.href,
                        data.name
                    )]
                )]
            )

        $("#hobby-container").append(hobby);

    })
});

document.querySelector('.hobby-input').addEventListener('change', function (event) {
    console.log(event.target.value);
})

document.querySelector('.hobby-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        console.log('Enter key was pressed!');
        console.log(event.target.value);
        $.ajax({
            method: "POST",
            url: "/hobby/",
            data: JSON.stringify({name: name}),
            contentType: "application/json; charset=utf-8"
        })
    }
})

function div(className, children = []) {
    let element = document.createElement("div");
    element.className = className;
    children.forEach(child => {
        element.append(child);
    })
    return element;
}

function anchor(className, href, text, children = []) {
    let element = document.createElement("a");
    element.className = className;
    element.href = href;
    element.text = text;
    children.forEach(child => {
        element.append(child);
    })
    return element;
}

function editHobby(id) {
    $(`#hobby-anchor-${id}`).hide();
    $(`#hobby-input-${id}`).show();
    console.log(id);
}

