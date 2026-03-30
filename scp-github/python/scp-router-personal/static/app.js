/**
 * SCP Router Management - Core Logic v3.2
 */

// Configuration
const API_URL = 'http://localhost:8000';
let sessionId = null;
let triSum = 0;
let savingsSum = 0;
let messageCount = 0;

// DOM Elements
const appContainer = document.querySelector('.app-container');
const sidebarToggle = document.getElementById('sidebarToggle');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const newSessionBtn = document.getElementById('newSessionBtn');
const modelSelect = document.getElementById('modelSelect');
const domainSelect = document.getElementById('domainSelect');
const compressionSelect = document.getElementById('compressionSelect');
const showStatsCheckbox = document.getElementById('showStatsCheckbox');
const dryRunCheckbox = document.getElementById('dryRunCheckbox');
const avgTRISpan = document.getElementById('avgTRI');
const avgSavingsSpan = document.getElementById('avgSavings');
const sessionHistoryList = document.getElementById('sessionHistory');
const activeAnchorsList = document.getElementById('activeAnchorsList');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initSession();
    loadHistory();
    fetchAnchors();
    
    // Sidebar Toggle
    sidebarToggle.addEventListener('click', () => {
        appContainer.classList.toggle('sidebar-collapsed');
        const icon = sidebarToggle.querySelector('i');
        if (appContainer.classList.contains('sidebar-collapsed')) {
            icon.setAttribute('data-lucide', 'panel-left-open');
        } else {
            icon.setAttribute('data-lucide', 'panel-left-close');
        }
        lucide.createIcons();
    });
});

// Create Session
async function initSession() {
    try {
        const response = await fetch(`${API_URL}/v3/sessions`, { method: 'POST' });
        const data = await response.json();
        sessionId = data.session_id;
        console.log('Session initialized:', sessionId);
        
        // Save to local history
        saveHistory(sessionId, 'Active Session');
        updateHistoryUI();
        return sessionId;
    } catch (error) {
        console.error('Session init failed:', error);
        addMessage('assistant', 'System offline. Ensure local gateway is running.');
    }
}

// History Management
function saveHistory(id, label) {
    let history = JSON.parse(localStorage.getItem('scp_history') || '[]');
    // Only add if not already present
    if (!history.find(h => h.id === id)) {
        history.unshift({ id, label, time: new Date().toISOString() });
        // Keep only last 10
        history = history.slice(0, 10);
        localStorage.setItem('scp_history', JSON.stringify(history));
    }
}

function loadHistory() {
    updateHistoryUI();
}

function updateHistoryUI() {
    const history = JSON.parse(localStorage.getItem('scp_history') || '[]');
    if (history.length === 0) return;

    // Preserve the header but clear old items
    const header = sessionHistoryList.querySelector('label');
    sessionHistoryList.innerHTML = '';
    sessionHistoryList.appendChild(header);

    history.forEach(item => {
        const div = document.createElement('div');
        div.className = `history-item ${item.id === sessionId ? 'active' : ''}`;
        div.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; width: 100%;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i data-lucide="message-square" size="14"></i>
                    <span style="font-size: 0.8rem;">${item.id}</span>
                </div>
                <span style="font-size: 0.6rem; color: var(--text-muted);">${new Date(item.time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            </div>
        `;
        div.onclick = () => {
            sessionId = item.id;
            updateHistoryUI();
            addMessage('assistant', `Resumed session ${item.id}. History recovery pending backend integration.`);
        };
        sessionHistoryList.appendChild(div);
    });
    lucide.createIcons();
}

// Anchor Management
async function fetchAnchors() {
    const domain = domainSelect.value;
    try {
        const response = await fetch(`${API_URL}/v3/anchors?domain=${domain}`);
        const data = await response.json();
        
        activeAnchorsList.innerHTML = '';
        data.anchors.forEach(a => {
            const span = document.createElement('span');
            span.className = 'anchor-tag';
            span.style = 'padding: 4px 10px; background: rgba(99, 102, 241, 0.1); border: 1px solid var(--primary); border-radius: 6px; font-size: 0.75rem; color: var(--primary); font-weight: 500; cursor: help;';
            span.textContent = a.code;
            span.title = a.expansion + ': ' + a.definition;
            activeAnchorsList.appendChild(span);
        });
    } catch (e) {
        console.error('Anchor fetch failed:', e);
    }
}

// Message Components
function addMessage(role, content, metrics = null) {
    const wrapper = document.createElement('div');
    wrapper.className = `msg-wrapper ${role}`;
    
    let metricsHtml = '';
    if (metrics && role === 'assistant' && showStatsCheckbox.checked) {
        const triScore = (metrics.tri * 100).toFixed(1);
        const savings = (metrics.compression_savings * 100).toFixed(1);
        const dryRunTag = metrics.model_used === 'dry-run-mock' ? '<span style="color: var(--accent-rose); border: 1px solid var(--accent-rose); padding: 1px 4px; border-radius: 4px; margin-right: 8px;">MOCK</span>' : '';
        
        metricsHtml = `
            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 15px; font-size: 0.7rem; color: var(--text-muted);">
                ${dryRunTag}
                <span>TRI: <b style="color: var(--accent-teal)">${triScore}%</b></span>
                <span>Savings: <b style="color: var(--accent-purple)">${savings}%</b></span>
            </div>
        `;
        updateGlobalStats(metrics);
    }

    wrapper.innerHTML = `
        <div class="bubble">
            <p>${escapeHtml(content).replace(/\n/g, '<br>')}</p>
            ${metricsHtml}
        </div>
        <div class="msg-meta">
            ${role === 'user' ? '<span>You</span>' : '<span>AI Assistant</span>'}
            <span>${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
        </div>
    `;
    
    chatMessages.appendChild(wrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    lucide.createIcons();
}

function updateGlobalStats(metrics) {
    if (metrics.tri) {
        triSum += metrics.tri;
        savingsSum += metrics.compression_savings;
        messageCount++;
        avgTRISpan.textContent = `${(triSum / messageCount * 100).toFixed(1)}%`;
        avgSavingsSpan.textContent = `${(savingsSum / messageCount * 100).toFixed(1)}%`;
    }
}

// Communication
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Lock UI
    messageInput.value = '';
    messageInput.style.height = 'auto';
    addMessage('user', message);
    
    // Loading State
    const loadingId = 'loading-' + Date.now();
    const loadingWrapper = document.createElement('div');
    loadingWrapper.className = 'msg-wrapper assistant';
    loadingWrapper.id = loadingId;
    loadingWrapper.innerHTML = `
        <div class="bubble" style="display: flex; align-items: center; gap: 10px;">
            <div class="loading-spinner"></div>
            <span style="font-size: 0.85rem; color: var(--text-muted);">Compressing protocol...</span>
        </div>
    `;
    chatMessages.appendChild(loadingWrapper);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/v3/route`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                message: message,
                domain: domainSelect.value,
                compression: compressionSelect.value,
                model: modelSelect.value,
                show_stats: showStatsCheckbox.checked,
                dry_run: dryRunCheckbox.checked
            })
        });

        const data = await response.json();
        document.getElementById(loadingId).remove();
        
        if (data.response) {
            addMessage('assistant', data.response, data.metrics);
        } else {
            addMessage('assistant', 'Gateway reported an error.');
        }
    } catch (e) {
        document.getElementById(loadingId).remove();
        addMessage('assistant', 'Connection lost. Retrying protocol handshake...');
    }
}

// Helpers
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

sendBtn.addEventListener('click', sendMessage);
newSessionBtn.addEventListener('click', () => {
    chatMessages.innerHTML = '';
    initSession();
});

domainSelect.addEventListener('change', fetchAnchors);

// Spinner CSS
const style = document.createElement('style');
style.textContent = `
    .loading-spinner {
        width: 16px;
        height: 16px;
        border: 2px solid var(--border);
        border-top: 2px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
`;
document.head.appendChild(style);
