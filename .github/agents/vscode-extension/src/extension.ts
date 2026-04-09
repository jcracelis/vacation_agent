import * as vscode from 'vscode';
import { VacationAgentViewProvider } from './VacationAgentViewProvider';
import { PythonAgentBridge } from './PythonAgentBridge';

export function activate(context: vscode.ExtensionContext) {
    console.log('Vacation Agent extension is now active');

    // Create the Python agent bridge
    const config = vscode.workspace.getConfiguration('vacationAgent');
    const pythonPath = config.get<string>('pythonPath', 'python');
    const projectPath = config.get<string>('projectPath', '');
    const openaiApiKey = config.get<string>('openaiApiKey', '');
    const qwenApiKey = config.get<string>('qwenApiKey', '');

    const bridge = new PythonAgentBridge(pythonPath, projectPath, openaiApiKey, qwenApiKey);

    // Register the view provider
    const viewProvider = new VacationAgentViewProvider(context.extensionUri, bridge);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            VacationAgentViewProvider.viewType,
            viewProvider,
            { webviewOptions: { retainContextWhenHidden: true } }
        )
    );

    // Register commands
    const startPlanningCommand = vscode.commands.registerCommand(
        'vacationAgent.startPlanning',
        () => {
            vscode.commands.executeCommand('vacationAgent.chatView.focus');
            viewProvider.startNewPlanning();
        }
    );

    const clearChatCommand = vscode.commands.registerCommand(
        'vacationAgent.clearChat',
        () => {
            viewProvider.clearChat();
        }
    );

    context.subscriptions.push(startPlanningCommand, clearChatCommand);

    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration((e) => {
            if (e.affectsConfiguration('vacationAgent')) {
                const newConfig = vscode.workspace.getConfiguration('vacationAgent');
                bridge.updateConfig(
                    newConfig.get<string>('pythonPath', 'python'),
                    newConfig.get<string>('projectPath', ''),
                    newConfig.get<string>('openaiApiKey', ''),
                    newConfig.get<string>('qwenApiKey', '')
                );
            }
        })
    );
}

export function deactivate() {
    // Cleanup if needed
}
