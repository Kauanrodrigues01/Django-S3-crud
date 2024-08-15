coracoes = document.querySelectorAll('.heart')

coracoes.forEach(coracao => {
    coracao.addEventListener('click', function(evt) {
        let coracao = evt.target
        if (coracao.getAttribute('src') == '/static/assets/%C3%ADcones/1x/heart-fill.svg'){
            coracao.setAttribute('src', '/static/assets/%C3%ADcones/1x/favorite_outline.png')
        }  
        else{
            coracao.setAttribute('src', '/static/assets/%C3%ADcones/1x/heart-fill.svg')
        }
    })
})