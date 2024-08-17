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

// carregamento assincrono de conteudo
document.addEventListener("DOMContentLoaded", function() {
    let lazyImages = [].slice.call(document.querySelectorAll("img.lazy-load"));

    if ("IntersectionObserver" in window) {
        let lazyImageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.onload = function() {
                        lazyImage.classList.add('loaded');
                    }
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function(lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    } else {
        // Fallback para browsers que não suportam IntersectionObserver
        lazyImages.forEach(function(lazyImage) {
            lazyImage.src = lazyImage.dataset.src;
            lazyImage.onload = function() {
                lazyImage.classList.add('loaded');
            }
        });
    }
})