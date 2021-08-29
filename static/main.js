function getToken(auth){
    const endpoint = '/api/token/';
    var request = $.post(endpoint, auth)
        .done(res => {
            const token = res.access;
            localStorage.setItem('accessToken', res.access)
            localStorage.setItem('refreshToken', res.refresh)
            window.location.replace("/")
        })
        .fail(err => {
            console.log(err);
        });
}
function refreshToken(){
    const refreshToken = localStorage.getItem('refreshToken');
    $.post('/api/token/refresh/', {'refresh':refreshToken})
    .done(res => {
        localStorage.setItem('accessToken', res.access)
    })
    .fail(err => {
        console.log(err)
    });
}


$('#loginForm').submit(function(event){
    event.preventDefault();
    const user = $('#user').val();
    const password = $('#password').val();
    const auth = {
        "commercial_registration_num": user,
        "password": password
    }
    getToken(auth);
})

function loadItems(){
    const accessToken = localStorage.getItem('accessToken');

    headers={
        "Authorization": `Bearer ${accessToken}`
    }
    $.ajax({
    type: "GET",
    url: '/api/notes/',
    headers: headers,
    success: function(data){
        data.forEach(item => {
            $('#content').append(`
                <div class="col-sm-3">
                    <div class="card" style="width: 18rem;">
                        <div class="card-body">
                            <h5 class="card-title">${item.title}</h5>
                            <p class="card-text">${item.note}</p>
                        </div>
                    </div>
                </div>
            `)
        });

    },
    error: function(err){
        if(err.status === 401){
            if(accessToken){
                refreshToken();
                loadItems()
            } else {
                window.location.replace("/login")
            }
        }
    }
    });
}


$('#registerForm').submit(function(event){
    event.preventDefault();
    const user = $('#user').val();
    const email = $('#email').val();
    const email2 = $('#email2').val();
    const password = $('#password').val();
    
    const form = {
        "commercial_registration_num": user,
        "email": email,
        "email2": email2,
        "password": password
    }
    console.log(form)
    $.post('/api/create-user/',form)
        .done(res => {
            auth = {
                "commercial_registration_num": user,
                "password": password,
            }
            getToken(auth)
        })
        .fail(res => {
            console.log(res)
        });
})

