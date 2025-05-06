function cardHTML(post) {
    return `
        <div class="tarjeta">
            <h2>${ post.title }}</h2>
            <p>${ post.content.slice(0,100)}...</p>
            <a href="/post/${post.id}/">Lee el post</a>

            <ul><p style="font-size: small; margin-top: 10px;">Tags:</p>
            ${post.tags.map(
                t => `<li><a class="taglink" href="/post_by_tag/${t.id}/">${t.name}</a></li>`
            ).join('')}
            </ul>
        </div>`;
}

function loadPosts(page = 1){
    fetch(`/api/posts/?page=${page}`)
        .then(r => r.json())
        .then(json => {
            const lista = Array.isArray(json) ? json : json.results;

            const cont = document.querySelector('.grid');
            lista.forEach(p => cont.insertAdjacentHTML('beforeend', cardHTML(p)));
            nextPage = json.next ??= null;
        })
        .catch(err => console.error('Error al cargar los posts:', err));
}

let nextPage = 1;
loadPosts(nextPage);