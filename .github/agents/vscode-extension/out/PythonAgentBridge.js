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
exports.PythonAgentBridge = void 0;
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
// ─── Python Agent Bridge ────────────────────────────────────────────────────
class PythonAgentBridge {
    /**
     * Create a bridge to the Python vacation agent.
     *
     * @param pythonPath     Path to Python executable
     * @param projectPath    Path to the agents/ project root
     * @param openaiApiKey   OpenAI API key (optional)
     * @param qwenApiKey     Qwen DashScope API key (optional)
     * @param ollamaBaseUrl  Ollama server URL (default http://localhost:11434)
     */
    constructor(pythonPath, projectPath, openaiApiKey = '', qwenApiKey = '', ollamaBaseUrl = 'http://localhost:11434') {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.openaiApiKey = openaiApiKey;
        this.qwenApiKey = qwenApiKey;
        this.ollamaBaseUrl = ollamaBaseUrl;
    }
    /** Update all configuration at once. */
    updateConfig(pythonPath, projectPath, openaiApiKey = '', qwenApiKey = '', ollamaBaseUrl = 'http://localhost:11434') {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.openaiApiKey = openaiApiKey;
        this.qwenApiKey = qwenApiKey;
        this.ollamaBaseUrl = ollamaBaseUrl;
    }
    // ─── Initialization ─────────────────────────────────────────────────
    /** Test whether the Python agent can be reached. */
    async initializeAgent() {
        const pythonAvailable = await this.testPython();
        if (!pythonAvailable) {
            return {
                success: false,
                message: 'Python not found. Please configure the Python path in settings.'
            };
        }
        if (this.projectPath && !fs.existsSync(this.projectPath)) {
            return {
                success: false,
                message: `Project path not found: ${this.projectPath}`
            };
        }
        return { success: true, message: 'Vacation Agent initialized successfully!' };
    }
    /** Quick smoke test: can we run Python? */
    async testPython() {
        return new Promise((resolve) => {
            const proc = (0, child_process_1.spawn)(this.pythonPath, ['--version']);
            proc.on('close', (code) => resolve(code === 0));
            proc.on('error', () => resolve(false));
        });
    }
    // ─── Agent Commands ─────────────────────────────────────────────────
    /** Send the initial greeting. */
    async sendGreeting() {
        return this.runPythonScript('greet');
    }
    /** Send a chat message and get the response. */
    async sendMessage(message) {
        return this.runPythonScript('chat', message);
    }
    /** Request a destination recommendation. */
    async planDestination(preference, duration, budget, travelers) {
        return this.runPythonScript('plan_destination', JSON.stringify({
            preference,
            duration_days: duration,
            budget,
            travelers
        }));
    }
    // ─── Internal: Script Execution ─────────────────────────────────────
    /**
     * Spawn a Python subprocess and return the parsed JSON response.
     *
     * @param command  Command name (greet, chat, plan_destination)
     * @param arg      Optional argument (JSON or plain string)
     */
    runPythonScript(command, arg) {
        return new Promise((resolve) => {
            const scriptPath = path.join(__dirname, '..', 'python_wrapper.py');
            // Build environment with API keys
            const env = { ...process.env };
            if (this.openaiApiKey) {
                env.OPENAI_API_KEY = this.openaiApiKey;
            }
            if (this.qwenApiKey) {
                env.QWEN_API_KEY = this.qwenApiKey;
            }
            if (this.ollamaBaseUrl) {
                env.OLLAMA_BASE_URL = this.ollamaBaseUrl;
            }
            // Build command-line arguments
            const args = [scriptPath, command];
            if (arg) {
                args.push(arg);
            }
            // Determine working directory
            const workingDir = this.projectPath || path.join(__dirname, '..', '..');
            // Spawn the Python process
            const proc = (0, child_process_1.spawn)(this.pythonPath, args, {
                cwd: workingDir,
                env,
                shell: process.platform === 'win32'
            });
            let output = '';
            let errorOutput = '';
            proc.stdout.on('data', (data) => { output += data.toString(); });
            proc.stderr.on('data', (data) => { errorOutput += data.toString(); });
            proc.on('close', (code) => {
                if (code === 0) {
                    try {
                        const response = JSON.parse(output.trim());
                        resolve(response);
                    }
                    catch {
                        // Not JSON — return as plain text
                        resolve({ success: true, message: output.trim() });
                    }
                }
                else {
                    resolve({
                        success: false,
                        message: errorOutput || 'Unknown error occurred'
                    });
                }
            });
            proc.on('error', (err) => {
                resolve({
                    success: false,
                    message: `Failed to start Python process: ${err.message}`
                });
            });
        });
    }
}
exports.PythonAgentBridge = PythonAgentBridge;
//# sourceMappingURL=PythonAgentBridge.js.map