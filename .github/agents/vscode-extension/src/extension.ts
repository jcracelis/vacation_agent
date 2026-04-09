import * as vscode from 'vscode';
import { VacationAgentViewProvider } from './VacationAgentViewProvider';
import { PythonAgentBridge } from './PythonAgentBridge';

// ─── Extension Lifecycle ────────────────────────────────────────────────────

export function activate(context: vscode.ExtensionContext) {
    console.log('🌴 Vacation Agent extension is now active');

    // ─── Read Configuration ─────────────────────────────────────────────
    const config = vscode.workspace.getConfiguration('vacationAgent');
    const pythonPath = config.get<string>('pythonPath', 'python');
    const projectPath = config.get<string>('projectPath', '');
    const openaiApiKey = config.get<string>('openaiApiKey', '');
    const qwenApiKey = config.get<string>('qwenApiKey', '');
    const ollamaBaseUrl = config.get<string>('ollamaBaseUrl', 'http://localhost:11434');

    // ─── Create Bridge ──────────────────────────────────────────────────
    const bridge = new PythonAgentBridge(
        pythonPath,
        projectPath,
        openaiApiKey,
        qwenApiKey,
        ollamaBaseUrl
    );

    // ─── Register View Provider ─────────────────────────────────────────
    const viewProvider = new VacationAgentViewProvider(
        context.extensionUri,
        bridge
    );

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            VacationAgentViewProvider.viewType,
            viewProvider,
            { webviewOptions: { retainContextWhenHidden: true } }
        )
    );

    // ─── Register Commands ──────────────────────────────────────────────
    context.subscriptions.push(
        vscode.commands.registerCommand('vacationAgent.startPlanning', () => {
            vscode.commands.executeCommand('vacationAgent.chatView.focus');
            viewProvider.startNewPlanning();
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('vacationAgent.clearChat', () => {
            viewProvider.clearChat();
        })
    );

    // ─── Watch for Configuration Changes ────────────────────────────────
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration((e) => {
            if (!e.affectsConfiguration('vacationAgent')) {
                return;
            }
            const newConfig = vscode.workspace.getConfiguration('vacationAgent');
            bridge.updateConfig(
                newConfig.get<string>('pythonPath', 'python'),
                newConfig.get<string>('projectPath', ''),
                newConfig.get<string>('openaiApiKey', ''),
                newConfig.get<string>('qwenApiKey', ''),
                newConfig.get<string>('ollamaBaseUrl', 'http://localhost:11434')
            );
        })
    );
}

export function deactivate() {
    // Cleanup if needed
}
