# Instagram Mock App

A modern, responsive Instagram mock application built with HTML, CSS, and JavaScript. This app replicates the core features of Instagram including a home feed with stories, direct messages, user profiles, and an explore page.

## Features

### 🏠 Home Page (`index.html`)
- **Stories Section**: Scrollable stories bar at the top with user avatars
- **Posts Feed**: Dynamic posts with images, likes, comments, and captions
- **Interactive Elements**: Like buttons, save functionality, and user interactions
- **Responsive Design**: Works on desktop and mobile devices

### 💬 Direct Messages (`dm.html`)
- **Conversations List**: Side panel with all active conversations
- **Chat Interface**: Full-featured messaging interface
- **Variant Messages**: Messages automatically change and update every 5-10 seconds to simulate real-time conversations
- **Send Messages**: Type and send messages with automatic responses
- **Active Status**: Shows user online status

### 👤 User Account Page (`account.html`)
- **Profile Header**: Avatar, username, stats (posts, followers, following)
- **Profile Bio**: Customizable bio with location and website
- **Posts Grid**: Three-column grid of user posts
- **Tabs**: Switch between Posts, Saved, and Tagged content
- **Hover Effects**: Interactive post overlays showing likes and comments

### 🔍 Explore Page (`explore.html`)
- **Photo Grid**: Three-column grid of explore posts
- **Random Images**: Dynamic content loading
- **Hover Effects**: Visual feedback on interaction

## File Structure

```
testrepo/
├── index.html          # Home page with stories and posts
├── dm.html             # Direct messages page
├── account.html        # User profile page
├── explore.html        # Explore/discover page
├── styles.css          # All styling
├── app.js              # Home page functionality
├── dm.js               # Messages functionality with variant messages
├── account.js          # Profile page functionality
├── explore.js          # Explore page functionality
├── package.json        # npm configuration
├── vite.config.js      # Vite dev server configuration
└── README.md           # This file
```

## Getting Started

### Prerequisites
- Node.js (v14 or higher) and npm installed on your system

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**: The app will automatically open at `http://localhost:3000`

### Alternative: Run without npm

If you prefer not to use npm, you can simply open `index.html` directly in your web browser, though some features may be limited.

### Navigate the App

Use the navigation bar to switch between pages:
- Home icon → Home feed
- Paper plane icon → Direct messages
- Compass icon → Explore
- User icon → Profile

## Key Features

### Variant Messages in DM
The direct messages page includes a special feature where messages automatically change and update:
- New messages appear every 5-10 seconds
- Messages can be sent or received
- Automatic responses to your messages
- Real-time conversation simulation

### Interactive Posts
- Click the heart icon to like/unlike posts
- View post details, comments, and engagement
- Scroll through stories at the top

### Responsive Design
- Mobile-friendly layout
- Desktop-optimized with sidebars
- Smooth transitions and animations

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript (ES6+)**: Dynamic functionality
- **Vite**: Fast development server with hot module replacement
- **Font Awesome**: Icons
- **Picsum Photos**: Random placeholder images
- **Pravatar**: Avatar placeholders

## Browser Support

Works on all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Customization

You can easily customize:
- Colors and themes in `styles.css`
- Post data in `app.js`
- Message variants in `dm.js`
- Profile information in `account.html`

## Available Scripts

- `npm install` - Install all dependencies
- `npm run dev` - Start the development server (with hot reload)
- `npm run build` - Build the app for production
- `npm run preview` - Preview the production build locally

## Notes

- This is a mock application for demonstration purposes
- All images are placeholder images from external services
- No backend or database is required - everything runs client-side
- Messages and posts are generated dynamically using JavaScript
- The dev server uses Vite for fast development with hot module replacement

## Future Enhancements

Potential features to add:
- User authentication
- Real-time messaging
- Image upload
- Search functionality
- Notifications
- Stories viewing
- Post creation

Enjoy exploring the Instagram mock app! 📸✨
