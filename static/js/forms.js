const groups = document.querySelectorAll('.form-group')

groups.forEach(group => {
    const input = group.children[1]

    if(input.type !== 'file') input.classList.add('form-control')
})