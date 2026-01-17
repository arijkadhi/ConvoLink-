// app.js - Complete Frontend Logic
const API_URL = "http://localhost:8000/api/v1";

let currentUser = null;
let currentConversationId = null;
let conversations = [];

// ============ Utility Functions ============
function saveToken(token) {
  localStorage.setItem("token", token);
}

function getToken() {
  return localStorage.getItem("token");
}

function clearToken() {
  localStorage.removeItem("token");
}

async function apiFetch(endpoint, options = {}) {
  const token = getToken();
  const headers = options.headers || {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return fetch(`${API_URL}${endpoint}`, { ...options, headers });
}

function showAlert(elementId, message, type = 'info') {
  const alertDiv = document.getElementById(elementId);
  alertDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
  setTimeout(() => alertDiv.innerHTML = '', 5000);
}

function formatDate(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`;
  return date.toLocaleDateString();
}

// ============ Auth Functions ============
async function register() {
  const username = document.getElementById("reg-username").value;
  const email = document.getElementById("reg-email").value;
  const password = document.getElementById("reg-password").value;

  if (!username || !email || !password) {
    showAlert('register-alert', 'Please fill all fields', 'error');
    return;
  }

  try {
    const res = await apiFetch("/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    if (res.ok) {
      const data = await res.json();
      showAlert('register-alert', `✅ Registration successful! Check your email (${email}) for welcome message!`, 'success');
      // Clear form
      document.getElementById("reg-username").value = '';
      document.getElementById("reg-email").value = '';
      document.getElementById("reg-password").value = '';
    } else {
      const error = await res.json();
      showAlert('register-alert', `❌ ${error.detail}`, 'error');
    }
  } catch (error) {
    showAlert('register-alert', `❌ Error: ${error.message}`, 'error');
  }
}

async function login() {
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  if (!username || !password) {
    showAlert('login-alert', 'Please fill all fields', 'error');
    return;
  }

  try {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await apiFetch("/auth/login", {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      saveToken(data.access_token);
      showAlert('login-alert', '✅ Login successful!', 'success');
      setTimeout(() => {
        loadApp();
      }, 1000);
    } else {
      const error = await res.json();
      showAlert('login-alert', `❌ ${error.detail}`, 'error');
    }
  } catch (error) {
    showAlert('login-alert', `❌ Error: ${error.message}`, 'error');
  }
}

function logout() {
  clearToken();
  currentUser = null;
  currentConversationId = null;
  conversations = [];
  document.getElementById('auth-container').classList.remove('hidden');
  document.getElementById('app-container').classList.add('hidden');
  document.getElementById('user-info').style.display = 'none';
}

async function loadApp() {
  try {
    // Get current user
    const res = await apiFetch("/auth/me");
    if (res.ok) {
      currentUser = await res.json();
      document.getElementById('username-display').textContent = `👤 ${currentUser.username}`;
      document.getElementById('user-info').style.display = 'flex';
      document.getElementById('auth-container').classList.add('hidden');
      document.getElementById('app-container').classList.remove('hidden');
      
      // Load conversations
      await loadConversations();
    } else {
      logout();
    }
  } catch (error) {
    console.error('Error loading app:', error);
    logout();
  }
}

// ============ Conversations Functions ============
async function loadConversations() {
  try {
    const res = await apiFetch("/conversations");
    if (res.ok) {
      conversations = await res.json();
      renderConversations();
    } else {
      console.error('Failed to load conversations');
    }
  } catch (error) {
    console.error('Error loading conversations:', error);
  }
}

function renderConversations() {
  const container = document.getElementById('conversations-list');
  
  if (conversations.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No conversations yet.<br>Send a message to start!</p></div>';
    return;
  }

  container.innerHTML = conversations.map(conv => {
    const otherUser = conv.user1.id === currentUser.id ? conv.user2 : conv.user1;
    const lastMsg = conv.last_message ? conv.last_message.content : 'No messages yet';
    const time = conv.last_message ? formatDate(conv.last_message.created_at) : '';
    const isActive = currentConversationId === conv.id ? 'active' : '';
    
    return `
      <div class="conversation-item ${isActive}" onclick="selectConversation(${conv.id})">
        <div class="conversation-header">
          <span class="conversation-users">👤 ${otherUser.username}</span>
          <span class="conversation-time">${time}</span>
        </div>
        <div class="last-message">${lastMsg}</div>
      </div>
    `;
  }).join('');
}

async function selectConversation(convId) {
  currentConversationId = convId;
  renderConversations(); // Update active state
  await loadMessages(convId);
}

// ============ Messages Functions ============
async function loadMessages(convId) {
  try {
    const res = await apiFetch(`/conversations/${convId}/messages`);
    if (res.ok) {
      const messages = await res.json();
      renderMessages(messages);
      
      // Show messages area
      document.getElementById('no-conversation-selected').style.display = 'none';
      document.getElementById('messages-header').style.display = 'block';
      document.getElementById('messages-content').classList.remove('hidden');
      document.getElementById('current-conv-id').textContent = convId;
      
      // Scroll to bottom
      const container = document.getElementById('messages-container');
      container.scrollTop = container.scrollHeight;
    }
  } catch (error) {
    console.error('Error loading messages:', error);
  }
}

function renderMessages(messages) {
  const container = document.getElementById('messages-container');
  
  if (messages.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No messages in this conversation yet.</p></div>';
    return;
  }

  container.innerHTML = messages.map(msg => {
    const isSent = msg.sender_id === currentUser.id;
    const className = isSent ? 'message-sent' : 'message-received';
    const time = formatDate(msg.created_at);
    const status = msg.is_read ? '✓✓' : '✓';
    
    return `
      <div class="message ${className}">
        <div>${msg.content}</div>
        <div class="message-info">${time} ${isSent ? status : ''}</div>
      </div>
    `;
  }).join('');
}

async function sendReply() {
  if (!currentConversationId) return;
  
  const content = document.getElementById('reply-message').value.trim();
  if (!content) {
    alert('Please enter a message');
    return;
  }

  try {
    // Get receiver from current conversation
    const conv = conversations.find(c => c.id === currentConversationId);
    const receiverId = conv.user1.id === currentUser.id ? conv.user2.id : conv.user1.id;

    const res = await apiFetch("/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        receiver_id: receiverId,
        content: content
      })
    });

    if (res.ok) {
      document.getElementById('reply-message').value = '';
      await loadMessages(currentConversationId);
      await loadConversations(); // Refresh to update last message
    } else {
      const error = await res.json();
      alert(`Error: ${error.detail}`);
    }
  } catch (error) {
    console.error('Error sending message:', error);
    alert('Failed to send message');
  }
}

async function sendNewMessage() {
  const receiverId = document.getElementById('new-receiver-id').value;
  const content = document.getElementById('new-message-content').value.trim();

  if (!receiverId || !content) {
    alert('Please enter both receiver ID and message');
    return;
  }

  try {
    const res = await apiFetch("/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        receiver_id: parseInt(receiverId),
        content: content
      })
    });

    if (res.ok) {
      const message = await res.json();
      document.getElementById('new-receiver-id').value = '';
      document.getElementById('new-message-content').value = '';
      
      alert('✅ Message sent! The receiver will get an email notification!');
      
      // Reload conversations and select the new one
      await loadConversations();
      if (message.conversation_id) {
        await selectConversation(message.conversation_id);
      }
    } else {
      const error = await res.json();
      alert(`Error: ${error.detail}`);
    }
  } catch (error) {
    console.error('Error sending message:', error);
    alert('Failed to send message');
  }
}

// ============ Initialize ============
window.addEventListener('DOMContentLoaded', () => {
  // Check if already logged in
  if (getToken()) {
    loadApp();
  }
  
  // Add enter key handlers
  document.getElementById('reply-message').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendReply();
    }
  });
});
