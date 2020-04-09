const clapBtn = document.getElementById('clap')
const clapsCount = document.getElementById('claps_count')
const id = clapBtn.getAttribute('data-id')
const model = document.getElementById('btn-model')

const showModel = () => {
    model.click()  
}

const setupBtnStyle = (isLiked) => {
    if(isLiked) {
        clapBtn.className = "btn btn-primary"
        clapBtn.innerText = "Like"
        clapBtn.removeAttribute('data-liked')
        clapsCount.textContent = Number(clapsCount.textContent) - 1
    } else {
        clapBtn.className = "btn btn-warning"
        clapBtn.innerText = "Unlike"
        clapBtn.setAttribute('data-liked', true)
        clapsCount.textContent = Number(clapsCount.textContent) + 1
    }
}

const toggleClap = (e) => {
    const isLiked = e.target.getAttribute('data-liked')? true:false 
    let url

    if(isLiked) {
        url = `/articles/${id}/clap/delete`
    } else {
        url = `/articles/${id}/clap/`
    }

    fetch(url)
    .then(res => {
        if(res.status === 201) {
            setupBtnStyle(isLiked)
        } else if(res.redirected) {
            console.log('you should login first')
            showModel()
        }
    })
}

clapBtn.addEventListener('click', toggleClap)