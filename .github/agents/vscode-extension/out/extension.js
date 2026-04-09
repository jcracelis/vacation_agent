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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const VacationAgentViewProvider_1 = require("./VacationAgentViewProvider");
const PythonAgentBridge_1 = require("./PythonAgentBridge");
// ─── Extension Lifecycle ────────────────────────────────────────────────────
function activate(context) {
    console.log('🌴 Vacation Agent extension is now active');
    // ─── Read Configuration ─────────────────────────────────────────────
    const config = vscode.workspace.getConfiguration('vacationAgent');
    const pythonPath = config.get('pythonPath', 'python');
    const projectPath = config.get('projectPath', '');
    const openaiApiKey = config.get('openaiApiKey', '');
    const qwenApiKey = config.get('qwenApiKey', '');
    const ollamaBaseUrl = config.get('ollamaBaseUrl', 'http://localhost:11434');
    // ─── Create Bridge ──────────────────────────────────────────────────
    const bridge = new PythonAgentBridge_1.PythonAgentBridge(pythonPath, projectPath, openaiApiKey, qwenApiKey, ollamaBaseUrl);
    // ─── Register View Provider ─────────────────────────────────────────
    const viewProvider = new VacationAgentViewProvider_1.VacationAgentViewProvider(context.extensionUri, bridge);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(VacationAgentViewProvider_1.VacationAgentViewProvider.viewType, viewProvider, { webviewOptions: { retainContextWhenHidden: true } }));
    // ─── Register Commands ──────────────────────────────────────────────
    context.subscriptions.push(vscode.commands.registerCommand('vacationAgent.startPlanning', () => {
        vscode.commands.executeCommand('vacationAgent.chatView.focus');
        viewProvider.startNewPlanning();
    }));
    context.subscriptions.push(vscode.commands.registerCommand('vacationAgent.clearChat', () => {
        viewProvider.clearChat();
    }));
    // ─── Watch for Configuration Changes ────────────────────────────────
    context.subscriptions.push(vscode.workspace.onDidChangeConfiguration((e) => {
        if (!e.affectsConfiguration('vacationAgent')) {
            return;
        }
        const newConfig = vscode.workspace.getConfiguration('vacationAgent');
        bridge.updateConfig(newConfig.get('pythonPath', 'python'), newConfig.get('projectPath', ''), newConfig.get('openaiApiKey', ''), newConfig.get('qwenApiKey', ''), newConfig.get('ollamaBaseUrl', 'http://localhost:11434'));
    }));
}
function deactivate() {
    // Cleanup if needed
}
//# sourceMappingURL=extension.js.map