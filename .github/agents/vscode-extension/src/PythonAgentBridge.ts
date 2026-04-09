import { spawn } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export interface AgentResponse {
    success: boolean;
    message: string;
    data?: any;
}

export class PythonAgentBridge {
    private pythonPath: string;
    private projectPath: string;
    private apiKey: string;

    constructor(pythonPath: string, projectPath: string, apiKey: string) {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.apiKey = apiKey;
    }

    updateConfig(pythonPath: string, projectPath: string, apiKey: string) {
        this.pythonPath = pythonPath;
        this.projectPath = projectPath;
        this.apiKey = apiKey;
    }

    async initializeAgent(): Promise<AgentResponse> {
        try {
            // Test if Python is available
            const pythonAvailable = await this.testPython();
            if (!pythonAvailable) {
                return {
                    success: false,
                    message: 'Python not found. Please configure the Python path in settings.'
                };
            }

            // Test if the vacation_agent project is accessible
            if (this.projectPath && !fs.existsSync(this.projectPath)) {
                return {
                    success: false,
                    message: `Project path not found: ${this.projectPath}`
                };
            }

            return {
                success: true,
                message: 'Vacation Agent initialized successfully!'
            };
        } catch (error) {
            return {
                success: false,
                message: `Initialization error: ${error}`
            };
        }
    }

    async testPython(): Promise<boolean> {
        return new Promise((resolve) => {
            const proc = spawn(this.pythonPath, ['--version']);
            proc.on('close', (code) => resolve(code === 0));
            proc.on('error', () => resolve(false));
        });
    }

    async sendGreeting(): Promise<AgentResponse> {
        return this.runPythonScript('greet');
    }

    async sendMessage(message: string): Promise<AgentResponse> {
        return this.runPythonScript('chat', message);
    }

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

    private runPythonScript(command: string, arg?: string): Promise<AgentResponse> {
        return new Promise((resolve) => {
            const scriptPath = path.join(__dirname, '..', 'python_wrapper.py');
            
            const env = { ...process.env };
            if (this.apiKey) {
                env.OPENAI_API_KEY = this.apiKey;
            }

            const args = [scriptPath, command];
            if (arg) {
                args.push(arg);
            }

            const workingDir = this.projectPath || path.join(__dirname, '..', '..');

            const proc = spawn(this.pythonPath, args, {
                cwd: workingDir,
                env,
                shell: process.platform === 'win32'
            });

            let output = '';
            let errorOutput = '';

            proc.stdout.on('data', (data) => {
                output += data.toString();
            });

            proc.stderr.on('data', (data) => {
                errorOutput += data.toString();
            });

            proc.on('close', (code) => {
                if (code === 0) {
                    try {
                        const response = JSON.parse(output.trim());
                        resolve(response);
                    } catch {
                        resolve({
                            success: true,
                            message: output.trim()
                        });
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
