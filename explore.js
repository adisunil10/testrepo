// Generate explore posts
const explorePostsData = Array.from({ length: 21 }, (_, i) => ({
    id: i + 1,
    image: `https://picsum.photos/300/300?random=${i + 100}`
}));

// Initialize explore page
function initExplore() {
    const exploreGrid = document.getElementById('exploreGrid');
    if (!exploreGrid) return;

    exploreGrid.innerHTML = '';

    explorePostsData.forEach(post => {
        const postElement = createExplorePostElement(post);
        exploreGrid.appendChild(postElement);
    });
}

// Create explore post element
function createExplorePostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'explore-item';
    postDiv.innerHTML = `<img src="${post.image}" alt="Explore post ${post.id}">`;

    postDiv.addEventListener('click', () => {
        // Could navigate to post detail page
        console.log('Clicked explore post:', post.id);
    });

    return postDiv;
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initExplore);

