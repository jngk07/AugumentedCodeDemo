// Sample video data
const sampleVideos = [
    {
        id: 1,
        title: "Amazing Nature Documentary - Wildlife in 4K",
        channel: "Nature Explorer",
        views: "2.3M",
        uploadDate: "2 days ago",
        duration: "15:42",
        thumbnail: "https://picsum.photos/320/180?random=1",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        description: "Explore the amazing world of wildlife in stunning 4K resolution. This documentary takes you on a journey through various ecosystems and showcases the beauty of nature.",
        likes: "45K",
        subscribers: "1.2M"
    },
    {
        id: 2,
        title: "Cooking Masterclass: Perfect Pasta in 10 Minutes",
        channel: "Chef's Kitchen",
        views: "856K",
        uploadDate: "1 week ago",
        duration: "10:23",
        thumbnail: "https://picsum.photos/320/180?random=2",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
        description: "Learn how to make perfect pasta in just 10 minutes with this easy-to-follow cooking tutorial. Professional chef tips and tricks included!",
        likes: "23K",
        subscribers: "890K"
    },
    {
        id: 3,
        title: "Tech Review: Latest Smartphone Features",
        channel: "Tech Guru",
        views: "1.8M",
        uploadDate: "3 days ago",
        duration: "12:15",
        thumbnail: "https://picsum.photos/320/180?random=3",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        description: "Comprehensive review of the latest smartphone features including camera quality, battery life, and performance benchmarks.",
        likes: "67K",
        subscribers: "2.1M"
    },
    {
        id: 4,
        title: "Relaxing Music for Study and Work - 2 Hours",
        channel: "Peaceful Sounds",
        views: "5.2M",
        uploadDate: "1 month ago",
        duration: "2:00:00",
        thumbnail: "https://picsum.photos/320/180?random=4",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
        description: "2 hours of relaxing instrumental music perfect for studying, working, or meditation. Helps improve focus and concentration.",
        likes: "89K",
        subscribers: "3.5M"
    },
    {
        id: 5,
        title: "Travel Vlog: Exploring Tokyo Streets",
        channel: "World Wanderer",
        views: "1.1M",
        uploadDate: "5 days ago",
        duration: "18:30",
        thumbnail: "https://picsum.photos/320/180?random=5",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        description: "Join me as I explore the vibrant streets of Tokyo, discovering hidden gems, local food, and cultural experiences.",
        likes: "34K",
        subscribers: "750K"
    },
    {
        id: 6,
        title: "Fitness Workout: 30-Minute Full Body",
        channel: "Fit Life",
        views: "923K",
        uploadDate: "1 week ago",
        duration: "30:45",
        thumbnail: "https://picsum.photos/320/180?random=6",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
        description: "Complete 30-minute full body workout that you can do at home. No equipment needed, suitable for all fitness levels.",
        likes: "28K",
        subscribers: "1.8M"
    },
    {
        id: 7,
        title: "DIY Home Decor: Budget-Friendly Ideas",
        channel: "Creative Home",
        views: "654K",
        uploadDate: "4 days ago",
        duration: "14:20",
        thumbnail: "https://picsum.photos/320/180?random=7",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        description: "Transform your home with these budget-friendly DIY decor ideas. Easy projects that anyone can do!",
        likes: "19K",
        subscribers: "420K"
    },
    {
        id: 8,
        title: "Gaming Highlights: Epic Moments Compilation",
        channel: "Pro Gamer",
        views: "2.7M",
        uploadDate: "2 days ago",
        duration: "11:55",
        thumbnail: "https://picsum.photos/320/180?random=8",
        videoUrl: "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4",
        description: "Best gaming moments and epic plays compilation from various popular games. Incredible skills and funny moments included!",
        likes: "78K",
        subscribers: "4.2M"
    }
];

// Load videos on home page
function loadVideos() {
    const videoGrid = document.getElementById('videoGrid');
    if (!videoGrid) return;

    videoGrid.innerHTML = '';
    
    sampleVideos.forEach(video => {
        const videoCard = createVideoCard(video);
        videoGrid.appendChild(videoCard);
    });
}

// Create video card element
function createVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'video-card';
    card.onclick = () => openVideo(video.id);
    
    card.innerHTML = `
        <div class="video-thumbnail">
            <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
            <span class="video-duration">${video.duration}</span>
        </div>
        <div class="video-info">
            <h3 class="video-title">${video.title}</h3>
            <div class="video-meta">
                <div class="channel-name">${video.channel}</div>
                <div class="video-stats">
                    <span>${video.views} views</span>
                    <span>• ${video.uploadDate}</span>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Open video player page
function openVideo(videoId) {
    localStorage.setItem('currentVideoId', videoId);
    window.location.href = 'video.html';
}

// Load video details on video page
function loadVideoDetails() {
    const videoId = localStorage.getItem('currentVideoId');
    if (!videoId) return;
    
    const video = sampleVideos.find(v => v.id == videoId);
    if (!video) return;
    
    // Update video player
    const videoPlayer = document.getElementById('videoPlayer');
    if (videoPlayer) {
        videoPlayer.src = video.videoUrl;
    }
    
    // Update video information
    document.getElementById('videoTitle').textContent = video.title;
    document.getElementById('videoViews').textContent = `${video.views} views`;
    document.getElementById('videoDate').textContent = `• ${video.uploadDate}`;
    document.getElementById('likeCount').textContent = video.likes;
    document.getElementById('channelName').textContent = video.channel;
    document.getElementById('subscriberCount').textContent = `${video.subscribers} subscribers`;
    document.getElementById('videoDescription').textContent = video.description;
    
    // Load suggested videos
    loadSuggestedVideos(videoId);
}

// Load suggested videos
function loadSuggestedVideos(currentVideoId) {
    const suggestedList = document.getElementById('suggestedVideosList');
    if (!suggestedList) return;
    
    const suggestedVideos = sampleVideos.filter(v => v.id != currentVideoId).slice(0, 5);
    
    suggestedList.innerHTML = '';
    suggestedVideos.forEach(video => {
        const item = document.createElement('div');
        item.className = 'suggested-video-item';
        item.onclick = () => openVideo(video.id);
        
        item.innerHTML = `
            <div class="suggested-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
            </div>
            <div class="suggested-info">
                <h4 class="suggested-title">${video.title}</h4>
                <div class="suggested-meta">
                    <div>${video.channel}</div>
                    <div>${video.views} views • ${video.uploadDate}</div>
                </div>
            </div>
        `;
        
        suggestedList.appendChild(item);
    });
}

// Search functionality
function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (query) {
        localStorage.setItem('searchQuery', query);
        window.location.href = 'search.html';
    }
}

// Load search results
function loadSearchResults() {
    const query = localStorage.getItem('searchQuery');
    if (!query) return;
    
    document.getElementById('searchResultsTitle').textContent = `Search results for "${query}"`;
    document.getElementById('searchInput').value = query;
    
    // Filter videos based on search query
    const filteredVideos = sampleVideos.filter(video => 
        video.title.toLowerCase().includes(query.toLowerCase()) ||
        video.channel.toLowerCase().includes(query.toLowerCase()) ||
        video.description.toLowerCase().includes(query.toLowerCase())
    );
    
    const searchResults = document.getElementById('searchResults');
    if (!searchResults) return;
    
    searchResults.innerHTML = '';
    
    if (filteredVideos.length === 0) {
        searchResults.innerHTML = '<p>No results found for your search.</p>';
        return;
    }
    
    filteredVideos.forEach(video => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.onclick = () => openVideo(video.id);
        
        item.innerHTML = `
            <div class="search-thumbnail">
                <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
            </div>
            <div class="search-info">
                <h3 class="search-title">${video.title}</h3>
                <div class="search-meta">
                    ${video.channel} • ${video.views} views • ${video.uploadDate}
                </div>
                <p class="search-description">${video.description}</p>
            </div>
        `;
        
        searchResults.appendChild(item);
    });
}

// Handle Enter key in search input
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    // Load appropriate content based on current page
    const currentPage = window.location.pathname;
    if (currentPage.includes('index.html') || currentPage === '/' || currentPage.endsWith('/')) {
        loadVideos();
    } else if (currentPage.includes('video.html')) {
        loadVideoDetails();
    } else if (currentPage.includes('search.html')) {
        loadSearchResults();
    }
});

// Mobile menu toggle (for future enhancement)
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}

// Add click event to menu button
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.querySelector('.menu-btn');
    if (menuBtn) {
        menuBtn.addEventListener('click', toggleSidebar);
    }
});
