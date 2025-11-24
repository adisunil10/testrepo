// Sample conversations data
const conversationsData = [
    {
        id: 1,
        name: 'sarah_m',
        avatar: 'https://i.pravatar.cc/150?img=1',
        preview: 'Hey! How are you?',
        time: '2m',
        unread: true
    },
    {
        id: 2,
        name: 'james_k',
        avatar: 'https://i.pravatar.cc/150?img=2',
        preview: 'Thanks for the help!',
        time: '1h',
        unread: false
    },
    {
        id: 3,
        name: 'emily_r',
        avatar: 'https://i.pravatar.cc/150?img=3',
        preview: 'See you tomorrow!',
        time: '3h',
        unread: true
    },
    {
        id: 4,
        name: 'mike_t',
        avatar: 'https://i.pravatar.cc/150?img=4',
        preview: 'That sounds great!',
        time: '5h',
        unread: false
    },
    {
        id: 5,
        name: 'lisa_w',
        avatar: 'https://i.pravatar.cc/150?img=5',
        preview: 'Can we meet up?',
        time: '1d',
        unread: true
    }
];

// Variant messages that will change
const variantMessages = [
    [
        { text: 'Hey! How are you doing?', time: '2:30 PM', sent: false },
        { text: 'I\'m doing great, thanks for asking!', time: '2:31 PM', sent: true },
        { text: 'That\'s awesome! Want to grab coffee later?', time: '2:32 PM', sent: false }
    ],
    [
        { text: 'Did you see the new update?', time: '10:15 AM', sent: false },
        { text: 'Yes! It looks amazing!', time: '10:16 AM', sent: true },
        { text: 'I know right? So excited about it!', time: '10:17 AM', sent: false }
    ],
    [
        { text: 'Are you free this weekend?', time: '3:45 PM', sent: false },
        { text: 'Yes, I should be! What\'s up?', time: '3:46 PM', sent: true },
        { text: 'Want to go hiking?', time: '3:47 PM', sent: false }
    ],
    [
        { text: 'Thanks for your help today!', time: '11:20 AM', sent: false },
        { text: 'No problem at all! Happy to help!', time: '11:21 AM', sent: true },
        { text: 'You\'re the best!', time: '11:22 AM', sent: false }
    ],
    [
        { text: 'Can you send me that file?', time: '4:10 PM', sent: false },
        { text: 'Sure! Sending it now.', time: '4:11 PM', sent: true },
        { text: 'Got it, thanks!', time: '4:12 PM', sent: false }
    ]
];

let currentConversationId = 1;
let messageVariants = {};

// Initialize conversations
function initConversations() {
    const conversationsList = document.getElementById('conversationsList');
    if (!conversationsList) return;

    conversationsList.innerHTML = '';

    conversationsData.forEach(conv => {
        const convElement = createConversationElement(conv);
        conversationsList.appendChild(convElement);
    });

    // Load first conversation
    loadConversation(1);
}

// Create conversation element
function createConversationElement(conv) {
    const convDiv = document.createElement('div');
    convDiv.className = 'conversation-item';
    convDiv.dataset.convId = conv.id;
    convDiv.innerHTML = `
        <img src="${conv.avatar}" alt="${conv.name}" class="conversation-avatar">
        <div class="conversation-info">
            <div class="conversation-name">${conv.name}</div>
            <div class="conversation-preview">${conv.preview}</div>
            <div class="conversation-time">${conv.time}</div>
        </div>
    `;

    convDiv.addEventListener('click', () => {
        loadConversation(conv.id);
        document.querySelectorAll('.conversation-item').forEach(item => {
            item.classList.remove('active');
        });
        convDiv.classList.add('active');
    });

    return convDiv;
}

// Load conversation messages
function loadConversation(convId) {
    currentConversationId = convId;
    const conv = conversationsData.find(c => c.id === convId);
    if (!conv) return;

    // Update chat header
    document.getElementById('chatUserAvatar').src = conv.avatar;
    document.getElementById('chatUsername').textContent = conv.name;
    document.getElementById('chatStatus').textContent = 'Active now';

    // Initialize or get variant messages for this conversation
    if (!messageVariants[convId]) {
        const variantIndex = (convId - 1) % variantMessages.length;
        messageVariants[convId] = [...variantMessages[variantIndex]];
    }

    // Display messages
    displayMessages(messageVariants[convId]);

    // Start message variation
    startMessageVariation(convId);
}

// Display messages
function displayMessages(messages) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;

    messagesContainer.innerHTML = '';

    messages.forEach(msg => {
        const messageElement = createMessageElement(msg);
        messagesContainer.appendChild(messageElement);
    });

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Create message element
function createMessageElement(msg) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${msg.sent ? 'sent' : 'received'}`;
    
    const avatar = msg.sent ? '' : `<img src="https://i.pravatar.cc/150?img=${currentConversationId}" alt="User" class="message-avatar">`;
    
    messageDiv.innerHTML = `
        ${avatar}
        <div>
            <div class="message-bubble">${msg.text}</div>
            <div class="message-time">${msg.time}</div>
        </div>
    `;

    return messageDiv;
}

// Start message variation - messages will change periodically
function startMessageVariation(convId) {
    // Clear any existing interval
    if (window.messageVariationInterval) {
        clearInterval(window.messageVariationInterval);
    }

    // Generate new variant messages every 5-10 seconds
    window.messageVariationInterval = setInterval(() => {
        if (currentConversationId === convId) {
            addVariantMessage(convId);
        }
    }, Math.random() * 5000 + 5000); // Random between 5-10 seconds
}

// Add variant message
function addVariantMessage(convId) {
    const newMessages = [
        'Hey, are you there?',
        'What are you up to?',
        'Just checking in!',
        'Did you see my last message?',
        'Hope you\'re having a great day!',
        'Quick question for you',
        'Thanks again!',
        'Let me know when you\'re free',
        'That sounds perfect!',
        'Can\'t wait to see you!'
    ];

    const sentMessages = [
        'Sure thing!',
        'Sounds good to me!',
        'I\'ll be there!',
        'Thanks!',
        'Perfect!',
        'Got it!',
        'Will do!',
        'Absolutely!',
        'No problem!',
        'Awesome!'
    ];

    // Randomly decide if message is sent or received
    const isSent = Math.random() > 0.5;
    const messagePool = isSent ? sentMessages : newMessages;
    const messageText = messagePool[Math.floor(Math.random() * messagePool.length)];

    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: 'numeric', 
        minute: '2-digit',
        hour12: true 
    });

    const newMessage = {
        text: messageText,
        time: timeString,
        sent: isSent
    };

    // Add to variant messages
    if (!messageVariants[convId]) {
        messageVariants[convId] = [];
    }
    messageVariants[convId].push(newMessage);

    // Display if this is the current conversation
    if (currentConversationId === convId) {
        const messagesContainer = document.getElementById('messagesContainer');
        const messageElement = createMessageElement(newMessage);
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// Send message functionality
function initSendMessage() {
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');

    if (!messageInput || !sendBtn) return;

    const sendMessage = () => {
        const text = messageInput.value.trim();
        if (!text) return;

        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });

        const newMessage = {
            text: text,
            time: timeString,
            sent: true
        };

        // Add to variant messages
        if (!messageVariants[currentConversationId]) {
            messageVariants[currentConversationId] = [];
        }
        messageVariants[currentConversationId].push(newMessage);

        // Display message
        const messagesContainer = document.getElementById('messagesContainer');
        const messageElement = createMessageElement(newMessage);
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Clear input
        messageInput.value = '';

        // Simulate response after 1-3 seconds
        setTimeout(() => {
            const responses = [
                'That\'s interesting!',
                'I see what you mean',
                'Thanks for letting me know!',
                'Got it!',
                'Sounds good!',
                'I\'ll check that out',
                'Thanks!',
                'Appreciate it!'
            ];
            const responseText = responses[Math.floor(Math.random() * responses.length)];
            
            const responseTime = new Date();
            const responseTimeString = responseTime.toLocaleTimeString('en-US', { 
                hour: 'numeric', 
                minute: '2-digit',
                hour12: true 
            });

            const responseMessage = {
                text: responseText,
                time: responseTimeString,
                sent: false
            };

            messageVariants[currentConversationId].push(responseMessage);
            const responseElement = createMessageElement(responseMessage);
            messagesContainer.appendChild(responseElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, Math.random() * 2000 + 1000);
    };

    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Update send button state
    messageInput.addEventListener('input', () => {
        sendBtn.disabled = !messageInput.value.trim();
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    initConversations();
    initSendMessage();
});

