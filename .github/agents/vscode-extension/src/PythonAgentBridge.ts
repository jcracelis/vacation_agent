import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

// ─── Types ──────────────────────────────────────────────────────────────────

export interface AgentResponse {
    success: boolean;
    message: string;
    provider?: string;
    model?: string;
    llmAvailable?: boolean;
    data?: any;
}

// ─── Python Agent Bridge ────────────────────────────────────────────────────

export class PythonAgentBridge {
    private pythonPath: string;
    private projectPath: string;
    private openaiApiKey: string;
    private qwenApiKey: string;
    private ollamaBaseUrl: string;

    /**
     * Create a bridge to the Python vacation agent.
     *
     * @param pythonPath     Path to Python executable
     * @param projectPath    Path to the agents/ project root
     * @param openaiApiKey   OpenAI API key (optional)
     * @param qwenApiKey     Qwen DashScope API key (optional)
     * @param ollamaBaseUrl  Ollama server URL (default http://localhost:11434)
     */
    constructor(
        pythonPath: string,
        projectPath: string,
        openaiApiKey: string = '',
        qwenApiKey: string = '',
        ollamaBaseUrl: string = 'http://localhost:11434'
    ) {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.openaiApiKey = openaiApiKey;
        this.qwenApiKey = qwenApiKey;
        this.ollamaBaseUrl = ollamaBaseUrl;
    }

    /** Update all configuration at once. */
    updateConfig(
        pythonPath: string,
        projectPath: string,
        openaiApiKey: string = '',
        qwenApiKey: string = '',
        ollamaBaseUrl: string = 'http://localhost:11434'
    ) {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.openaiApiKey = openaiApiKey;
        this.qwenApiKey = qwenApiKey;
        this.ollamaBaseUrl = ollamaBaseUrl;
    }

    // ─── Initialization ─────────────────────────────────────────────────

    /** Test whether the Python agent can be reached. */
    async initializeAgent(): Promise<AgentResponse> {
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
    async testPython(): Promise<boolean> {
        return new Promise((resolve) => {
            const proc = spawn(this.pythonPath, ['--version']);
            proc.on('close', (code) => resolve(code === 0));
            proc.on('error', () => resolve(false));
        });
    }

    // ─── Agent Commands ─────────────────────────────────────────────────

    /** Send the initial greeting. */
    async sendGreeting(): Promise<AgentResponse> {
        return this.runPythonScript('greet');
    }

    /** Send a chat message and get the response. */
    async sendMessage(message: string): Promise<AgentResponse> {
        return this.runPythonScript('chat', message);
    }

    /** Request a destination recommendation. */
    async planDestination(
        preference: string,
        duration: number,
        budget: number,
        travelers: number
    ): Promise<AgentResponse> {
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
    private runPythonScript(command: string, arg?: string): Promise<AgentResponse> {
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
            const proc = spawn(this.pythonPath, args, {
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
                        const response: AgentResponse = JSON.parse(output.trim());
                        resolve(response);
                    } catch {
                        // Not JSON — return as plain text
                        resolve({ success: true, message: output.trim() });
                    }
                } else {
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
