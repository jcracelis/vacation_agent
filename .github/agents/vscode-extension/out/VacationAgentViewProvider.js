"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.VacationAgentViewProvider = void 0;
const vscode = __importStar(require("vscode"));
class VacationAgentViewProvider {
    constructor(extensionUri, bridge) {
        this.extensionUri = extensionUri;
        this.messageHistory = [];
        this.bridge = bridge;
    }
    async resolveWebviewView(webviewView, context, _token) {
        this.view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this.extensionUri]
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
        // Handle messages from the webview
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.command) {
                case 'sendMessage':
                    await this.handleUserMessage(message.text);
                    break;
                case 'startPlanning':
                    await this.handleStartPlanning();
                    break;
                case 'clearChat':
                    this.clearChat();
                    break;
            }
        });
        // Initialize with greeting
        await this.sendGreeting();
    }
    async sendGreeting() {
        this.addMessage('assistant', '🌴 Connecting to Vacation Agent...');
        const response = await this.bridge.sendGreeting();
        if (response.success) {
            this.addMessage('assistant', response.message);
        }
        else {
            this.addMessage('assistant', `⚠️ ${response.message}`);
        }
    }
    async handleUserMessage(text) {
        this.addMessage('user', text);
        // Show thinking indicator with rotating quotes
        await this.showThinkingWithQuotes();
        const response = await this.bridge.sendMessage(text);
        // Remove thinking indicator
        this.removeTypingIndicator();
        if (response.success) {
            this.addMessage('assistant', response.message);
        }
        else {
            this.addMessage('assistant', `⚠️ Error: ${response.message}`);
        }
    }
    /** Show a thinking indicator that cycles through travel quotes. */
    async showThinkingWithQuotes() {
        const quotes = [
            '🌴 "The world is a book..."',
            '✈️ "Travel makes one modest..."',
            '🏖️ "Life is either a daring adventure..."',
            '🗺️ "Not all those who wander are lost..."',
            '🌊 "The sea cures everything..."',
            '🌅 "Jobs fill your pockets, adventures fill your soul..."',
            '🧳 "Travel is the only thing you buy that makes you richer..."',
            '🌍 "Once a year, go someplace you\'ve never been before..."',
        ];
        // Show first quote immediately
        this.addMessage('assistant', quotes[0], true);
        // Rotate through remaining quotes every 2 seconds
        for (let i = 1; i < quotes.length; i++) {
            await new Promise(resolve => setTimeout(resolve, 2000));
            this.updateThinkingMessage(quotes[i]);
        }
    }
    /** Update the text of the current thinking indicator. */
    updateThinkingMessage(text) {
        this.postMessageToWebview({
            command: 'updateTyping',
            content: text
        });
    }
    async handleStartPlanning() {
        this.clearChat();
        await this.sendGreeting();
    }
    startNewPlanning() {
        this.clearChat();
        this.sendGreeting();
    }
    clearChat() {
        this.messageHistory = [];
        this.postMessageToWebview({
            command: 'clearChat'
        });
    }
    addMessage(role, content, isTyping = false) {
        this.messageHistory.push({ role, content });
        this.postMessageToWebview({
            command: 'addMessage',
            role,
            content,
            isTyping
        });
    }
    removeTypingIndicator() {
        this.postMessageToWebview({
            command: 'removeTyping'
        });
    }
    postMessageToWebview(message) {
        if (this.view) {
            this.view.webview.postMessage(message);
        }
    }
    getHtmlForWebview(webview) {
        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'chat.js'));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'chat.css'));
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource} 'unsafe-inline'; script-src ${webview.cspSource};">
            <link href="${styleUri}" rel="stylesheet">
            <title>Vacation Agent</title>
        </head>
        <body>
            <div id="chat-container">
                <div id="messages"></div>
                <div id="input-area">
                    <textarea 
                        id="message-input" 
                        placeholder="Ask about your dream vacation..."
                        rows="2"
                    ></textarea>
                    <button id="send-button">Send</button>
                </div>
            </div>
            <script src="${scriptUri}"></script>
        </body>
        </html>`;
    }
}
exports.VacationAgentViewProvider = VacationAgentViewProvider;
VacationAgentViewProvider.viewType = 'vacationAgent.chatView';
//# sourceMappingURL=VacationAgentViewProvider.js.map