# 🎥 YouTube Clone - Getting Started

## Quick Start

### Option 1: Direct Browser Access (Recommended)
1. Open `test.html` in your web browser to see the overview
2. Click on "Home Page" to start using the YouTube Clone
3. No server setup required!

### Option 2: Local Server (For full functionality)
1. Run the server script:
   ```bash
   ./start-server.sh
   ```
   Or manually:
   ```bash
   python3 server.py --open
   ```
2. Open your browser to `http://localhost:8000/test.html`

## 📁 Project Structure

```
youtube-clone/
├── 📄 index.html           # Home page with video grid
├── 📄 video.html           # Video player page
├── 📄 search.html          # Search results page
├── 📄 test.html            # Test/overview page
├── 📄 README.md            # Detailed documentation
├── 📄 GETTING_STARTED.md   # This file
├── 📄 server.py            # Local development server
├── 📄 start-server.sh      # Server startup script
├── 📁 css/
│   └── 📄 styles.css       # Main stylesheet
├── 📁 js/
│   └── 📄 script.js        # JavaScript functionality
├── 📁 images/              # Thumbnail images
└── 📁 videos/              # Video files directory
```

## 🚀 Features

### ✅ Implemented Features
- **Home Page**: Video grid with 8 sample videos
- **Video Player**: Full-featured video player with controls
- **Search**: Real-time search through video content
- **Responsive Design**: Works on all device sizes
- **Navigation**: Header, sidebar, and page routing
- **YouTube-like UI**: Dark theme with familiar styling

### 📱 Pages
1. **Home (`index.html`)**: Main video grid
2. **Video Player (`video.html`)**: Individual video viewing
3. **Search (`search.html`)**: Search results and filtering

### 🎬 Sample Content
- 8 diverse video categories (Nature, Cooking, Tech, Music, Travel, Fitness, DIY, Gaming)
- Realistic metadata (views, upload dates, channel info)
- Placeholder thumbnails and video sources

## 🔧 How It Works

### Navigation Flow
1. **Home → Video**: Click any video thumbnail
2. **Video → Suggested**: Click suggested videos in sidebar
3. **Search**: Use search bar from any page
4. **Back to Home**: Click logo or use browser back button

### Data Storage
- Uses browser's Local Storage for state management
- Maintains current video ID and search queries
- No backend database required

### Responsive Behavior
- **Desktop**: Full sidebar + video grid
- **Tablet**: Collapsible sidebar + responsive grid
- **Mobile**: Hidden sidebar + single column layout

## 🎯 Testing Guide

### Basic Functionality
1. ✅ Load home page and see video grid
2. ✅ Click video to open player page
3. ✅ Search for videos using search bar
4. ✅ Navigate between pages
5. ✅ Test responsive design (resize browser)

### Advanced Features
1. ✅ Video player controls work
2. ✅ Suggested videos load correctly
3. ✅ Search filters work properly
4. ✅ Mobile menu toggles (on small screens)
5. ✅ State persists between page loads

## 🛠️ Customization

### Adding New Videos
Edit `js/script.js` and add to the `sampleVideos` array:
```javascript
{
    id: 9,
    title: "Your Video Title",
    channel: "Your Channel",
    views: "1M",
    uploadDate: "1 day ago",
    duration: "10:30",
    thumbnail: "path/to/thumbnail.jpg",
    videoUrl: "path/to/video.mp4",
    description: "Video description...",
    likes: "50K",
    subscribers: "2M"
}
```

### Styling Changes
Modify `css/styles.css` to change:
- Colors and theme
- Layout and spacing
- Typography and fonts
- Responsive breakpoints

### Adding New Pages
1. Create new HTML file
2. Include CSS and JS files
3. Add navigation links
4. Update JavaScript routing

## 🌐 Browser Compatibility

### Fully Supported
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Partially Supported
- ⚠️ Internet Explorer (basic functionality only)
- ⚠️ Older mobile browsers

## 🔍 Troubleshooting

### Common Issues

**Videos not loading?**
- Check video URLs in `script.js`
- Ensure proper CORS headers for video files
- Try using the local server option

**Search not working?**
- Verify JavaScript is enabled
- Check browser console for errors
- Clear browser cache and reload

**Responsive design issues?**
- Test in different browsers
- Check CSS media queries
- Verify viewport meta tag

**Page navigation broken?**
- Check file paths are correct
- Ensure all HTML files are in same directory
- Verify JavaScript routing logic

## 📞 Support

If you encounter issues:
1. Check the browser console for errors
2. Verify all files are in correct locations
3. Try using the local server option
4. Test in a different browser

## 🎉 Success!

You now have a fully functional YouTube clone with:
- ✅ 3 interactive pages
- ✅ Video player functionality
- ✅ Search capabilities
- ✅ Responsive design
- ✅ YouTube-like interface

Enjoy exploring your YouTube clone! 🚀
