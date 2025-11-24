// Sample posts data
const postsData = [
    {
        id: 1,
        username: 'sarah_m',
        avatar: 'https://i.pravatar.cc/150?img=1',
        image: 'https://picsum.photos/600/600?random=1',
        likes: 1234,
        caption: 'Beautiful sunset today! 🌅',
        time: '2 hours ago',
        comments: 45
    },
    {
        id: 2,
        username: 'james_k',
        avatar: 'https://i.pravatar.cc/150?img=2',
        image: 'https://picsum.photos/600/600?random=2',
        likes: 892,
        caption: 'Coffee and coding ☕️💻',
        time: '5 hours ago',
        comments: 23
    },
    {
        id: 3,
        username: 'emily_r',
        avatar: 'https://i.pravatar.cc/150?img=3',
        image: 'https://picsum.photos/600/600?random=3',
        likes: 2156,
        caption: 'Weekend vibes ✨',
        time: '1 day ago',
        comments: 67
    },
    {
        id: 4,
        username: 'mike_t',
        avatar: 'https://i.pravatar.cc/150?img=4',
        image: 'https://picsum.photos/600/600?random=4',
        likes: 567,
        caption: 'New project coming soon! 🚀',
        time: '2 days ago',
        comments: 12
    },
    {
        id: 5,
        username: 'lisa_w',
        avatar: 'https://i.pravatar.cc/150?img=5',
        image: 'https://picsum.photos/600/600?random=5',
        likes: 3456,
        caption: 'Nature is healing 🌿',
        time: '3 days ago',
        comments: 89
    }
];

// Initialize posts
function initPosts() {
    const postsContainer = document.getElementById('postsContainer');
    if (!postsContainer) return;

    postsContainer.innerHTML = '';

    postsData.forEach(post => {
        const postElement = createPostElement(post);
        postsContainer.appendChild(postElement);
    });
}

// Create post element
function createPostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post';
    postDiv.innerHTML = `
        <div class="post-header">
            <img src="${post.avatar}" alt="${post.username}" class="post-avatar">
            <a href="#" class="post-username">${post.username}</a>
            <div class="post-more">
                <i class="fas fa-ellipsis"></i>
            </div>
        </div>
        <img src="${post.image}" alt="Post" class="post-image">
        <div class="post-actions">
            <i class="far fa-heart post-action like-btn" data-post-id="${post.id}"></i>
            <i class="far fa-comment post-action"></i>
            <i class="far fa-paper-plane post-action"></i>
            <i class="far fa-bookmark post-action post-save"></i>
        </div>
        <div class="post-likes" id="likes-${post.id}">${formatNumber(post.likes)} likes</div>
        <div class="post-caption">
            <a href="#" class="username">${post.username}</a> ${post.caption}
        </div>
        <div class="post-comments">View all ${post.comments} comments</div>
        <div class="post-time">${post.time}</div>
    `;

    // Add like functionality
    const likeBtn = postDiv.querySelector('.like-btn');
    const likesElement = postDiv.querySelector(`#likes-${post.id}`);
    let isLiked = false;
    let currentLikes = post.likes;

    likeBtn.addEventListener('click', () => {
        isLiked = !isLiked;
        if (isLiked) {
            likeBtn.classList.remove('far');
            likeBtn.classList.add('fas', 'liked');
            currentLikes++;
        } else {
            likeBtn.classList.remove('fas', 'liked');
            likeBtn.classList.add('far');
            currentLikes--;
        }
        likesElement.textContent = `${formatNumber(currentLikes)} likes`;
    });

    return postDiv;
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initPosts);

