// Sample profile posts data
const profilePostsData = Array.from({ length: 12 }, (_, i) => ({
    id: i + 1,
    image: `https://picsum.photos/300/300?random=${i + 20}`
}));

// Initialize profile
function initProfile() {
    initProfilePosts();
    initTabs();
}

// Initialize profile posts
function initProfilePosts() {
    const postsGrid = document.getElementById('profilePostsGrid');
    if (!postsGrid) return;

    postsGrid.innerHTML = '';

    profilePostsData.forEach(post => {
        const postElement = createProfilePostElement(post);
        postsGrid.appendChild(postElement);
    });
}

// Create profile post element
function createProfilePostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'profile-post-item';
    postDiv.innerHTML = `
        <img src="${post.image}" alt="Post ${post.id}">
        <div class="post-overlay">
            <span><i class="fas fa-heart"></i> ${Math.floor(Math.random() * 1000)}</span>
            <span><i class="fas fa-comment"></i> ${Math.floor(Math.random() * 100)}</span>
        </div>
    `;

    postDiv.addEventListener('mouseenter', () => {
        const overlay = postDiv.querySelector('.post-overlay');
        if (overlay) overlay.style.display = 'flex';
    });

    postDiv.addEventListener('mouseleave', () => {
        const overlay = postDiv.querySelector('.post-overlay');
        if (overlay) overlay.style.display = 'none';
    });

    return postDiv;
}

// Initialize tabs
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all tabs
            tabButtons.forEach(b => b.classList.remove('active'));
            
            // Add active class to clicked tab
            btn.classList.add('active');
            
            const tab = btn.dataset.tab;
            
            // Handle tab switching
            switch(tab) {
                case 'posts':
                    showPosts();
                    break;
                case 'saved':
                    showSaved();
                    break;
                case 'tagged':
                    showTagged();
                    break;
            }
        });
    });
}

// Show posts
function showPosts() {
    const postsGrid = document.getElementById('profilePostsGrid');
    if (!postsGrid) return;
    
    postsGrid.innerHTML = '';
    profilePostsData.forEach(post => {
        const postElement = createProfilePostElement(post);
        postsGrid.appendChild(postElement);
    });
}

// Show saved posts
function showSaved() {
    const postsGrid = document.getElementById('profilePostsGrid');
    if (!postsGrid) return;
    
    postsGrid.innerHTML = '';
    
    // Show saved posts (different images)
    const savedPosts = Array.from({ length: 6 }, (_, i) => ({
        id: i + 1,
        image: `https://picsum.photos/300/300?random=${i + 50}`
    }));
    
    savedPosts.forEach(post => {
        const postElement = createProfilePostElement(post);
        postsGrid.appendChild(postElement);
    });
}

// Show tagged posts
function showTagged() {
    const postsGrid = document.getElementById('profilePostsGrid');
    if (!postsGrid) return;
    
    postsGrid.innerHTML = '';
    
    // Show tagged posts (different images)
    const taggedPosts = Array.from({ length: 4 }, (_, i) => ({
        id: i + 1,
        image: `https://picsum.photos/300/300?random=${i + 70}`
    }));
    
    taggedPosts.forEach(post => {
        const postElement = createProfilePostElement(post);
        postsGrid.appendChild(postElement);
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initProfile);



