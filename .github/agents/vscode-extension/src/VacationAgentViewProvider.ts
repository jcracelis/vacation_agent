import * as vscode from 'vscode';
import { PythonAgentBridge } from './PythonAgentBridge';

export class VacationAgentViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'vacationAgent.chatView';

    private view?: vscode.WebviewView;
    private bridge: PythonAgentBridge;
    private messageHistory: Array<{ role: string; content: string }> = [];

    constructor(
        private readonly extensionUri: vscode.Uri,
        bridge: PythonAgentBridge
    ) {
        this.bridge = bridge;
    }

    public async resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
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

    private async sendGreeting() {
        this.addMessage('assistant', '🌴 Connecting to Vacation Agent...');
        
        const response = await this.bridge.sendGreeting();
        
        if (response.success) {
            this.addMessage('assistant', response.message);
        } else {
            this.addMessage('assistant', `⚠️ ${response.message}`);
        }
    }

    private async handleUserMessage(text: string) {
        this.addMessage('user', text);

        // Show thinking indicator with rotating quotes
        await this.showThinkingWithQuotes();

        const response = await this.bridge.sendMessage(text);

        // Remove thinking indicator
        this.removeTypingIndicator();

        if (response.success) {
            this.addMessage('assistant', response.message);
        } else {
            this.addMessage('assistant', `⚠️ Error: ${response.message}`);
        }
    }

    /** Show a thinking indicator that cycles through travel quotes. */
    private async showThinkingWithQuotes() {
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
    private updateThinkingMessage(text: string) {
        this.postMessageToWebview({
            command: 'updateTyping',
            content: text
        });
    }

    private async handleStartPlanning() {
        this.clearChat();
        await this.sendGreeting();
    }

    public startNewPlanning() {
        this.clearChat();
        this.sendGreeting();
    }

    public clearChat() {
        this.messageHistory = [];
        this.postMessageToWebview({
            command: 'clearChat'
        });
    }

    private addMessage(role: string, content: string, isTyping = false) {
        this.messageHistory.push({ role, content });
        this.postMessageToWebview({
            command: 'addMessage',
            role,
            content,
            isTyping
        });
    }

    private removeTypingIndicator() {
        this.postMessageToWebview({
            command: 'removeTyping'
        });
    }

    private postMessageToWebview(message: any) {
        if (this.view) {
            this.view.webview.postMessage(message);
        }
    }

    private getHtmlForWebview(webview: vscode.Webview): string {
        const scriptUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, 'media', 'chat.js')
        );
        const styleUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, 'media', 'chat.css')
        );

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
