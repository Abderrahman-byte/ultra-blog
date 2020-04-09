const tagsDivs = document.querySelectorAll('.tag-div')
const saveBtn = document.getElementById('save')
const token = document.querySelector('#csrf>input')
const successAlert = document.getElementById('success-alert')

successAlert.style.display = 'none'

tagsDivs.forEach(div => {
    div.addEventListener('click', (e) => {
        div.classList.toggle('selected')
    })
})

const success = () => {
    successAlert.style.display = 'block'

    setTimeout(() => successAlert.style.display = 'none', 3000)
}

saveBtn.addEventListener('click', (e) => {
    const form = new FormData()
    let fav_tags = []
    const csrf_token = token.value

    tagsDivs.forEach(div => {
        if(div.classList.contains('selected')) {
            fav_tags.push(div.getAttribute('data-id'))
        }
    })

    fetch('/auth/fav_tags/update/', {
        method: 'POST',
        body: JSON.stringify({fav_tags}),
        headers: {
            'X-CSRFToken': csrf_token
        }
    }).then(() => {
        success()
    })
})